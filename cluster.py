import numpy as np

from sklearn.cluster import MiniBatchKMeans, KMeans

def computeKMeans(sample, k):
    k_means = KMeans(init='k-means++', n_clusters=k, n_init=10)
    X = [];

    k_means.fit(sample)
    return k_means.cluster_centers_

def computeClusters(distortedClasses, k, numberOfDifferentClasses, N):
    centroidsOfAllClasses = []
    for i in range(0, numberOfDifferentClasses):
        X = []

        # compute clusters of each class
        for distoredClass in distortedClasses[i*N:(N+N*i)]:
            values = []
            for value in distoredClass.characteristicsValues[:]:
                values.append(value[0])
            X.append(values)

        centroids = computeKMeans(X, k)

        for j in range(0,k):
            centroidsOfAllClasses.append(centroids[j])
    return centroidsOfAllClasses