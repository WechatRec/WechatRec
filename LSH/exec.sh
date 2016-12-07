INPUT_PATH=/home/hduser/WechatRec/part.txt

# get dictionary
rm -r -f out
# specify cache dir for jieba and how many tokens in one shingle
hadoop jar $HADOOP_STREAMING -mapper 'mapper.py /home/hduser/WechatRec/cache 2' -reducer reducer.py -input $INPUT_PATH -output out -file stopwords.txt
echo 'finished 1st mr'
cat > pause
# map shingles to index
rm -f dict.txt
cat out/part* >> dict.txt
cat dict.txt | python handle.py
rm -r -f out

# get document vector
rm -r -f out2
hadoop jar $HADOOP_STREAMING -mapper mapper2.py -reducer reducer2.py -input inter -output out2
cat > pause
echo 'finished 2nd mr'
# get document vector with weight
rm -r -f out_lda
hadoop jar $HADOOP_STREAMING -mapper mapper2_w8.py -reducer reducer2.py -input inter -output out_lda
cat > pause
echo 'finished 3rd mr'
# minhash and lsh
num_shingle=`wc -l inter | cut -f1 -d' '`
# config
printf "prime=primes.txt\nseed=599\nsig_size=200\nband_size=4\nnum_shingle=$num_shingle" > config
rm -r -f out3
hadoop jar $HADOOP_STREAMING -file lsh_mapper.py -mapper 'lsh_mapper.py config $num_shingle' -reducer lsh_reducer.py -input out2/part* -output out3
cat > pause
echo 'finished 4th mr'
# get candidates for each article
rm -r -f out4
hadoop jar $HADOOP_STREAMING -mapper identity.py -reducer candidate.py -input out3/part* -output out4

# get clusters of docs
rm -f adjacency
cat out4/part* >> adjacency
python cc.py adjacency
