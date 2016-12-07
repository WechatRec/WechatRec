INPUT_PATH=/home/hduser/WechatRec/clean_input/*
start_time=`date +%s`

# Step 1  --------------------
# get dictionary
rm -r -f out
# specify cache dir for jieba and how many tokens in one shingle
hadoop jar $HADOOP_STREAMING -mapper 'mapper.py /home/hduser/WechatRec/cache 1' -reducer reducer.py -input $INPUT_PATH -output out -file stopwords.txt

echo 'finished 1st mr'
end_time=`date +%s`
echo "first mr: $((end_time - start_time))" > pause
cat >> pause

# map shingles to index
rm -f dict.txt
cat out/part* >> dict.txt
cat dict.txt | python handle.py

# Step 2  --------------------
# get document vector
rm -r -f out2
start_time=`date +%s`
hadoop jar $HADOOP_STREAMING -mapper mapper2.py -reducer reducer2.py -input inter -output out2

echo 'finished 2nd mr'
end_time=`date +%s`
echo "second mr: $((end_time - start_time))" >> pause
cat >> pause

# get document vector with weight
rm -r -f out_lda
start_time=`date +%s`
hadoop jar $HADOOP_STREAMING -mapper mapper2_w8.py -reducer reducer2.py -input inter -output out_lda

echo 'finished 3rd mr'
end_time=`date +%s`
echo "third mr: $((end_time - start_time))" >> pause
cat >> pause

# Step 3  --------------------
# minhash and lsh
num_shingle=`wc -l inter | cut -f1 -d' '`
# config
printf "prime=primes.txt\nseed=599\nsig_size=200\nband_size=4\nnum_shingle=$num_shingle" > config
rm -r -f out3
start_time=`date +%s`
hadoop jar $HADOOP_STREAMING -file lsh_mapper.py -mapper 'lsh_mapper.py config $num_shingle' -reducer lsh_reducer.py -input out2/part* -output out3

echo 'finished 4th mr'
end_time=`date +%s`
echo "4th mr: $((end_time - start_time))" >> pause
cat >> pause

# Step 4  --------------------
# get candidates for each article
rm -r -f out4
start_time=`date +%s`
hadoop jar $HADOOP_STREAMING -mapper identity.py -reducer candidate.py -input out3/part* -output out4
end_time=`date +%s`
echo "5th mr: $((end_time - start_time))" >> pause

# get clusters of docs
rm -f adjacency
cat out4/part* >> adjacency
python cc.py adjacency
