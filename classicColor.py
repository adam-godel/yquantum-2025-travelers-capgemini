import networkx as nx
import matplotlib.pyplot as plt
import gcol

graph = {
    'A': {'B': 1, 'C': 1},
    'B': {'A': 1, 'D': 1, 'E': 1},
    'C': {'A': 1, 'F': 1},
    'D': {'B': 1, 'G': 1},
    'E': {'B': 1, 'F': 1, 'H': 1},
    'F': {'C': 1, 'E': 1},
    'G': {'D': 1, 'H': 1},
    'H': {'E': 1, 'G': 1}
}


G = nx.Graph(graph)
c = gcol.node_coloring(G, opt_alg=1)
print("Here is a node coloring of graph G:", c)
nx.draw_networkx(G,
                 pos=nx.spring_layout(G, seed=3),
                 node_color=gcol.get_node_colors(G, c, gcol.colorful),
                 with_labels=False,
                 node_size=80)
plt.show()