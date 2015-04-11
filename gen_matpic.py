# -*- coding: utf-8 -*-

import networkx
import argparse
import numpy
import json

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

    graph = json_graph.node_link_graph({"nodes":nodes, "links":links}, directed=False, multigraph=False)

    graphs = list(networkx.connected_component_subgraphs(graph))

    for graph in graphs:

        if 0 in graph.nodes():

            nodes = [node["name"] for node in nodes if nodes.index(node) in graph.nodes()]

            labels = {}

            for index, node in zip(graph.nodes(), nodes):

                labels[index] = node

            graph = networkx.relabel_nodes(graph, labels)

            data = json_graph.node_link_data(graph)

            with open("/var/www/html/msif/" + name + ".json", 'w') as target:

                json.dump(data, target)

            matrix =  networkx.to_numpy_matrix(graph)

            return matrix, nodes

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("path", help="")

    argument_parser.add_argument("name", help="")

    args = argument_parser.parse_args()

    path = args.path

    name = args.name

    foo(path, name)

