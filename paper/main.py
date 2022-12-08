import sys

import graph_tools
import networkx as nx
import csv
import matplotlib as mpl
import multiprocessing
import os
import igraph as ig
import random
import json
import statistics

def csv_to_network(csv_filename):

    network = nx.Graph()

    with open(csv_filename, 'r', newline='') as csv_file:

        lines = csv.reader(csv_file)

        for src, dest in lines:

            network.add_edge(src, dest)

    return network

def get_results(csv_filename, result_name_to_filename):

    network = csv_to_network(csv_filename)

    n = len(list(result_name_to_filename.keys()))
    ps = [None] * n
    i = 0

    for result_name, filename in result_name_to_filename.items():

        f = None

        if result_name == "rich_club_coefficients":
            f = get_rich_club_coefficients

        elif result_name == "degree_frequencies":
            f = get_degree_frequencies

        elif result_name == "vote_ranks":
            f = get_vote_ranks

        elif result_name == "closeness_centralities":
            f = get_closeness_centralities

        elif result_name == "betweenness_centralities":
            f = get_betweenness_centralities

        elif result_name == "density":
            f = get_density

        elif result_name == "articulation_points":
            f = get_articulation_points

        elif result_name == "diameters":
            f = get_diameters

        elif result_name == "hubs":
            f = get_hubs

        else:
            f = None

        p = multiprocessing.Process(target=f, args=(network, filename))
        ps[i] = p
        i += 1
        p.start()

    for i in range(0, n):
        p = ps[i]
        p.join()

def get_rich_club_coefficients(network, filename):

    rich_club_coefficients = nx.rich_club_coefficient(network, False)
    out_json_file = open(filename, "w")
    json.dump(rich_club_coefficients, out_json_file)

def get_degree_frequencies(network, filename):

    degrees = list(nx.degree(network))
    degree_to_frequency = {}

    for _, degree in degrees:

        if degree_to_frequency.get(degree) is None:
            degree_to_frequency[degree] = 1

        else:
            degree_to_frequency[degree] += 1

    out_json_file = open(filename, "w")
    json.dump(degree_to_frequency, out_json_file)

def get_vote_ranks(network, filename):

    vote_ranks = nx.voterank(network)
    out_json_file = open(filename, "w")
    json.dump(vote_ranks, out_json_file)

def get_closeness_centralities(network, filename):
    closeness_centralities = nx.closeness_centrality(network)
    out_json_file = open(filename, "w")
    json.dump(closeness_centralities, out_json_file)

def get_betweenness_centralities(network, filename):
    betweenness_centralities = nx.betweenness_centrality(network)
    out_json_file = open(filename, "w")
    json.dump(betweenness_centralities, out_json_file)

def get_density(network, filename):
    density = nx.density(network)
    out_json_file = open(filename, "w")
    json.dump(density, out_json_file)

def get_articulation_points(network, filename):
    articulation_points = list(nx.articulation_points(network))
    out_json_file = open(filename, "w")
    json.dump(articulation_points, out_json_file)

def find_diameter_from_src(network, src):
    dest = list(nx.bfs_edges(network, src))[-1][1]
    diameter = nx.shortest_path_length(network, src, dest)
    return diameter

def get_diameters(network, filename):

    nodes = list(nx.nodes(network))
    n = len(nodes)
    node_to_diameter = {}

    for i in range(0, n):
        node = str(nodes[i])
        diameter = find_diameter_from_src(network, node)
        node_to_diameter[node] = diameter

    out_json_file = open(filename, "w")
    json.dump(node_to_diameter, out_json_file)

def get_hubs(network, filename):

    results = nx.hits(network)
    hubs = results[0]
    out_json_file = open(filename, "w")
    json.dump(hubs, out_json_file)

def display_results(csv_filename, result_name_to_filename):

    network = csv_to_network(csv_filename)

    n = len(list(result_name_to_filename.keys()))
    ps = [None] * n
    i = 0

    for result_name, filename in result_name_to_filename.items():

        f = None

        if result_name == "rich_club_coefficients":
            f = display_rich_club_coefficients

        elif result_name == "degree_frequencies":
            f = display_degree_frequencies

        elif result_name == "vote_ranks":
            f = display_vote_ranks

        elif result_name == "density":
            f = display_density

        elif result_name == "articulation_points":
            f = display_articulation_points

        elif result_name == "diameters":
            f = display_diameters

        elif result_name == "centralities":
            f = display_centralities

        else:
            continue

        p = multiprocessing.Process(target=f, args=(network, filename))

        ps[i] = p
        i += 1
        p.start()

    for i in range(0, n):
        p = ps[i]
        p.join()


def display_rich_club_coefficients(network, filename):

    in_json_file = open(filename, "r")
    rich_club_coefficients = json.load(in_json_file)
    degrees = list(rich_club_coefficients.keys())
    n_degrees = len(degrees)
    for i in range(0, n_degrees):
        degrees[i] = int(degrees[i])
    degrees.sort()
    coefficients = [0] * n_degrees
    for i in range(0, n_degrees):
        degree = degrees[i]
        coefficient = rich_club_coefficients[str(degree)]
        coefficients[i] = coefficient

    fig, ax = mpl.pyplot.subplots(dpi=150)
    ax.plot(degrees, coefficients, "black")

    ax.set_xticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500])
    ax.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    mpl.pyplot.xlabel("Degree")
    mpl.pyplot.ylabel("Rich Club Coefficient")

    mpl.pyplot.title("Degree vs. Rich Club Coefficient")

    mpl.pyplot.grid(color='black', linestyle="dotted", linewidth=1)

    mpl.pyplot.xticks(rotation=45)

    mpl.pyplot.tight_layout()
    out_filename = filename.split(".")[0] + ".png"
    mpl.pyplot.savefig(out_filename)

def display_degree_frequencies(network, filename):

    in_json_file = open(filename, "r")
    degree_to_frequencies = json.load(in_json_file)
    degrees = list(degree_to_frequencies.keys())
    degrees_len = len(degrees)
    for i in range(0, degrees_len):
        degrees[i] = int(degrees[i])

    degrees.sort()
    frequencies = [0] * degrees_len

    for i in range(0, degrees_len):
        degree = degrees[i]
        frequency = degree_to_frequencies[str(degree)]
        frequencies[i] = frequency

    all_degrees = list(dict(nx.degree(network)).values())

    average_degree = sum(all_degrees) / len(all_degrees)
    max_degree = max(all_degrees)
    min_degree = min(all_degrees)
    sd = statistics.stdev(all_degrees)
    median = statistics.median(all_degrees)

    print(median)
    print(sd)
    print(min_degree)
    print(max_degree)
    print(average_degree)
    print(degrees_len)

    n_degrees = 101
    degrees = [int(degrees[i]) for i in range(1, n_degrees)]
    frequencies = [frequencies[i] for i in range(1, n_degrees)]

    fig, ax = mpl.pyplot.subplots(dpi=150)

    ax.plot(degrees, frequencies, color="black")

    ax.set_xticks([i * 5 for i in range(0, 21)])
    ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 5500])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    mpl.pyplot.xlabel("Degree")
    mpl.pyplot.ylabel("Degree Frequency")

    mpl.pyplot.title("Degree vs. Degree Frequency Where 0 < Degree < 101")

    mpl.pyplot.grid(color='black', linestyle="dotted", linewidth=1)

    mpl.pyplot.xticks(rotation=45)

    mpl.pyplot.tight_layout()
    out_filename = filename.split(".")[0] + ".png"
    mpl.pyplot.savefig(out_filename)

def display_vote_ranks(network, filename):

    n_degrees = 101
    degrees = dict(nx.degree(network))
    in_json_file = open(filename, "r")
    vote_ranks = json.load(in_json_file)
    ranks = list(range(0, n_degrees))
    degrees = [degrees[vote_ranks[i]] for i in range(0, n_degrees)]

    fig, ax = mpl.pyplot.subplots(dpi=150)

    ax.plot(ranks, degrees, color="black")

    ax.set_xticks([i * 5 for i in range(0, 21)])
    ax.set_yticks([0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    mpl.pyplot.xlabel("Rank")
    mpl.pyplot.ylabel("Degree")

    mpl.pyplot.title("Rank vs. Degree Where 0 ≤ Rank < 101")

    mpl.pyplot.grid(color='black', linestyle="dotted", linewidth=1)

    mpl.pyplot.xticks(rotation=45)

    mpl.pyplot.tight_layout()
    out_filename = filename.split(".")[0] + ".png"
    mpl.pyplot.savefig(out_filename)

def display_density(network, filename):

    return

def display_articulation_points(network, filename):

    in_json_file = open(filename, "r")
    articulation_points = json.load(in_json_file)
    articulation_points_len = len(articulation_points)
    out_filename = filename.split(".")[0] + "_results" + ".json"
    out_json_file = open(out_filename, "w")
    json.dump(articulation_points_len, out_json_file)

def display_diameters(network, filename):

    in_json_file = open(filename, "r")
    diameters_dict = json.load(in_json_file)
    diameters = diameters_dict.values()
    max_diameter = max(diameters)
    min_diameter = min(diameters)
    average_diameter = sum(diameters) / len(diameters)

    result_dict = {
        "min_diameter": min_diameter,
        "max_diameter": max_diameter,
        "average_diameter": average_diameter
    }

    out_filename = filename.split(".")[0] + "_results" + ".json"
    out_json_file = open(out_filename, "w")
    json.dump(result_dict, out_json_file)

def display_centralities(network, filename):

    in_json_file_closeness = open("results/closeness_centralities.json", "r")
    in_json_file_betweenness = open("results/betweenness_centralities.json", "r")

    closeness_centralities = json.load(in_json_file_closeness)
    betweenness_centralities = json.load(in_json_file_betweenness)

    closeness_centrality = [0] * len(closeness_centralities)
    betweenness_centrality = [0] * len(betweenness_centralities)

    for i in range(0, len(closeness_centralities)):
        closeness_centrality[i] = float(closeness_centralities[str(i)])
        betweenness_centrality[i] = float(betweenness_centralities[str(i)])

    fig, ax = mpl.pyplot.subplots(dpi=150)
    ax.scatter(x=closeness_centrality, y=betweenness_centrality, color="black")

    ax.set_xticks([0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55])
    ax.set_yticks([0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27, 0.3])

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    mpl.pyplot.xlabel("Closeness Centrality")
    mpl.pyplot.ylabel("Betweenness Centrality")

    mpl.pyplot.title("Closeness Centrality vs. Betweenness Centrality")

    mpl.pyplot.grid(color='black', linestyle="dotted", linewidth=1)

    mpl.pyplot.xticks(rotation=45)

    mpl.pyplot.tight_layout()
    out_filename = "centralities.png"
    mpl.pyplot.savefig(out_filename)


def main():

    argv = sys.argv

    if len(argv) < 4:
        return

    get_or_display_results = argv[1]
    csv_filename = argv[2]
    result_name_to_filename = {}

    for i in range(3, len(argv)):
        argv_string = argv[i]
        result_name, filename = argv_string.split(":")
        result_name_to_filename[result_name] = filename

    if get_or_display_results == "get":
        get_results(csv_filename, result_name_to_filename)

    else:
        display_results(csv_filename, result_name_to_filename)


if __name__ == '__main__':
    display_degree_frequencies(csv_to_network("musae_git_edges.csv"), "results/degree_frequencies.json")