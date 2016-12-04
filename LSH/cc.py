#!/usr/bin/python

# @param1: path to adjacency list

import sys

def load_graph(path):
    graph = dict()
    with open(path, 'r') as f:
        for line in f:
            src, dests = line.strip().split('\t', 1)
            dests = dests.split(',')
            graph[src] = dests
    return graph

def connected_component(graph):
    clusters = []
    while len(graph) > 0:
        queue = set([graph.keys()[0]]) # start bfs from the first node
        cluster = set()
        while len(queue) > 0:
            # get one node from expansion queue
            node = queue.pop()
            if graph.has_key(node): # if the node has not been visited
                # add the node to cluster
                cluster.add(node)
                # expand the node and add children to queue
                queue = queue.union(graph.pop(node))
        clusters.append(' '.join(cluster))
    return clusters

if __name__ == '__main__':
    path = sys.argv[1]
    out = 'doc_cluster.txt'
    graph = load_graph(path)
    clusters = connected_component(graph)
    with open(out, 'w') as f:
        f.write('\n'.join(clusters))
