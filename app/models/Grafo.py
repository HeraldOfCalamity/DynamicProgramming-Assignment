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
        print(node)
        G.add_node(nodes[node]["name"])


def fill_edges(nodes):
    for i in nodes:
        sig = nodes[i]["sig"]
        we = nodes[i]["weights"]
        name = nodes[i]["name"]
        if isinstance(sig, list) and isinstance(we, list):
            for s, w in zip(sig, we):
                # Convertir s a cadena para que coincida con los nodos
                G.add_edge(name, str(s), weight=w)
    # print(G.nodes())
    # print(G.edges())


def find_shortest_path(source, target):
    print(G.nodes())
    return nx.shortest_path(G, source=source, target=target, weight="weight")


def find_shortest_distance(source, target):
    print(G.nodes())
    return nx.shortest_path_length(G, source=source, target=target, weight="weight")


def saveGraph(naem):
    for u, v, weight in G.edges(data='weight', default=1):
        print(f"Arista: {u} - {v}, Peso: {weight}")

    random.seed(42)
    pos = nx.random_layout(G, seed=random.randint(1, 1000))
    elarge = [(u, v) for (u, v, d) in G.edges(
        data=True) if int(d["weight"]) > 5]
    esmall = [(u, v) for (u, v, d) in G.edges(
        data=True) if int(d["weight"]) <= 5]

    nx.draw_networkx_edges(G, pos, edgelist=elarge,
                           width=6, edge_color='black', node_size=500)
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6,
                           edge_color='black', style='dashed', node_size=500)

    # print(G.nodes)

    nx.draw_networkx_labels(G, pos, font_size=20,
                            font_family="sans-serif", font_color="white")
    nx.draw_networkx_nodes(G, pos, node_color=["blue"], node_size=500)
# edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f'./app/static/images/{naem}')


def saveGraphr(naem, resp):
    for u, v, weight in G.edges(data='weight', default=1):
        print(f"Arista: {u} - {v}, Peso: {weight}")

    random.seed(42)
    pos = nx.random_layout(G, seed=random.randint(1, 1000))

    # Filtrar los nodos que están en resp
    nodes_to_color = [node_id for node_id in resp]

    # Crear un diccionario de colores para los nodos
    node_colors = [
        'blue' if node_id in nodes_to_color else 'gray' for node_id in G.nodes()]

    # Filtrar las conexiones que pertenecen a los nodos en resp
    edges_to_color = [(u, v) for (u, v) in G.edges()
                      if u in nodes_to_color and v in nodes_to_color]

    elarge = [(u, v) for (u, v, d) in G.edges(
        data=True) if int(d["weight"]) > 5]
    esmall = [(u, v) for (u, v, d) in G.edges(
        data=True) if int(d["weight"]) <= 5]

    # Crear una lista de conexiones a colorear de rojo
    red_edges = [(u, v) for (u, v) in G.edges() if (u, v)
                 in edges_to_color or (v, u) in edges_to_color]

    # Dibujar conexiones grandes en negro
    nx.draw_networkx_edges(G, pos, edgelist=elarge,
                           width=6, edge_color='black', node_size=500)
    # Dibujar conexiones pequeñas en negro
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6,
                           edge_color='black', style='dashed', node_size=500)

    nx.draw_networkx_labels(G, pos, font_size=20,
                            font_family="sans-serif", font_color="white")

    # Dibujar nodos con colores correspondientes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)

    # Dibujar conexiones de resp en rojo
    nx.draw_networkx_edges(G, pos, edgelist=red_edges,
                           width=6, edge_color='red')

    # Etiquetas de peso en las conexiones
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f'./app/static/images/{naem}')


def tpyeof():
    for u, v, weight in G.edges(data='weight', default=1):
        print(f"Arista: {type(u)} - {type(v)}, Peso: {type(weight)}")
