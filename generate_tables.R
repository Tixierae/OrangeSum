library(jsonlite)

path_to_examples = './summarization_dataset/random_examples.json'

exs = fromJSON(path_to_examples)

reduce_threshold = 2000

for (ex in exs){
  
  for_cat = paste0("\\begin{table} \n \\centering \n \\begin{tabular}{|cr|L|} \n \\hline \n & Document &",ifelse(nchar(ex[['document']])>reduce_threshold+1000,"\\baselineskip=7pt {\\scriptsize ",ifelse(nchar(ex[['document']])>reduce_threshold,"\\baselineskip=8pt {\\small ",'')),ex[['document']],ifelse(nchar(ex[['document']])>reduce_threshold,'}','')," \\\\ \n \\hline \n \\hline \n \\multirow{5}{*}[-3.5em]{\\rotatebox[origin=c]{90}{\\textsc{Abstract}}} & Gold & ",ex[['summaries']][['abstract']][['gold']]," \\\\ \n & mBART & ",ex[['summaries']][['abstract']][['mbart']], "\\\\ \n & mBARThez &", ex[['summaries']][['abstract']][['mbarthez']]," \\\\ \n & BARThez &", ex[['summaries']][['abstract']][['barthez']], "\\\\ \n & C2C &", ex[['summaries']][['abstract']][['camembert2camembert']],"\\\\ \n \\hline \n \\hline \n \\multirow{5}{*}[-2em]{\\rotatebox[origin=c]{90}{\\textsc{Title}}} & Gold &", ex[['summaries']][['title']][['gold']]," \\\\ \n & mBART &", ex[['summaries']][['title']][['mbart']], "\\\\ \n & mBARThez &", ex[['summaries']][['title']][['mbarthez']], "\\\\ \n & BARThez &", ex[['summaries']][['title']][['barthez']], "\\\\ \n & C2C & ",ex[['summaries']][['title']][['camembert2camembert']],"\\\\ \n \\hline \n \\end{tabular} \n \\caption{C2C stands for CamemBERT2CamemBERT} \n \\label{table2} \n \\end{table}")
  
  for_cat = gsub('%','\\%',for_cat,fixed=TRUE)
  
  cat(for_cat)
  
  cat('\n \n \n')
  
}
