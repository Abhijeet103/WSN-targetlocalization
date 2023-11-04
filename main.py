import random

import networkx as nx
import simpy
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from Topology import Topology
from Mobility_Model import MobilityModel
from Node import *
from LocalizationAlgorithms import weighted_centroid , MDS_Localization

# Assuming you have already defined your Topology and MobilityModel classes

# Create a topology
num_anchor_nodes = 25
topology_size = 200
range_threshold = 50
topology = Topology(num_anchor_nodes, topology_size, range_threshold)

# Add a mobile node to the topology
mobile_node = topology.add_mobile_node(25, 50, 50)

# Create a SimPy environment
env = simpy.Environment()

# Define speed and pause time ranges
speed_range = (5,10)  # Example range, adjust as needed
pause_time_range = (1,2)  # Example range, adjust as needed

# Initialize a MobilityModel
mobility_model = MobilityModel(topology, mobile_node, env, speed_range,100 , pause_time_range  )

# Set up the plot for animation
fig, ax = plt.subplots()
pos = {n: topology.graph.nodes[n]['position'] for n in topology.graph.nodes}
node_colors = ['lightblue' if topology.graph.nodes[n]['type'] == 'AnchorNode' else 'red' for n in topology.graph.nodes]
node_sizes = [1000 if topology.graph.nodes[n]['type'] == 'MobileNode' else 500 for n in topology.graph.nodes]
nx.draw(topology.graph, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, font_size=10, ax=ax)
id_mobile  = topology.get_mobile_node_id()

def update(frame):
    if frame > 0:
        env.run(until=frame)
        ax.clear()
        # Re-add edges within range
        randNodeid =  random.randint(0 , num_anchor_nodes-1)
        node =  topology.anchor_nodes[randNodeid]
        topology.delete_anchor_node(randNodeid)
        topology.add_edges_within_range()
        topology.add_anchor_node(randNodeid ,node.x, node.y)
        pos = {n: topology.graph.nodes[n]['position'] for n in topology.graph.nodes}
        node_colors = ['lightblue' if topology.graph.nodes[n]['type'] ==  NodeType.ANCHOR else 'red' for n in topology.graph.nodes]
        node_sizes = [1000 if topology.graph.nodes[n]['type'] == NodeType.MOBILE else 500 for n in topology.graph.nodes]
        nx.draw(topology.graph, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, font_size=10, ax=ax)
        # Call visualize_topology to update the positions of mobile nodes in the visualization
        actualx, actualy = topology.mobile_nodes.x, topology.mobile_nodes.y
        hop = topology.compute_hop_table()
        # dropping a random node
        predictedx, predictedy = MDS_Localization(topology)

        #weighted_centroid(hop, topology)
        print(actualx , actualy)
        print(predictedx , predictedy)

        # Calculate MSE
        rmse = ((predictedx - actualx) ** 2 + (predictedy - actualy) ** 2)**0.5 / 2
        print(f"RMSE: {rmse}")

        # Draw the actual and predicted locations
        plt.scatter(actualx, actualy, color='green', marker='o', s=100, label='Actual')
        plt.scatter(predictedx, predictedy, color='red', marker='x', s=100, label='Predicted')

        # Add legend
        plt.legend()

        # Adjust plot limits if needed
        plt.xlim(0, topology_size)
        plt.ylim(0, topology_size)


        # adjacency_matrix = nx.to_numpy_array(topology.graph)
        # print("Adjacency Matrix:")
        # print(adjacency_matrix)


# Create an animation
ani = FuncAnimation(fig, update, frames=range(100), repeat=False, interval=1000) # Adjust interval as needed
plt.show()
