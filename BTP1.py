import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import simpy
import math

env = simpy.Environment()
# Define the dimensions of the simulation space
x_max = 100
y_max = 100

# Define the number of anchor nodes
num_anchor_nodes = 25

# Define the distance between each anchor node
dist_between_anchors = x_max / (num_anchor_nodes ** 0.5 + 1)

# Define the unknown node locations
unknown_node_locs = np.random.uniform(low=0, high=x_max, size=(1, 2))

# Define the location of the sink node
sink_node_pos = np.array([x_max / 2, y_max / 2])

# Create an adjacency matrix for the graph
graph = nx.Graph()

# Create the anchor node locations
anchor_node_locs = np.zeros((num_anchor_nodes, 2))
anchor_count = 0
for i in range(num_anchor_nodes):
    col = i % int(num_anchor_nodes ** 0.5)
    row = i // int(num_anchor_nodes ** 0.5)
    anchor_node_locs[anchor_count][0] = (col + 1) * dist_between_anchors
    anchor_node_locs[anchor_count][1] = (row + 1) * dist_between_anchors
    anchor_count += 1

# Add edges between anchor nodes and their neighbors
for i in range(num_anchor_nodes):
    col = i % int(num_anchor_nodes ** 0.5)
    row = i // int(num_anchor_nodes ** 0.5)
    for j in range(num_anchor_nodes):
        if i != j:
            col_j = j % int(num_anchor_nodes ** 0.5)
            row_j = j // int(num_anchor_nodes ** 0.5)
            if col_j == col or row_j == row or abs(col_j - col) == abs(row_j - row):
                dist = ((anchor_node_locs[i][0] - anchor_node_locs[j][0]) ** 2 +
                        (anchor_node_locs[i][1] - anchor_node_locs[j][1]) ** 2) ** 0.5
                if dist < 2 * dist_between_anchors:
                    graph.add_edge(i, j,weight =1)

#Add edges between anchor nodes and sink node
for i in range(num_anchor_nodes):
    dist = ((anchor_node_locs[i][0] - sink_node_pos[0]) ** 2 +
            (anchor_node_locs[i][1] - sink_node_pos[1]) ** 2) ** 0.5
    if dist < 2 * dist_between_anchors:
        graph.add_edge(i, num_anchor_nodes, weight=1)

# Add edges between sink node and its neighbors
for i in range(num_anchor_nodes):
    dist = ((anchor_node_locs[i][0] - sink_node_pos[0]) ** 2 +
            (anchor_node_locs[i][1] - sink_node_pos[1]) ** 2) ** 0.5
    if dist < 2 * dist_between_anchors:
        graph.add_edge(num_anchor_nodes, i, weight=1)

# Print the adjacency matrix
adj_mat = nx.to_numpy_array(graph)
print(adj_mat)
# print(anchor_node_locs)
# print(unknown_node_locs)
# print(sink_node_pos)
# Calculate the hop count for each anchor node
# Calculate the hop count for each anchor node
hop_count = np.zeros(num_anchor_nodes)
for i in range(num_anchor_nodes):
    path_length = nx.shortest_path_length(graph, source=i, target=num_anchor_nodes, weight='weight')
    hop_count[i] = path_length   # Exclude the sink node from the hop count

print("hop",hop_count)
# Create the plot of the graph
# pos = {}
# for i in range(num_anchor_nodes):
#     pos[i] = tuple(anchor_node_locs[i])
# pos[num_anchor_nodes] = tuple(sink_node_pos)
#
# # Color the sink node green
# node_colors = ['blue'] * num_anchor_nodes + ['green']
#
# nx.draw_networkx_nodes(graph, pos, node_size=200, node_color=node_colors)
# nx.draw_networkx_edges(graph, pos, arrows=True)
# nx.draw_networkx_labels(graph, pos, font_size=10, font_family="sans-serif")
# plt.axis("off")
# plt.show()

weights = []
for i in range(len(hop_count)):
    weights.append(1/hop_count[i])

print(weights)

def centroidLocalization(unknown_node):
    threshold_nodes =[]
    threshold_weights = []
    for i in range(len(anchor_node_locs)):
        distance = math.sqrt((anchor_node_locs[i][0] - unknown_node[0]) ** 2 + (anchor_node_locs[i][1] - unknown_node[1]) ** 2)
        if distance <= 20:
            threshold_nodes.append(anchor_node_locs[i])
            threshold_weights.append(weights[i])

    x=0
    y=0
    sumX = 0
    sumY =0
    totalWeight = 0
    for i in range(len(threshold_nodes)):
        sumX +=   threshold_weights[i]*threshold_nodes[i][0]
        sumY += threshold_weights[i]*threshold_nodes[i][1]
        totalWeight += threshold_weights[i]

    x = sumX/totalWeight
    y = sumY/totalWeight
    print(x,y)
    return [x,y]
    # print(threshold_weights)
    # print(threshold_nodes)

def plot_topology(unknown_node_pos, predicted_pos ,accuracy):
    # Plot the anchor nodes
    plt.clf()
    plt.scatter(anchor_node_locs[:, 0], anchor_node_locs[:, 1], c='b', label='Anchor Nodes')

    # Plot the unknown nodes
    plt.scatter(unknown_node_pos[0][0], unknown_node_pos[0][1], c='r', label='Unknown Node')

    # Plot the predicted position
    plt.scatter(predicted_pos[0], predicted_pos[1], marker='x', c='r', s=100, label='Predicted Position')

    # Plot the sink node
    plt.scatter(sink_node_pos[0], sink_node_pos[1], marker='^', c='g', s=200, label='Sink Node')

    # Set the axis limits
    plt.xlim(0, x_max)
    plt.ylim(0, y_max)
    # Add the text box for predicted and actual position
    text = f"Predicted Pos: ({predicted_pos[0]:.2f}, {predicted_pos[1]:.2f})\nActual Pos: ({unknown_node_pos[0][0]:.2f}, {unknown_node_pos[0][1]:.2f})\nAccuracy: {accuracy:.2f}%"
    plt.text(0.02, 1.1, text, transform=plt.gca().transAxes, va='top', ha='left', fontsize=12)
    # Add the legend and show the plot
    # Add the legend and show the plot
    plt.legend(bbox_to_anchor=(-.16, 1), loc='upper left')
    plt.pause(0.01) # Pause the plot for 0.01 seconds to create a video effect


def unknown_node_behavior(env):
    unknown_node_vel = np.array([1, 1])  # Initial velocity of the unknown node
    unknown_node_pos = unknown_node_locs[0]  # Initial position of the unknown node
    unknown_node_path = [unknown_node_pos]  # List to store the path of the unknown node
    print(unknown_node_pos)

    while True:
        # Update the position of the unknown node
        unknown_node_pos = unknown_node_pos + unknown_node_vel

        # Check if the unknown node has collided with the boundary of the simulation space
        if (unknown_node_pos[0] < 0) or (unknown_node_pos[0] > x_max):
            unknown_node_vel[0] = -unknown_node_vel[0]
        if (unknown_node_pos[1] < 0) or (unknown_node_pos[1] > y_max):
            unknown_node_vel[1] = -unknown_node_vel[1]

        # Append the current position
        unknown_node_path.append(unknown_node_pos)
        #predicted_pos = predict_unknown_node_position([1,1] , anchor_node_locs)
        predicted_pos = centroidLocalization(unknown_node_pos)
        print(predicted_pos)
        errorX = abs(unknown_node_pos[0] - predicted_pos[0])
        errorY =  abs(unknown_node_pos[1] - predicted_pos[1])
        accX = (1 - errorX/unknown_node_pos[0])*100
        accY = (1 - errorY / unknown_node_pos[1]) * 100
        totalacc  = (accX +accY) /2
        # Update the plot
        plot_topology([unknown_node_pos],predicted_pos,totalacc)

        # Randomly change the velocity of the unknown node at random times
        if np.random.random() < 0.1:  # Probability of changing the velocity is 0.1
            unknown_node_vel = np.random.uniform(low=-1, high=1, size=2)

        # Wait for some time before the next update
        yield env.timeout(1)


# Start the simulation
#centroidLocalization([43,10])
env.process(unknown_node_behavior(env))
env.run(until=1000)
