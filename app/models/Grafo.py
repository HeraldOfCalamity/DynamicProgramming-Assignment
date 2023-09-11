import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import random
matplotlib.use('Agg')


def new_graph():
    global G

    G = nx.DiGraph()


def fillNodes(nodes):
    for node in nodes:
        G.add_node(node)


def fill_edges(nodes):
    for i in nodes:
        sig = nodes[i]["sig"]
        we = nodes[i]["weights"]
        name = nodes[i]["name"]
        if isinstance(sig, list) and isinstance(we, list):
            for s, w in zip(sig, we):
                # Convertir s a cadena para que coincida con los nodos
                G.add_edge(name, str(s), weight=w)
        else:
            G.add_edge(name, str(sig), weight=we)


def find_shortest_path(source, target):
    return nx.shortest_path(G, source=source, target=target, weight="weight")


def find_shortest_distance(source, target):
    return nx.shortest_path_length(G, source=source, target=target, weight="weight")


def saveGraph(naem):
    for u, v, weight in G.edges(data='weight', default=1):
        print(f"Arista: {u} - {v}, Peso: {weight}")

    random.seed(42)
    pos = nx.random_layout(G, seed=random.randint(1, 1000))
    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 5]

    nx.draw_networkx_edges(G, pos, edgelist=elarge,
                           width=6, edge_color='black', node_size=500)
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6,
                           edge_color='black', style='dashed', node_size=500)

    nx.draw_networkx_labels(G, pos, font_size=20,
                            font_family="sans-serif", font_color="white")
    nx.draw_networkx_nodes(G, pos, node_color=["blue"], node_size=500)
# edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f'./app/temp/{naem}')
