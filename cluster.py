import numpy as np

from sklearn.cluster import MiniBatchKMeans, KMeans

def computeCluster(sample, k):
    k_means = KMeans(init='k-means++', n_clusters=k, n_init=10)
    X = [];

    k_means.fit(sample)
    return k_means.cluster_centers_