import csv
import networkx as nx
import multiprocessing


def csv_to_network(csv_filename):

    network = nx.Graph()

    with open(csv_filename, 'r', newline='') as csv_file:

        lines = csv.reader(csv_file)

        for src, dest in lines:

            network.add_edge(src, dest)

    return network


def main():

    csv_filename = "musae_git_edges.csv"
    network = csv_to_network(csv_filename)

    tasks = [

    ]

    n = len(tasks)
    ps = [None] * n

    for i in range(0, n):
        task = tasks[i]
        p = multiprocessing.Process(target=task, args=(network, ))
        ps[i] = p
        p.start()

    for i in range(0, n):
        p = ps[i]
        p.join()

main()