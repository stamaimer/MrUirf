# -*- coding: utf-8 -*-

import networkx
import argparse
import numpy
import json
import matplotlib.pyplot as plt
from networkx.readwrite import json_graph

def foo(data, name):

    nodes = data["nodes"]
    links = data["links"]

    for link in links[:]:

        if {"source":link["target"], "target":link["source"]} not in links:

            links.remove(link)

    graph = json_graph.node_link_graph({"nodes":nodes, "links":links}, directed=False, multigraph=False)

    graphs = list(networkx.connected_component_subgraphs(graph))

    numpy.set_printoptions(threshold='nan')

    for graph in graphs:

        if 0 in graph.nodes():

            nodes = [node["name"] for node in nodes if nodes.index(node) in graph.nodes()]

            for node in nodes:

                print node

            matrix =  networkx.to_numpy_matrix(graph)

            pos = networkx.spring_layout(graph, iterations=200)

            networkx.draw(graph, pos, node_color='#A0CBE2', edge_cmap=plt.cm.Blues, with_labels=True)

            plt.savefig(name)

if __name__ == '__main__':

    argument_parser = argparse.ArgumentParser(description='')

    argument_parser.add_argument('path', help='')

    argument_parser.add_argument('name', help='')

    args = argument_parser.parse_args()

    path = args.path

    name = args.name

    with open(path) as source:

        data = json.load(source)

    foo(data, name)

