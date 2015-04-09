# -*- coding: utf-8 -*-

import networkx
import argparse
import numpy
import json
import os

import matplotlib.pyplot as plt

from networkx.readwrite import json_graph

def foo(path, name):

    with open(path) as source:

        data = json.load(source)

    nodes = data["nodes"]
    links = data["links"]

    for link in links[:]:

        if {"source":link["target"], "target":link["source"]} not in links:

            links.remove(link)

    data = {"nodes":nodes, "links":links }

    graph = json_graph.node_link_graph(data, directed=False, multigraph=False)

    graphs = list(networkx.connected_component_subgraphs(graph))

#    numpy.set_printoptions(threshold="nan")

    for graph in graphs:

        if 0 in graph.nodes():

            nodes = [node["name"] for node in nodes if nodes.index(node) in graph.nodes()]

            labels = {}

            for index, node in zip(graph.nodes(), nodes):

                labels[index] = node

            graph = networkx.relabel_nodes(graph, labels, copy=False)

            data = json_graph.node_link_data(graph)

            with open(name + ".json", 'w') as target:

                json.dump(data, target)

            matrix =  networkx.to_numpy_matrix(graph)

            numpy.savetxt(name + ".matrix", matrix, delimiter=',')

            return os.path.abspath(name + ".matrix"), nodes

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("path", help="")

    argument_parser.add_argument("name", help="")

    args = argument_parser.parse_args()

    path = args.path

    name = args.name

    foo(path, name)

