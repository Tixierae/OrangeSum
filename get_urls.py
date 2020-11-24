import time 

import urllib.request
from bs4 import BeautifulSoup

import multiprocessing
from multiprocessing import cpu_count, Pool

def get_urls(cat):
    
    if cat == 'auto':
        base_url = 'https://auto.orange.fr/news/?state='
    else:
        base_url = 'https://actu.orange.fr/' + cat + '/?state='
    
    if 'previous_run_urls' in globals():
        all_urls = set(previous_run_urls)
    else: 
        all_urls = set()
    
    n_urls = len(all_urls)
    state_idx = 1
    patience_counter = 1
    
    while True:
        try:
            resp = urllib.request.urlopen(base_url + str(state_idx))
        except:
            continue
        
        soup = BeautifulSoup(resp, my_parser, from_encoding=resp.info().get_param('charset'))
        
        new_urls = set([link['href'] for link in soup.find_all('a', href=True) if len(link['href']) > min_size and 'https' in link['href'] and link['href'] not in all_urls])
        
        all_urls.update(new_urls)
        
        with open('./data/links/urls.txt', 'a', encoding='utf8') as file:
            for url in new_urls:
                file.write(cat + ',' + url + '\n')
        
        # stop as soon as there are no more links to add, with some patience
        if not len(all_urls) > n_urls:
            patience_counter += 1
        
        if patience_counter > patience:
            break
        
        n_urls = len(all_urls)
        state_idx += 1


#  = = = = = parameters = = = = =

my_parser = 'lxml'
societe_subcats = ['sante','environnement','fait-divers','people','culture','media','high-tech','insolite']
cats = ['france','monde','politique','auto'] + ['societe/' + elt for elt in societe_subcats] # stopped using 'finance' because of url extraction issues
min_size = 50 # min nb of chars for a URL to be kept
patience = 5

# optional: load final URLs from previous run
with open('./data/links/urls_final.txt', 'r', encoding='utf8') as file:
    previous_run_urls = file.read().splitlines()

# remove categories, just keep URLs
previous_run_urls = [elt.split(',')[1] for elt in previous_run_urls]

n_cores = cpu_count()

start_time = time.time()   
print(n_cores,'core(s) will be used')
pool = Pool(processes=n_cores)
urls_per_cat = pool.map(get_urls, cats)
pool.close()
pool.join()
urls_per_cat = dict(zip(cats,urls_per_cat))

print('= = = done in',round(time.time() - start_time,2),'sec(s)= = =')
        
    