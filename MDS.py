import numpy as np
import simpy
from scipy.spatial import distance
from sklearn.manifold import MDS
import matplotlib.pyplot as plt


def calculate_mds_map(coordinates):
    # Calculate the dissimilarity matrix using Euclidean distance
    dissimilarity_matrix = distance.squareform(distance.pdist(coordinates))

    # Apply MDS to obtain the map
    embedding = MDS(n_components=2, dissimilarity='precomputed')
    map_coords = embedding.fit_transform(dissimilarity_matrix)

    distances_3d = []
    for i in range(1, len(coordinates)):
        distance_3d = distance.euclidean(coordinates[0], coordinates[i])
        distances_3d.append(distance_3d)

    distances_2d = []
    for i in range(1, len(map_coords)):
        distance_2d = distance.euclidean(map_coords[0], map_coords[i])
        distances_2d.append(distance_2d)

    # Calculate the mean distances
    mean_distance_3d = np.mean(distances_3d)
    mean_distance_2d = np.mean(distances_2d)

    # Calculate the percentage difference
    accuracy = (1 - (mean_distance_3d - mean_distance_2d) / mean_distance_3d) * 100

    return map_coords, accuracy


def plot_mds_map(map_coords,  accuracy):
    plt.clf()
    plt.scatter(map_coords[:, 0], map_coords[:, 1], c='blue', label='Anchor Nodes')
    plt.scatter(map_coords[0, 0], map_coords[0, 1], marker = 'X' ,c='red', label='Target Node')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('MDS Map (Accuracy: {:.2f}%)'.format(accuracy))
    plt.legend()
    plt.grid(True)
    plt.draw()
    plt.pause(1)


def target_node_behavior(coordinates):
    while True:
        # Randomly change the coordinates of the target node
        target = coordinates[0]
        target += np.random.uniform(-1, 1, size=3)
        target %= 90

        # Update the MDS map and calculate accuracy
        map_coords, accuracy = calculate_mds_map(coordinates)

        # Plot the MDS map with accuracy
        plot_mds_map(map_coords, accuracy)

        # Wait for a certain duration before the next update
        yield env.timeout(1)  # Change the timeout value as desired




# Number of points
num_points = 10

# Generate random coordinates
coordinates = np.random.uniform(low=-90, high=90, size=(num_points, 3))

# Create SimPy environment
env = simpy.Environment()

# Start the target node behavior process
env.process(target_node_behavior(coordinates))

# Initialize Matplotlib interactive mode
plt.ion()

# Run the simulation indefinitely
plt.show()
env.run()
