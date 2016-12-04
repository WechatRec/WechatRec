#!/usr/bin/env python

import sys

def output(cluster):
    for e in cluster:
        for candidate in cluster:
            if candidate != e:
                print '%s\t%s' % (e, candidate)

prev_band_id, prev_band_hash = None, None
cluster = []

for line in sys.stdin:
    band_id_hash, doc_id = line.strip().split("\t", 1)
    band_id, band_hash = band_id_hash.split(',')

    if prev_band_id is None and prev_band_hash is None:
        prev_band_id, prev_band_hash = band_id, band_hash

    if prev_band_id is band_id:
        if prev_band_hash == band_hash:
            cluster.append(doc_id)
        else:
            output(cluster)
            cluster = [doc_id]
    else:
        output(cluster)
        cluster = [doc_id]
    prev_band_id, prev_band_hash = band_id, band_hash
if len(cluster) > 0:
    output(cluster)
