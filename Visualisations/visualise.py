import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import seaborn as sns
import csv
import os
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from itertools import cycle

# def create_graph(adj_matrix, config):
#     G = nx.DiGraph()

#     locations_path = config['locations_path']['default'] #'DataNew/Locations/Locations.csv'
#     with open(locations_path, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the header row
#         for row in reader:
#             number, station_name, lat, lon, province = row
#             G.add_node(number, pos=(float(lon), float(lat)), province=province)

#     for i in range(adj_matrix.shape[0]):
#         strongest_influence_indices = np.argsort(adj_matrix[:, i])[-1:]  # Enter number of influential stations
#         for j in strongest_influence_indices:
#             if adj_matrix[j, i] > 0:
#                 G.add_edge(list(G.nodes())[j], list(G.nodes())[i])

#     return G

#official
# def create_graph(adj_matrix, config):
#     G = nx.DiGraph()

#     locations_path = config['locations_path']['default'] #'DataNew/Locations/Locations.csv'
#     with open(locations_path, 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the header row
#         for row in reader:
#             number, station_name, lat, lon, province = row
#             G.add_node(number, pos=(float(lon), float(lat)), province=province)

#     for i in range(adj_matrix.shape[1]):  # Iterate over the columns instead of rows
#         strongest_influence_indices = np.argsort(adj_matrix[i, :])[-3:]  # Enter number of influential stations
#         for j in strongest_influence_indices:
#             if adj_matrix[i, j] > 0:  # Use adj_matrix[i, j] instead of adj_matrix[j, i]
#                 G.add_edge(list(G.nodes())[j], list(G.nodes())[i], weight=adj_matrix[i, j])  # Add the 'weight' attribute

#     return G

def create_graph(adj_matrix, config):

    G = nx.DiGraph()

    locations_path = config['locations_path']['default']
    threshold = 0.0000025  # Introduce this in your config

    with open(locations_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            number, station_name, lat, lon, province = row
            G.add_node(number, pos=(float(lon), float(lat)), province=province)

    # adj_matrix=adj_matrix.T

    for i in range(adj_matrix.shape[1]):  # Iterate over the columns instead of rows
        strongest_influence_indices = np.argsort(adj_matrix[i, :])[-2:]
        for j in strongest_influence_indices:
            weight = adj_matrix[i, j]
            if weight > threshold:  # Check if the weight is greater than the threshold
                G.add_edge(list(G.nodes())[j], list(G.nodes())[i], weight=weight)

    return G


# def plot_map(adj_matrix, config, split):
#     hex_colors = {
#         0: '#E52B50', 1: '#40826D', 2: '#8000FF', 3: '#3F00FF', 4: '#40E0D0', 5: '#008080', 6: '#483C32', 7: '#D2B48C',
#         8: '#00FF7F', 9: '#A7FC00', 10: '#708090', 11: '#C0C0C0', 12: '#FF2400', 13: '#0F52BA', 14: '#92000A', 15: '#FA8072',
#         16: '#E0115F', 17: '#FF007F', 18: '#C71585', 19: '#FF0000', 20: '#E30B5C', 21: '#6A0DAD', 22: '#CC8899', 23: '#003153',
#         24: '#8E4585', 25: '#FFC0CB', 26: '#1C39BB', 27: '#C3CDE6', 28: '#D1E231', 29: '#FFE5B4', 30: '#DA70D6', 31: '#FF4500',
#         32: '#FF6600', 33: '#808000', 34: '#CC7722', 35: '#000080', 36: '#E0B0FF', 37: '#800000', 38: '#FF00AF', 39: '#FF00FF',
#         40: '#BFFF00', 41: '#C8A2C8', 42: '#FFF700', 43: '#B57EDC', 44: '#29AB87', 45: '#00A86B'
#     }

#     for key in hex_colors:
#         hex_colors[key] = '#000000'


#     G = create_graph(adj_matrix, config)
#     node_positions = nx.get_node_attributes(G, 'pos')

#     fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

#     min_lon = min(pos[0] for pos in node_positions.values())
#     max_lon = max(pos[0] for pos in node_positions.values())
#     min_lat = min(pos[1] for pos in node_positions.values())
#     max_lat = max(pos[1] for pos in node_positions.values())

#     width = max_lon - min_lon
#     height = max_lat - min_lat

#     m = Basemap(
#         llcrnrlon=min_lon - 0.1 * width, llcrnrlat=min_lat - 0.1 * height,
#         urcrnrlon=max_lon + 0.1 * width, urcrnrlat=max_lat + 0.1 * height,
#         resolution='i', ax=ax
#     )
#     m.drawcoastlines(linewidth=0.5)
#     m.drawmapboundary(fill_color='lightblue')
#     m.fillcontinents(color='white', lake_color='lightblue')

#     node_degrees = G.out_degree()
#     sorted_nodes = sorted(node_degrees, key=lambda x: x[1], reverse=True)  # Sort nodes by out-degree
#     top_nodes = sorted_nodes[:44]  # Select the top 10 most influential nodes

#     # Add number of outgoing edges as labels for top 10 nodes
#     top_node_labels = {node[0]: f"{node[0]}\n[{node[1]}]" for node in top_nodes}
#     nx.draw_networkx_labels(
#         G, pos=node_positions, labels=top_node_labels,
#         font_color='black', font_size=5, ax=ax
#     )

#     # node_sizes = [100 * degree + 80 for _, degree in top_nodes]
#     node_colors = [hex_colors[int(key)] for key, _ in top_nodes]
#     nx.draw_networkx_nodes(
#         G, pos=node_positions, nodelist=[node[0] for node in top_nodes],
#         node_color='white', edgecolors=node_colors, node_size=200, ax=ax
#     )

#     edge_list = G.out_edges([node[0] for node in top_nodes])
#     edge_colors = [hex_colors[int(key)] for key, _ in edge_list]

#     nx.draw_networkx_edges(
#         G, pos=node_positions, edgelist=G.out_edges([node[0] for node in top_nodes]),
#         edge_color=edge_colors, arrows=True, arrowstyle='->', width=1, ax=ax
#     )

#     ax.set_title("Strongest Dependencies")

#     directory = 'Visualisations/' + config['modelVis']['default']+ '/horizon_' + config['horizonVis']['default'] + '/' + 'geographicVis/'
#     filename = 'geoVis_split_' + split + '.png'

#     # Create the directory if it doesn't exist
#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     filepath = os.path.join(directory, filename)
#     fig.savefig(filepath)

# def plot_map(adj_matrix, config, split):

#     hex_colors = {
#         0: '#E52B50', 1: '#40826D', 2: '#8000FF', 3: '#3F00FF', 4: '#40E0D0', 5: '#008080', 6: '#483C32', 7: '#D2B48C',
#         8: '#00FF7F', 9: '#A7FC00', 10: '#708090', 11: '#C0C0C0', 12: '#FF2400', 13: '#0F52BA', 14: '#92000A', 15: '#FA8072',
#         16: '#E0115F', 17: '#FF007F', 18: '#C71585', 19: '#FF0000', 20: '#E30B5C', 21: '#6A0DAD', 22: '#CC8899', 23: '#003153',
#         24: '#8E4585', 25: '#FFC0CB', 26: '#1C39BB', 27: '#C3CDE6', 28: '#D1E231', 29: '#FFE5B4', 30: '#DA70D6', 31: '#FF4500',
#         32: '#FF6600', 33: '#808000', 34: '#CC7722', 35: '#000080', 36: '#E0B0FF', 37: '#800000', 38: '#FF00AF', 39: '#FF00FF',
#         40: '#BFFF00', 41: '#C8A2C8', 42: '#FFF700', 43: '#B57EDC', 44: '#29AB87', 45: '#00A86B'
#     }

#     for key in hex_colors:
#         hex_colors[key] = '#000000'

#     # Create graph using adjacency matrix
#     G = create_graph(adj_matrix, config)
#     # I'm assuming 'pos' is the key in config for node positions; adjust if not.
#     node_positions = nx.get_node_attributes(G, 'pos')

#     # Setup plot
#     fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

#     min_lon = min(pos[0] for pos in node_positions.values())
#     max_lon = max(pos[0] for pos in node_positions.values())
#     min_lat = min(pos[1] for pos in node_positions.values())
#     max_lat = max(pos[1] for pos in node_positions.values())

#     width = max_lon - min_lon
#     height = max_lat - min_lat

#     m = Basemap(
#         llcrnrlon=min_lon - 0.1 * width, llcrnrlat=min_lat - 0.1 * height,
#         urcrnrlon=max_lon + 0.1 * width, urcrnrlat=max_lat + 0.1 * height,
#         resolution='i', ax=ax
#     )
#     m.drawcoastlines(linewidth=0.5)
#     m.drawmapboundary(fill_color='lightblue')
#     m.fillcontinents(color='white', lake_color='lightblue')

#     node_degrees = G.out_degree()
#     sorted_nodes = sorted(node_degrees, key=lambda x: x[1], reverse=True)
#     top_nodes = sorted_nodes[:20]

#     top_node_labels = {node[0]: f"{node[0]}\n[{node[1]}]" for node in top_nodes}
#     nx.draw_networkx_labels(
#         G, pos=node_positions, labels=top_node_labels,
#         font_color='black', font_size=5, ax=ax
#     )

#     node_colors = [hex_colors[int(key)] for key, _ in top_nodes]
#     nx.draw_networkx_nodes(
#         G, pos=node_positions, nodelist=[node[0] for node in top_nodes],
#         node_color='white', edgecolors=node_colors, node_size=200, ax=ax
#     )

#     # Assuming the edges in your adjacency matrix have weight data
#     edge_weights = nx.get_edge_attributes(G, "weight")
#     normalized_weights = [(w - min(edge_weights.values())) / (max(edge_weights.values()) - min(edge_weights.values()))
#                           for w in edge_weights.values()]

#     colormap = plt.cm.viridis
#     edge_colors = [colormap(w) for w in normalized_weights]

#     # nx.draw_networkx_edges(
#     #     G, pos=node_positions, edgelist=edge_weights.keys(),
#     #     edge_color=edge_colors, arrows=True, arrowstyle='->', width=1, ax=ax
#     # )

#     norm = Normalize(vmin=min(edge_weights.values()), vmax=max(edge_weights.values()))
#     sm = ScalarMappable(cmap=colormap, norm=norm)
#     sm.set_array([])  # You have to set_array due to the way ScalarMappable works

#     # Plot the edges as you did before
#     nx.draw_networkx_edges(
#         G, pos=node_positions, edgelist=edge_weights.keys(),
#         edge_color=edge_colors, arrows=True, arrowstyle='->', width=1, ax=ax
#     )

# # 2. Add the colorbar to the plot
#     cbar = plt.colorbar(sm, orientation='vertical', ax=ax)
#     cbar.set_label('Edge Weight')

#     ax.set_title("Strongest Dependencies")

#     directory = 'Visualisations/' + config['modelVis']['default'] + '/horizon_' + config['horizonVis']['default'] + '/geographicVis/'
#     filename = 'geoVis_split_' + split + '.png'
    
#     # Create the directory if it doesn't exist
#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     filepath = os.path.join(directory, filename)
#     fig.savefig(filepath)

import os
import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

def plot_map(adj_matrix, config, split):
    hex_colors = {
        0: '#E52B50', 1: '#40826D', 2: '#8000FF', 3: '#3F00FF', 4: '#40E0D0', 5: '#008080', 6: '#483C32', 7: '#D2B48C',
        8: '#00FF7F', 9: '#A7FC00', 10: '#708090', 11: '#C0C0C0', 12: '#FF2400', 13: '#0F52BA', 14: '#92000A', 15: '#FA8072',
        16: '#E0115F', 17: '#FF007F', 18: '#C71585', 19: '#FF0000', 20: '#E30B5C', 21: '#6A0DAD', 22: '#CC8899', 23: '#003153',
        24: '#8E4585', 25: '#FFC0CB', 26: '#1C39BB', 27: '#C3CDE6', 28: '#D1E231', 29: '#FFE5B4', 30: '#DA70D6', 31: '#FF4500',
        32: '#FF6600', 33: '#808000', 34: '#CC7722', 35: '#000080', 36: '#E0B0FF', 37: '#800000', 38: '#FF00AF', 39: '#FF00FF',
        40: '#BFFF00', 41: '#C8A2C8', 42: '#FFF700', 43: '#B57EDC', 44: '#29AB87', 45: '#00A86B'
    }
    # I'm assuming you have a reason for the below line, so retaining it as-is.
    for key in hex_colors:
        hex_colors[key] = '#000000'

    # Create graph using adjacency matrix
    G = create_graph(adj_matrix, config)
    node_positions = nx.get_node_attributes(G, 'pos')

    # Setup plot
    fig, ax = plt.subplots(figsize=(8, 8), dpi=300)

    min_lon = min(pos[0] for pos in node_positions.values())
    max_lon = max(pos[0] for pos in node_positions.values())
    min_lat = min(pos[1] for pos in node_positions.values())
    max_lat = max(pos[1] for pos in node_positions.values())

    width = max_lon - min_lon
    height = max_lat - min_lat

    m = Basemap(
        llcrnrlon=min_lon - 0.1 * width, llcrnrlat=min_lat - 0.1 * height,
        urcrnrlon=max_lon + 0.1 * width, urcrnrlat=max_lat + 0.1 * height,
        resolution='i', ax=ax
    )
    m.drawcountries()
    m.drawcoastlines()
    m.drawmapboundary(fill_color='lightblue')
    m.fillcontinents(color='white', lake_color='white')

    # m.drawcoastlines(linewidth=0.5)
    # m.drawmapboundary(fill_color='lightblue')
    # m.fillcontinents(color='white', lake_color='lightblue')
        # m.drawmapboundary(fill_color='lightblue')
    node_degrees = G.out_degree()
    sorted_nodes = sorted(node_degrees, key=lambda x: x[1], reverse=True)
    top_nodes = sorted_nodes[:20]
    drawn_nodes = [node[0] for node in top_nodes]

    # top_node_labels = {node[0]: f"{node[0]}\n[{node[1]}]" for node in top_nodes}
    # nx.draw_networkx_labels(
    #     G, pos=node_positions, labels=top_node_labels,
    #     font_color='black', font_size=5, ax=ax
    # )

    top_node_labels = {node[0]: f"{node[0]}" for node in top_nodes}
    nx.draw_networkx_labels(
        G, pos=node_positions, labels=top_node_labels,
        font_color='black', font_size=9, ax=ax
    )

    node_colors = [hex_colors[int(key)] for key, _ in top_nodes]
    nx.draw_networkx_nodes(
        G, pos=node_positions, nodelist=drawn_nodes,
        node_color='white', edgecolors=node_colors, node_size=200, ax=ax
    )

    edge_weights = nx.get_edge_attributes(G, "weight")
    normalized_weights = [(w - min(edge_weights.values())) / (max(edge_weights.values()) - min(edge_weights.values())) for w in edge_weights.values()]

    colormap = plt.cm.viridis
    edge_colors = [colormap(w) for w in normalized_weights]

    # Filter edges to only include those that connect between drawn nodes
    # drawn_edges = [edge for edge in edge_weights.keys() if edge[0] in drawn_nodes and edge[1] in drawn_nodes]

    # nx.draw_networkx_edges(
    #     G, pos=node_positions, edgelist=drawn_edges,
    #     edge_color=edge_colors, arrows=True, arrowstyle='->', width=1, ax=ax
    # )
    drawn_edges = [edge for edge in edge_weights.keys() if edge[0] in drawn_nodes]

    nx.draw_networkx_edges(
        G, pos=node_positions, edgelist=drawn_edges,
        edge_color=edge_colors, arrows=True, arrowstyle='->', width=1.3, ax=ax
    )


    norm = Normalize(vmin=min(edge_weights.values()), vmax=max(edge_weights.values()))
    sm = ScalarMappable(cmap=colormap, norm=norm)
    sm.set_array([])

    cbar = plt.colorbar(sm, orientation='horizontal', ax=ax)
    cbar.set_label('Edge Weight')

    ax.set_title("Strongest Dependencies")

    directory = 'Visualisations/' + config['modelVis']['default'] + '/horizon_' + config['horizonVis']['default'] + '/geographicVis/'
    filename = 'geoVis_split_' + split + '.png'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    fig.savefig(filepath)

# Assuming `create_graph` function is defined elsewhere in your code



def plot_heatmap(adj_matrix, config, split):
    fig_heatmap, ax_heatmap = plt.subplots()
    sns.heatmap(adj_matrix, cmap='YlGnBu', ax=ax_heatmap)
    ax_heatmap.set_title("Adjacency Matrix Heatmap")



    directory = 'Visualisations/' + config['modelVis']['default']+ '/horizon_' + config['horizonVis']['default'] + '/' + 'heatmap/'
    filename = 'heatmap_split_' + split + '.png'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    fig_heatmap.savefig(filepath)



def strong_dfs_paths(G, source, weight_threshold, visited=None, path=None):
    """Recursively finds strong paths using DFS."""
    if visited is None:
        visited = set()
    if path is None:
        path = [source]

    visited.add(source)

    strong_paths = []
    for neighbor in G[source]:
        weight = G[source][neighbor].get('weight', 0)  # Safely get the weight attribute with a default value of 0
        if neighbor not in visited and weight > weight_threshold:
            visited.add(neighbor)
            path.append(neighbor)
            strong_paths.append(list(path))
            strong_paths.extend(strong_dfs_paths(G, neighbor, weight_threshold, visited, path))
            path.pop()

    return strong_paths


def plot_strong_chains(adj_matrix, config, split):
    G = create_graph(adj_matrix, config)
    weight_threshold = 0.0000025
    
    strong_paths = []
    for node in G:
        strong_paths.extend(strong_dfs_paths(G, node, weight_threshold))
    
    # Filter paths with 2 or more edges (i.e., 3 or more nodes)
    strong_paths = [path for path in strong_paths if len(path) >= 3]

    # Extract unique nodes from the strong paths
    strong_nodes = set()
    for path in strong_paths:
        strong_nodes.update(path)

    # Create unique path signatures and assign colors
    path_colors = {}
    number_of_colors = 10
    unique_colors = plt.cm.tab10(np.linspace(0, 1, number_of_colors))
    colors_cycle = cycle(unique_colors)

    for path in strong_paths:
        signature = "-".join(path[:2])
        if signature not in path_colors:
            path_colors[signature] = next(colors_cycle)

    fig, ax = plt.subplots(figsize=(10, 6))

    node_positions = nx.get_node_attributes(G, 'pos')
    min_lon = min(pos[0] for pos in node_positions.values())
    max_lon = max(pos[0] for pos in node_positions.values())
    min_lat = min(pos[1] for pos in node_positions.values())
    max_lat = max(pos[1] for pos in node_positions.values())

    width = max_lon - min_lon
    height = max_lat - min_lat

    m = Basemap(
        llcrnrlon=min_lon - 0.1 * width, llcrnrlat=min_lat - 0.1 * height,
        urcrnrlon=max_lon + 0.1 * width, urcrnrlat=max_lat + 0.1 * height,
        resolution='i', ax=ax
    )
    m.drawcoastlines(linewidth=0.5)
    m.drawmapboundary(fill_color='lightblue')
    m.fillcontinents(color='white', lake_color='lightblue')

    # Convert latitude and longitude to x, y for the basemap
    pos = {node: m(G.nodes[node]['pos'][0], G.nodes[node]['pos'][1]) for node in G.nodes()}

    # Draw nodes and their labels
    nx.draw_networkx_nodes(G, pos, nodelist=strong_nodes, node_size=300, node_color="white", edgecolors="black", ax=ax)
    nx.draw_networkx_labels(G, pos, labels={node: node for node in strong_nodes}, font_size=9, ax=ax)

    # Draw the paths with unique colors
    for path in strong_paths:
        signature = "-".join(path[:2])
        color = path_colors[signature]
        for i in range(len(path) - 1):
            nx.draw_networkx_edges(G, pos, edgelist=[(path[i], path[i + 1])], edge_color=color, width=2, arrows=True, arrowstyle='->', ax=ax)

    
    directory = 'Visualisations/' + config['modelVis']['default']+ '/horizon_' + config['horizonVis']['default'] + '/' + 'chains/'
    filename = 'chains_split_' + split + '.png'
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    fig.savefig(filepath)



def plot(config):
    
    number_of_splits = int(config['splitVis']['default'])
    for split in range(number_of_splits):
        split=str(split)
        matrix_path = "Results/" + config['modelVis']['default'] + "/" + config['horizonVis']['default'] + " Hour Forecast/Matrices_update/adjacency_matrix_" + split + ".csv"
        df = pd.read_csv(matrix_path, index_col=0)
        adj_matrix = df.values

        # plot_strong_chains(adj_matrix, config, split)
        plot_map(adj_matrix, config , split)
        plot_heatmap(adj_matrix, config, split)
