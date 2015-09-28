import clustering.kmeans as kmeans

import util.progress_bar as p_bar
import util.logger as logger


"""
 Calculate using the distances between the points and their barycenters
 and the dinstances between the barycenters themselves.

--------------------------------------------------------------------------------

 Db is the largest distance between two cluster barycenters

 Db = max(d(Gk, Gk'))

--------------------------------------------------------------------------------

 Ew is the sum of distances between points of each cluster and their barycenters

 For each cluster c
    For each point p in cluster c
        Ew += d(p, c.centroid)

--------------------------------------------------------------------------------

 Et is the sum of distances of all points to the barycenter of entire dataset.

 For each point p in dataset
    Et += d(p, centroid),

 where centroid is the barycenter of entire dataset.

--------------------------------------------------------------------------------

 PBM index:

 C = ( (1/K) * (Et / Ew) * Db )^2
"""

def compute(training_set, start_k=2, end_k=7):
    Results = []

    # Main loop. Computes indices for different amount of clusters
    for k in range(start_k, end_k + 1):
        p_bar.init(0, "pbm(" + str(k) + ")")

        # 1) Compute clusters.
        clusters = kmeans.compute(k, training_set)

        # 2) Find maximum distance between two clusters barycenters
        Db = __max_barycenter_distance(clusters)

        Ew = __distance_within_barycenter(clusters)

        Et = __distance_between_barycenter(clusters)

        C = (1/k * (Et / Ew) * Db)**2

        Results.append(C)

        p_bar.finish()

    return Results

#-------------------------------------------------------------------------------

'''
    Computes the largest distance between two cluster barycenters
'''
def __max_barycenter_distance(clusters):
    n = len(clusters)

    if n == 1:
        return 0

    max_d = kmeans.distance(clusters[0].center, clusters[1].center)

    for i in range(0, n-1):
        for j in range(i, n):
            distance = kmeans.distance(clusters[i].center,
                                        clusters[j].center)
            if distance > max_d:
                max_d = distance

    return max_d

#-------------------------------------------------------------------------------

'''
    Computes the sum of distances between points of each cluster
    and their barycenter
'''
def __distance_within_barycenter(clusters):
    Sum = 0

    for c in clusters:
        for p in c.points:
            Sum += kmeans.distance(p, c.center)

    return Sum

#-------------------------------------------------------------------------------

'''
    Computes the sum of distances of all points to the
    barycenter of entire dataset
'''
def __distance_between_barycenter(clusters):
    Sum = 0

    center = __compute_barycenter(clusters)

    for c in clusters:
        for p in c.points:
            Sum += kmeans.distance(p, center)

    return Sum

#-------------------------------------------------------------------------------

'''
    Computes barycenter of entire dataset
'''
def __compute_barycenter(clusters):
    dim = len(clusters[0].points[0])
    center = []

    for i in range(0, dim):
        center.append(0)

    divider = 0

    for cluster in clusters:
        for point in cluster.points:
            center = kmeans.sum(point, center)
            divider += 1

    for i in range(0, dim):
        center[i] /= divider

    return center
