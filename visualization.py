"""
Logistics Visualization Module
==============================

This module provides visualization tools for simulating and animating logistics
delivery networks. It integrates `networkx` for graph topology handling and
`matplotlib` for rendering static maps and dynamic vehicle movements.
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
import numpy as np

def get_graph_and_pos(graph_dict):
    """"
    Constructs a NetworkX graph and calculates fixed node positions.

    This function converts an adjacency dictionary into a graph object and uses
    the spring layout algorithm with a fixed seed to generate consistent
    coordinates for visualization.

    Args:
        graph_dict (dict): A dictionary representing the graph where keys are nodes
                           and values are dictionaries of neighbors with edge weights.
                           Example: {'A': {'B': 5}, 'B': {'A': 5}}

    Returns:
        tuple: A tuple (G, pos) containing:
            - G (networkx.Graph): The generated graph object.
            - pos (dict): A dictionary of node coordinates {node: (x, y)}.
    """
    G = nx.Graph()
    for u, neighbors in graph_dict.items():
        for v, w in neighbors.items():
            if not G.has_edge(u, v):
                G.add_edge(u, v, weight=w)
    pos = nx.spring_layout(G, seed=42, k=0.5)
    return G, pos

def draw_base_map(ax, G, pos, warehouse):
    """
    Renders the static base map (roads, cities, warehouse) onto a Matplotlib axis.

    Visualizes the graph structure including edges (roads) and nodes (cities).
    The warehouse node is highlighted with a distinct color and size.

    Args:
        ax (matplotlib.axes.Axes): The target Axes object to draw on.
        G (networkx.Graph): The logistics graph object.
        pos (dict): Dictionary of node positions.
        warehouse (Hashable): The identifier for the warehouse node (e.g., 'K').
    """

    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color='#e0e0e0', width=1.5, alpha=0.7
    )

    all_nodes = list(G.nodes)
    cities = [n for n in all_nodes if n != warehouse]

    nx.draw_networkx_nodes(
        G, pos, nodelist=cities, ax=ax,
        node_color='#89CFF0',
        edgecolors='white',
        linewidths=1.5, node_size=700
    )

    if warehouse in G.nodes:
        nx.draw_networkx_nodes(
            G, pos, nodelist=[warehouse],
            node_color='#FFD700', edgecolors='orange',
            linewidths=2, node_size=900, ax=ax, label="Склад"
        )

    for node, (x, y) in pos.items():
        ax.text(
            x, y, s=str(node),
            fontsize=10, fontweight='bold', color='#333333',
            ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8)
        )

def animate_delivery(vehicles, graph_dict, warehouse):
    """
    Initializes and executes the delivery simulation animation.

    This function sets up the plot, computes the interpolation paths for smooth
    movement, and animates truck icons traveling between nodes along their
    optimal routes.

    Args:
        vehicles (list): A list of dictionaries, each representing a truck.
                         Must contain 'optimal_route' (list of nodes) and 'id'.
        graph_dict (dict): The graph data in adjacency dictionary format.
        warehouse (Hashable): The identifier for the warehouse node.

    Returns:
        matplotlib.animation.FuncAnimation: The animation object.
        (Note: This object must be assigned to a variable to persist.)
    """
    G, pos = get_graph_and_pos(graph_dict)

    fig, ax = plt.subplots(figsize=(12, 8))
    draw_base_map(ax, G, pos, warehouse)

    lines = []
    trucks = []

    colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A8', '#FF8F33', '#8D33FF']
    vehicles_data = []
    max_frames = 0
    legend_handles = []

    for i, v in enumerate(vehicles):
        route = v.get('optimal_route', [])
        if len(route) < 2:
            continue
        path_points = []
        steps_per_segment = 50

        for j in range(len(route) - 1):
            start_pos = np.array(pos[route[j]])
            end_pos = np.array(pos[route[j + 1]])
            segment = np.linspace(start_pos, end_pos, steps_per_segment)
            path_points.extend(segment[:-1])

        path_points.append(np.array(pos[route[-1]]))
        vehicles_data.append(path_points)
        max_frames = max(max_frames, len(path_points))

        color = colors[i % len(colors)]

        line, = ax.plot([], [], color=color, alpha=0.7, linewidth=3)
        lines.append(line)

        truck_icon = ax.text(0, 0, "🚚", fontsize=24, ha='center', va='center', zorder=20)
        trucks.append(truck_icon)

        label_text = f"Вантажівка {v.get('id')} ({len(v.get('packages', []))} пак.)"
        legend_line, = ax.plot([], [], color=color, linewidth=3, label=label_text)
        legend_handles.append(legend_line)

    ax.legend(handles=legend_handles, loc='upper left', fontsize=10, frameon=True, framealpha=0.9)
    ax.set_title("Доставка пакунків", fontsize=16, pad=20)
    ax.axis('off')

    def init():
        for line, truck in zip(lines, trucks):
            line.set_data([], [])
            truck.set_position((0, 0))
            truck.set_alpha(0)
        return lines + trucks

    def update(frame):
        for i, data in enumerate(vehicles_data):
            if frame < len(data):
                x, y = data[frame]
                trucks[i].set_alpha(1)
                trucks[i].set_position((x, y))

                history = np.array(data[:frame + 1])
                if len(history) > 0:
                    lines[i].set_data(history[:, 0], history[:, 1])
            else:
                if len(data) > 0:
                    x, y = data[-1]
                    trucks[i].set_position((x, y))
        return lines + trucks

    ani = FuncAnimation(
        fig, update, frames=max_frames + 30,
        init_func=init, interval=20, blit=False, repeat=False
    )
    plt.tight_layout()
    plt.show()
    return ani
