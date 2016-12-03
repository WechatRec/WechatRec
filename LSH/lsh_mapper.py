#!/usr/bin/python

# lsh_mapper.py

import sys
from random import randrange
import minhash


# config
config = minhash.get_config(sys.argv[1])
sig_size = int(config['sig_size'])
num_shingle = int(config['num_shingle'])
band_size = int(config['band_size'])
doc_file = 'sample_input_file.txt'
 
def get_band(l, n):
    for i in xrange(0, len(l), n):
        yield tuple(l[i:i+n])

def main():
    for docid,doc in enumerate(open(doc_file,'r')):
        # print "%d\t%s" % (docid,doc)

        words = map(int, doc.strip().split()) # convert string to array of int list

        signature = minhash.minHash(sig_size, num_shingle, words)
        
        banded = get_band(signature, band_size)
        for band_id, band in enumerate(banded):
            print "%d\t%d\t%d" % (band_id, hash(band), docid)
  

if __name__ == '__main__':
    main()
