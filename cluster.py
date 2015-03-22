import numpy as np

from sklearn.cluster import MiniBatchKMeans, KMeans

def computeCluster(sample, k):
    k_means = KMeans(init='k-means++', n_clusters=3, n_init=10)
    
    k_means.fit(sample)
    k_means_cluster_centers = k_means.cluster_centers_
