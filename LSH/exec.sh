INPUT_PATH=input

# get dictionary
rm -r -f out
hadoop jar $HADOOP_STREAMING -mapper mapper.py -reducer reducer.py -input $INPUT_PATH -output out -file stopwords.txt

# map shingles to index
rm -f dict.txt
cat out/part* >> dict.txt
cat dict.txt | python handle.py
rm -r -f out

# get document vector
rm -r -f out2
hadoop jar $HADOOP_STREAMING -mapper mapper2.py -reducer reducer2.py -input inter -output out2

# minhash and lsh
num_shingle=`wc -l inter | cut -f1 -d' '`
rm -r -f out3
hadoop jar $HADOOP_STREAMING -file lsh_mapper.py -mapper 'lsh_mapper.py config $num_shingle' -reducer lsh_reducer.py -input out2/part* -output out3

# get candidates for each article
rm -r -f out4
hadoop jar $HADOOP_STREAMING -mapper identity.py -reducer candidate.py -input out3/part* -output out4
