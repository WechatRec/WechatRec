#!/bin/bash

idx=200
max_idx=`wc -l ../data/id/id.txt | cut -f1 -d' '`
size=20

while [ "$idx" -lt "$max_idx" ]; do
echo 'offset from '$idx
python get_article.py ../data/id/id.txt $idx $size
idx=$((idx+size))
echo 'current batch finished'
sleep 60
echo 'next batch'
done
