from sklearn.cluster import MiniBatchKMeans, KMeans
import util.global_variables as global_v
from clustering.cluster import Cluster
from numpy import sqrt

def compute(k, training_set):
    clusters = []
    centroids, labels = __computeClusters(k, training_set)

    # distinguish k clusters
    for j in range(0,k):
        # points of this cluster
        points = []
        for c in range(0, len(training_set)):
            if labels[c] == j:
                points.append(training_set[c].characteristicsValues)

        cluster = Cluster(centroids[j], points, training_set[c].name, j,
                            give_info = False,
                            do_ellipsoid=False,
                            do_cuboid=False)

        clusters.append(cluster)

    return clusters

'''
    Computes k cluster by applying kmeans to given sample.
'''
def __computeKMeans(k, sample):
    k_means = KMeans(init='k-means++', n_clusters=k, n_init=10,
                        max_iter=global_v.CLUS_MAX_ITER,
                        tol=global_v.CLUS_TOL, random_state=4444)

    k_means.fit(sample)

    return k_means.cluster_centers_, k_means.labels_

'''
    Computes k clusters of given sample of learning_set.
'''
def __computeClusters(k, training_set):
    X = []

    # compute clusters of each class
    for training_symbol in training_set[:]:
        values = []
        for value in training_symbol.characteristicsValues[:]:
            values.append(value)

        X.append(values)

    centroids, points_labels = __computeKMeans(k, X)

    return centroids, points_labels

def __find_closest_cluster(foreignPoint, clusters):
    min_dist = 0
    min_cluster = clusters[0]
    min_i = 0
    for i in range(len(clusters[0].center)):
        min_dist += (clusters[0].center[i] - foreignPoint[i])**2
    min_dist = sqrt(min_dist)

    for i in range(0,len(clusters)):
        distance = 0
        for j in range(len(clusters[i].center)):
            center = clusters[i].center
            distance += (center[j] - foreignPoint[j])**2
        distance = sqrt(distance)
        if min_dist > distance:
            min_dist = distance
            min_cluster = clusters[i]
            min_i = i
    return min_i


def distance(point1, point2):
    dist = 0

    for i in range(0, len(point1)):
        dist += (point1[i] - point2[i])**2

    dist = sqrt(dist)

    return dist
