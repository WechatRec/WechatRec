#!/usr/bin/env python

"""
-- config file --
@param prime: string
    file path to precomputed primes
@param seed: int
    seed to generate random number, make sure to have same hash functions in distributed env
@param num_shingle: int
    number of distinct shingles
@param sig_size: int
    number of hash functions to use in min-hash
@param band_size: int
    number of rows per band
@param dict: string
    file path to dictionary of tokens

-- config example --
prime=primes.txt
seed=599
num_shingle=100000
sig_size=200
band_size=5
dict=dict.txt
"""

import sys
from random import randrange
import random
from bisect import bisect_left
import time

def next_prime(num): # get the smallest prime no smaller than than num
    with open(prime_file, 'r') as f:
        primes = map(lambda e: int(e), f.read().strip().split(', '))
    high = len(primes)
    pos = bisect_left(primes, num, 0, high)
    prime = num
    if pos == high:
        prime = 4294967311 # if num > 10**7, use a very large prime
    else:
        prime = primes[pos] # next prime of num
    return prime

# @param1: int - number of coefficients, @param2: int - number of shingles
def getRandomCoeffs(k, num_shingle): # generate k different coefficients < num_shingle
    assert k < num_shingle # k must be smaller
    randList = []
    while len(randList) < k:
        rand = random.randint(0, num_shingle - 1)
        if rand not in randList:
            randList.append(rand)
    return randList

# @param1: int - number of signatures, @param2: int - number of shingles, @param3: [shingleId] - sparse vector representation of a document
def minHash(sig_size, num_shingle, doc):
    # get hash function coefficients
    vecA = getRandomCoeffs(sig_size, num_shingle)
    vecB = getRandomCoeffs(sig_size, num_shingle)
    prime = next_prime(num_shingle)
    # hash function h(x) = (a * x + b) % next_prime % num_shingle
    signature = []
    for i in xrange(sig_size): # hash sig_size times
        minCode = num_shingle # the minimum row number to be added to signature
        # for each shingle in the document, hash it
        for shingleId in doc:
            hashCode = (vecA[i] * shingleId + vecB[i]) % prime % num_shingle
            if hashCode < minCode:
                minCode = hashCode
        # add the smallest hashCode to signature
        signature.append(minCode)
    return signature

def get_config(config_path):
    config = dict()
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip().split('=', 1)
            config[line[0]] = line[1]
    return config

def get_band(l, n):
    for i in xrange(0, len(l), n):
        yield tuple(l[i:i+n])

def main():
    for line in sys.stdin:
        # print "%d\t%s" % (docid,doc)
        docid, doc = line.strip().split('\t', 1)
        words = map(int, doc.strip().split()) # convert string to array of int list

        signature = minHash(sig_size, num_shingle, words)

        banded = get_band(signature, band_size)
        for band_id, band in enumerate(banded):
            print "%d,%d\t%s" % (band_id, hash(band), docid)

# config
#config = get_config(sys.argv[1])
#num_shingle = int(sys.argv[2])
config = get_config('config')
num_shingle = int(config['num_shingle'])
sig_size = int(config['sig_size'])
band_size = int(config['band_size'])
prime_file = config['prime']

if __name__ == '__main__':
    main()
