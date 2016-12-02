1st
map
emit <word,doc_id>
reduce to 1 reducer
emit dict<word>  array<word_indx,array<doc_id>>

//todo
2nd map
emit <docid,word_index>
reduce <docid, array<word_index>>


1. 目前k-shingle的结果很奇怪,很多stopword去除不掉
2. 不知道为什么只有一个reducer， 似乎map中的key没有用？？？？第二步mr还需要调试
