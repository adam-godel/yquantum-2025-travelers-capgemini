import json
import pandas as pd
import math

import networkx as nx
import matplotlib.pyplot as plt
import gcol

# Load your JSON file
with open(r"\Users\sirer\OneDrive\Desktop\cdProjects\Quantum\yquantum-2025-travelers-capgemini\LACountyFireHazardLevel.json") as file:
    full_data = json.load(file)
print("success")

# Step 1: Process the data to get centroids
centroids = {}

for idx, feature in enumerate(full_data['features']):
    attributes = feature.get('attributes', {})
    geometry = feature.get('geometry', {})

    if 'rings' in geometry and geometry['rings']:
        points = geometry['rings'][0]
        num_points = len(points)

        avg_lon = sum(p[0] for p in points) / num_points
        avg_lat = sum(p[1] for p in points) / num_points
        hazard_level = attributes.get('HAZ_CLASS', 'Unknown')

        centroids[idx + 1] = (hazard_level, avg_lat, avg_lon)

# Step 2: Compute Euclidean distances between all pairs
def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

distance_matrix = {}

for id1, attributes1 in centroids.items():
    hazard_level1 = attributes1[0]
    coord1 = (attributes1[1], attributes1[2])
    if(hazard_level1 not in distance_matrix.keys()):
        distance_matrix[hazard_level1] = {}
    distance_matrix[hazard_level1][id1] = {}
    for id2, attributes2 in centroids.items():
        hazard_level2 = attributes2[0]
        coord2 = (attributes2[1], attributes2[2])
        if id1 != id2 and hazard_level1 == hazard_level2:
            distance_matrix[hazard_level1][id1][id2] = euclidean_distance(coord1, coord2)

# Result: distance_matrix is your dictionary of dictionaries!


epselon = 0.01

moderateGraph = {}
for id1 in distance_matrix["Moderate"].keys():
    for id2 in distance_matrix["Moderate"][id1].keys():
        dist = distance_matrix["Moderate"][id1][id2]
        if(dist < epselon):
            if(id1 not in moderateGraph.keys()):
                moderateGraph[id1] = {}
            if(id2 not in moderateGraph[id1].keys()):
                moderateGraph[id1][id2] = 1
            


highGraph = {}
for id1 in distance_matrix["High"].keys():
    for id2 in distance_matrix["High"][id1].keys():
        dist = distance_matrix["High"][id1][id2]
        if(dist < epselon):
            if(id1 not in highGraph.keys()):
                highGraph[id1] = {}
            if(id2 not in highGraph[id1].keys()):
                highGraph[id1][id2] = 1



veryHighGraph = {}
for id1 in distance_matrix["Very High"].keys():
    for id2 in distance_matrix["Very High"][id1].keys():
        dist = distance_matrix["Very High"][id1][id2]
        if(dist < epselon):
            if(id1 not in veryHighGraph.keys()):
                veryHighGraph[id1] = {}
            if(id2 not in veryHighGraph[id1].keys()):
                veryHighGraph[id1][id2] = 1


print("moderate neighbors:", len(moderateGraph.keys()))
print("high neighbors:", len(highGraph.keys()))
print("very high neighbors:", len(veryHighGraph.keys()))

G = nx.Graph(moderateGraph)
c = gcol.node_coloring(G, opt_alg=1)

print("Here is a node coloring of graph G:", c)
nx.draw_networkx(G,
                 pos=nx.spring_layout(G, seed=3),
                 node_color=gcol.get_node_colors(G, c, gcol.colorful),
                 with_labels=False,
                 node_size=80)
plt.show()
