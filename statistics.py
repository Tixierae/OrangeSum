import os
import re
import json
import numpy as np
import matplotlib.pyplot as plt

path_to_docs = './data/docs/parsed/'

docnames = os.listdir(path_to_docs)

my_keys = ['title','heading','article']
lens = dict(zip(my_keys,[[],[],[]]))

nmax = 4 # greatest n-gram order considered in 'compute_overlap.py'

for counter,docname in enumerate(docnames):
    
    with open(path_to_docs + docname, 'r', encoding='utf8') as file:
        doc = json.load(file)
            
    for key in my_keys:
        lens[key].append(len(doc[key].split()))
    
    if counter % round(len(docnames)/10) == 0:
        print(counter)

for key in my_keys:
    
    print('= = = size (in nb of words) of',key,'= = =')
    print('min: %s, max: %s, average: %s, median: %s' % (min(lens[key]),max(lens[key]),round(np.mean(lens[key]),2),np.median(lens[key])))
    
    print('nb of docs with empty',key,':',len([elt for elt in lens[key] if elt == 0]))
    
    print('nb of docs with <= 5 words',key,':',len([elt for elt in lens[key] if elt <= 5]))
    
    if key == 'article':
        print('nb of docs with article <= 20 words:',len([elt for elt in lens[key] if elt <= 20]))
    
    plt.figure()
    plt.hist(lens[key],density=False)
    plt.grid(True)
    plt.xlabel('Nb of words')
    plt.ylabel('Counts')
    plt.title('Size (in nb of words) of ' + key)
    plt.savefig('./plots/' + 'size_distr_' + key + '.pdf')

with open('./data/overlap/overlaps.json', 'r', encoding='utf8') as file:
    overlaps = json.load(file)

for key in ['t','h','t+h']:
    
    print('= = = = percentage of novel ngrams in:',key,'= = = =')
    
    for n in range(1,nmax + 1):
        print('* * * * order:',n,'* * * *')
        print(round(np.mean([v[key][str(n)] for k,v in overlaps.items() if not v[key][str(n)] == 'NA']),1))

for perc in [10,20,30,40,50,60]:
    print('= = = = nb of title+heading summaries with at least:',perc,'% new unigrams = = = =')
    print(len([k for k,v in overlaps.items() if v['t+h']['1'] >= perc]))

