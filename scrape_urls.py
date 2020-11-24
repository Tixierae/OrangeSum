import time
import multiprocessing
import urllib.request
from bs4 import BeautifulSoup
from multiprocessing import cpu_count, Pool

def scrape_one_url(my_list):
    
    my_idx, _, my_url, = my_list
    
    try:
        resp = urllib.request.urlopen(my_url)
        my_soup = str(BeautifulSoup(resp, my_parser, from_encoding=resp.info().get_param('charset')))
        with open('./data/docs/raw/' + str(my_idx) + '.txt', 'w', encoding='utf8') as file:
            file.write(my_soup)
    except:
        pass

# = = = = 

n_cores = cpu_count()
my_parser = 'lxml'

# = = get unique urls = =

with open('./data/links/urls.txt', 'r', encoding='utf8') as file:
    cat_urls = file.read().splitlines()

# '=====' was added manually at the end of urls.txt to separate new URLs from that of previous runs
idx_new = [idx for idx,elt in enumerate(cat_urls) if '=====' in elt]

# we don't want to be parsing the URLs from previous runs
if len(idx_new)>0:
    idx_new = idx_new[0] + 1 # +1 is to skip the '=====' line
    cat_urls = cat_urls[idx_new:]
else:
    idx_new = 0

print('starting from idx:',idx_new)

already_seen = set()
unique_cat_urls = []
counter = idx_new
for cat_url in cat_urls:
    cat_url_split = cat_url.split(',')
    if cat_url_split[1] not in already_seen:
        unique_cat_urls.append([counter] + cat_url_split)
        already_seen.add(cat_url_split[1])
        counter += 1 # we need that to keep ordering when we pool map

print(len(unique_cat_urls),'unique urls')

# we are not writing the unique indexes as they are equal to the line numbers
with open('./data/links/urls_final.txt', 'a', encoding='utf8') as file:
    for elt in unique_cat_urls:
        file.write(','.join(elt[1:]) + '\n')

# = = get raw HTML of the urls = = 

start_time = time.time()

print(n_cores,'core(s) will be used')

pool = Pool(processes=n_cores)
pool.map(scrape_one_url, unique_cat_urls)
pool.close()
pool.join()

print('= = = done in',round(time.time() - start_time,2),'sec(s)= = =')
