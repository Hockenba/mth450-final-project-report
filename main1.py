import sys

import networkx
import networkx as nx
import csv
from matplotlib import pyplot as plt
from multiprocessing import Process
from networkx.algorithms.community import greedy_modularity_communities
import os
import igraph as ig
import random

def network_to_csv(network, csv_filename):

    with open(csv_filename, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        edges = nx.edges(network)
        writer.writerows(edges)

    return


def csv_to_network(csv_filename):

    network = networkx.Graph()

    with open(csv_filename, 'r', newline='') as csv_file:

        lines = csv.reader(csv_file)

        for src, dest in lines:

            network.add_edge(src, dest)

    return network


def display_rich_club_coefficient(network):

    rich_club_coefficients = nx.rich_club_coefficient(network, False)
    degrees = list(rich_club_coefficients.keys())
    coefficients = list(rich_club_coefficients.values())

    fig, ax = plt.subplots(dpi=150)

    ax.plot(degrees, coefficients, "black")

    ax.set_xticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500])
    ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.xlabel("Degree")
    plt.ylabel("Rich Club Coefficient")

    plt.title("Degree vs. Rich Club Coefficient on the GitHub Network")

    plt.grid(color='black', linestyle="dotted", linewidth=1)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    print("Rich Finished")

def display_degree_frequency(network):

    degrees = list(nx.degree(network))
    n = (int(max(degrees, key=lambda t: t[1])[1]) + 1)
    degree_values = [0] * n
    frequencies = [0] * n

    for _, degree in degrees:
        degree_values[degree] = degree
        frequencies[degree] += 1

    degree_values = [degree_values[i] for i in range(1, 101)]
    frequencies = [frequencies[i] for i in range(1, 101)]

    fig, ax = plt.subplots(dpi=150)

    ax.plot(degree_values, frequencies, color="black")

    ax.set_xticks([i * 5 for i in range(0, 21)])
    ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.xlabel("Degree")
    plt.ylabel("Degree Frequency")

    plt.title("Degree vs. Degree Frequency Where 0 < Degree < 101")

    plt.grid(color='black', linestyle="dotted", linewidth=1)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    print("Degree Finished")


def display_hits(network):

    results = nx.hits(network)
    hubs = results[0]
    nodes = list(hubs.keys())
    for i in range(0, len(nodes)):
        nodes[i] = int(nodes[i])
    hub_values = list(hubs.values())

    fig, ax = plt.subplots(dpi=150)

    ax.scatter(nodes, hub_values, color="black")

    ax.set_xticks([0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000])
    ax.set_yticks([0, 0.0004, 0.0008, 0.0012, 0.0016, 0.0020, 0.0024, 0.0028, 0.0032, 0.0036, 0.0040])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.xlabel("Node i")
    plt.ylabel("Hub/Authority Value")

    plt.title("Hub/Authority Value of Each Node in the Sampled GitHub Network")

    plt.grid(color='black', linestyle="dotted", linewidth=1)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    print("Hub Finished")



def display_closeness_centralities(network):

    n = len(list(nx.nodes(network)))
    k = 1000
    sample = random.sample(range(0, n), k)
    sample.sort(key= lambda node_i: nx.degree(network, str(node_i)))
    closeness_centralities = [0.0] * k

    for i in range(0, k):
        node = str(sample[i])
        closeness_centrality = nx.closeness_centrality(network, node)
        closeness_centralities[i] = closeness_centrality

    fig, ax = plt.subplots(dpi=150)

    ax.scatter(sample, closeness_centralities, color="black")

    ax.set_xticks([0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000])
    ax.set_yticks([0, 0.0004, 0.0008, 0.0012, 0.0016, 0.0020, 0.0024, 0.0028, 0.0032, 0.0036, 0.0040])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.xlabel("Node")
    plt.ylabel("Hub Value")

    plt.title("Hub/Authority Value of Each Node in the Sampled GitHub Network")

    plt.grid(color='black', linestyle="dotted", linewidth=1)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    print("Closeness Finished")

def find_diameter_from_src(network, src):
    dest = list(nx.bfs_edges(network, src))[-1][1]
    diameter = nx.shortest_path_length(network, src, dest)
    return diameter

def display_diameter(network):

    n = len(list(nx.nodes(network)))
    k = n
    sample = random.sample(range(0, n), k)
    k_diameters = [0] * k
    i = 0

    for i in range(0, k):
        node = str(sample[i])
        diameter = find_diameter_from_src(network, node)
        k_diameters[i] = diameter
        print(i)

    max_diameter = max(k_diameters)
    average_diameter = sum(k_diameters) / k

    print(f"The max diameter of the network on k={k} is {max_diameter}")
    print(f"The average diameter of the network on k={k} is {average_diameter}")
    print("Diameter Finished")


def display_articulation_points(network):

    articulation_points = list(nx.articulation_points(network))
    n = len(articulation_points)
    articulation_points_degrees = [0] * n
    articulation_points_i = []

    for i in range(0, n):

        articulation_points_i.append(i)
        articulation_point = articulation_points[i]
        degree = nx.degree(network, articulation_point)
        articulation_points_degrees[i] = degree

    fig, ax = plt.subplots(dpi=150)

    ax.scatter(articulation_points_i, articulation_points_degrees, color="black")

    ax.set_xticks([0, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500])
    ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.xlabel("Articulation Point i")
    plt.ylabel("Degree")

    plt.title("Degree of Each Articulation Point in the Network")

    plt.grid(color='black', linestyle="dotted", linewidth=1)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    print("Articulation Points Finished")


def display_connected_components(network):

    connected_components = nx.connected_components(network)
    print(connected_components)
    print("Connected Components Finished")

def display_communities(network):

    print("Communities Finished")

def display_effective_size(network):

    effective_sizes = nx.effective_size(network, "10000")
    print("Effective Size Finished")

def display_density(network):
    density = nx.density(network)
    print(f"The density of the network is {density}")
    print("Density Finished")

def display_center(network):

    center = nx.center(network)
    print("Center Finished")

def display_vote_rank(network):

    k = 1000
    k_influential_nodes = nx.voterank(network, k)
    k_influential_nodes_to_degree = list(nx.degree(network, k_influential_nodes))
    k_influential_nodes_to_degree.sort(key=lambda t: t[1])
    nodes = [0] * k
    degrees = [0] * k
    i = 0
    for node, degree in k_influential_nodes_to_degree:
        nodes[i] = int(node)
        degrees[i] = degree
        i += 1


    fig, ax = plt.subplots(dpi=150)

    ax.plot(degrees, coefficients, "black")

    ax.set_xticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500])
    ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.xlabel("Degree")
    plt.ylabel("Rich Club Coefficient")

    plt.title("Degree vs. Rich Club Coefficient on the GitHub Network")

    plt.grid(color='black', linestyle="dotted", linewidth=1)

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    print("Rich Finished")



def main():

    csv_filename = "musae_git_edges.csv"
    network = csv_to_network(csv_filename)

    """
    
    tasks = [
        #display_vote_rank
        #display_degree_frequency,
        #display_rich_club_coefficient,
        #display_hits,
        display_diameter,
        #display_articulation_points,
        #display_density,
        #display_closeness_centralities,
        #display_effective_size,
    ]

    n = len(tasks)
    ps = [None] * n

    for i in range(0, n):
        task = tasks[i]
        p = Process(target=task, args=(network, ))
        ps[i] = p
        p.start()

    for i in range(0, n):
        p = ps[i]
        p.join()
    """

if __name__ == '__main__':
    main()