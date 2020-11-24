path_to_summaries = './summarization_dataset/summaries/'

# = = = compute length = = = 

for (a_t in c('abstracts','titles')){
  
  cat('* * * * * ',a_t,'* * * * * \n')
  
  my_files = list.files(paste0(path_to_summaries,a_t))
  
  tmp = lapply(my_files,function(x) {
    to_return = readLines(paste0(path_to_summaries,a_t,'/',x))
    Encoding(to_return) = 'UTF-8'
    to_return
  })
  
  names(tmp) = my_files
  
  for (my_file in my_files){
    cat('= = =',my_file,'= = =\n')
    cat(round(mean(unlist(lapply(tmp[[my_file]], function(x) length(unlist(strsplit(x,split=' ')))))),2),'\n')
  }
  
}

# = = = duplicate words = = =

n_top_words = 500

for (a_t in c('abstracts','titles')){
  
  cat('* * * * * ',a_t,'* * * * * \n')
  
  my_files = list.files(paste0(path_to_summaries,a_t))
  
  my_files = setdiff(my_files,'source_documents.txt')
  
  tmp = lapply(my_files,function(x) {
    to_return = readLines(paste0(path_to_summaries,a_t,'/',x))
    Encoding(to_return) = 'UTF-8'
    to_return
  })
    
  names(tmp) = my_files
  
  tmp = lapply(tmp,function(x) strsplit(tolower(gsub('[[:punct:] ]+',' ',x)),split=' '))
  
  all_words = as.character(unlist(tmp))
  
  word_freqs = sort(table(all_words),decreasing=TRUE)
  most_freq_words = names(head(word_freqs,n_top_words))

  # % of summs with at least one rep of non top 500 words
  for (my_file in my_files){
    
    perc_rep = round(100*length(which(unlist(lapply(tmp[[my_file]],function(x) {
      to_test = table(x)
      idx_remove = which(names(to_test)%in%most_freq_words)
      if (length(idx_remove)>0){
        to_test = to_test[-idx_remove]
      }
      any(to_test>1) # is there at least one repeated word?
    }))))/length(tmp[[my_file]]),2)
    
    cat('= = =',my_file,'= = =\n')
    cat(perc_rep,'\n')
    
  }
  
}






