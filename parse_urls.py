import os
import re
import json
import time
from bs4 import BeautifulSoup

import multiprocessing
from multiprocessing import cpu_count, Pool

# docs used for development: 5, 26045, 17629, 31128, 3, 21, 168, 146, 166, 6

def remove_eol(x):
    x = re.sub('\n','',x)
    # remove empty lines
    x = os.linesep.join([s for s in x.splitlines() if s])
    # remove extra, leading and trailing whitespace
    x = ' '.join(x.split()).strip()
    return x


def parse_doc(docname):
    
    with open('./data/docs/raw/' + docname, 'r', encoding='utf8') as file:
        raw_doc = file.read()
    
    my_soup = BeautifulSoup(raw_doc,my_parser)
    
    try:
        my_title = my_soup.find_all('title')[0].text
    except:
        my_title = ''
    
    my_article = str(my_soup.find_all('div',{'class': 'sticky-text-column'}))
    
    if my_article == '[]':
        return
    
    match = re.search(r'\d{4}-\d{2}-\d{2}', my_article)
    my_date = match.group() # returns the 1st match only
    
    my_soup_1 = BeautifulSoup(my_article,my_parser)
    
    # first, search for headings among the strong tags at the beginning of the article
    # (this is to address the problem of, e.g., '5.txt')
    if '<strong>' in str(my_soup_1):
        test = str(my_soup_1).find('<strong>')
        if test < 1300:
            try:
                my_heading = my_soup_1.find_all('strong')[0].text
            except:
                my_heading = ''
        else:
            my_heading = ''
    else:
        my_heading = ''
    
    # then, try the first paragraph of the article text. Select if it appears elsewhere (e.g., see '168.txt')
    if my_heading == '':
        candidate_heading = str(my_soup_1).split('</p><!-- Fin Date --><!-- TEXTE --><p>')[1].split('</p><p>')[0]
        
        if str(my_soup).count(re.sub('"','&quot;',candidate_heading)) >= 1:
            my_heading = BeautifulSoup(candidate_heading,my_parser).text
        else:
            my_heading = ''
    
    my_article_text = my_soup_1.text
    
    # remove footer of embedded video
    try:
        to_remove = my_soup_1.find_all('div',{'class': 'daily-motion-footer'})[0].text
        my_article_text = re.sub(to_remove,'',my_article_text)
    except:
        pass
    
    # remove first and last chars if square brackets
    if my_article_text[0] == '[':
        my_article_text = my_article_text[1:]
    
    if my_article_text[-1] == ']':
        my_article_text = my_article_text[:-1]
    
    if not my_heading == '':
        # remove everything before the heading (including the heading)
        my_article_text = my_article_text.split(my_heading)[1]
    else:
        # remove everything before the first paragraph, e.g., "AFP</span></span>, publié le jeudi 02 juillet 2020 à 21h05</p><!-- Fin Date --><!-- TEXTE --><p>"
        my_article_text = ' '.join(my_article_text.split('\n')[1:])
    
    # remove embedded code
    try:
        my_article_text = my_article_text.split('window.pvp')[0] + my_article_text.split('});')[1]
    except:
        pass
    
    my_article_text = remove_eol(my_article_text)
    my_heading = remove_eol(my_heading)
    
    my_dict = {'date' : my_date,
               'title' : my_title,
               'heading' : my_heading,
               'article' : my_article_text}
    
    with open('./data/docs/parsed/' + re.sub('.txt','.json',docname), 'w', encoding='utf8') as file:
        json.dump(my_dict, file, sort_keys=True, indent=4, ensure_ascii=False)

# = = = = 

n_cores = cpu_count()
my_parser = 'lxml'

raw_docs_names = os.listdir('./data/docs/raw/')

parsed_docs_names = os.listdir('./data/docs/parsed/') # from previous runs

parsed_docs_names = set([elt.split('.')[0] for elt in parsed_docs_names]) # remove file extension, keep index

raw_docs_names = [elt for elt in raw_docs_names if elt.split('.')[0] not in parsed_docs_names]

start_time = time.time()

print(n_cores,'core(s) will be used')

pool = Pool(processes=n_cores)
pool.map(parse_doc, raw_docs_names)
pool.close()
pool.join()

print('= = = done in',round(time.time() - start_time,2),'sec(s)= = =')
