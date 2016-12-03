1st
map
emit [word,doc_id] 

reduce to 1 reducer
emit dict[word]  
array[word_indx,array[doc_id]]




2nd map
emit [docid,word_index]
reduce [docid, array[word  _index]]  
//目前测试只搞出一个reducer？
1. 目前k-shingle的结果很奇怪,很多stopword去除不掉，单机版很正常
