# Input:
# - `anchors`: list of 3D coordinates of anchor nodes
# - `distances`: list of measured distances from each anchor to the unknown node
# Output:
# - `location`: 3D coordinates of the estimated location of the unknown node

def centroid_localization(anchors, distances):
    # Step 1: Compute the weights for each anchor based on the measured distances
    weights = []
    for d in distances:
        w = 1.0 / (d ** 2)
        weights.append(w)
    # Step 2: Compute the centroid of the weighted anchor positions
    x_sum, y_sum, z_sum, w_sum = 0.0, 0.0, 0.0, 0.0
    for i in range(len(anchors)):
        x, y, z = anchors[i]
        w = weights[i]
        x_sum += w * x
        y_sum += w * y
        z_sum += w * z
        w_sum += w
    x_avg = x_sum / w_sum
    y_avg = y_sum / w_sum
    z_avg = z_sum / w_sum
    # Step 3: Return the estimated location as the centroid coordinates
    location = (x_avg, y_avg, z_avg)
    return location
