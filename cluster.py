import numpy as np

from sklearn.cluster import MiniBatchKMeans, KMeans

def computeKMeans(sample, k):
    k_means = KMeans(init='k-means++', n_clusters=k, n_init=10)
    X = [];

    k_means.fit(sample)
    return k_means.cluster_centers_, k_means.labels_

def computeClusters(distortedClasses, k, numberOfDifferentClasses, N):
    centroidsOfAllClasses = []
    labelsOfAllClasses = []
    for i in range(0, numberOfDifferentClasses):
        X = []

        # compute clusters of each class
        for distoredClass in distortedClasses[i*N:(N+N*i)]:
            values = []
            for value in distoredClass.characteristicsValues[:]:
                values.append(value)

            X.append(values)

        centroids, points_labels = computeKMeans(X, k)
        
        for j in range(0,k):
            centroidsOfAllClasses.append(centroids[j])
        
        labelsOfAllClasses.append(points_labels)
          
    return centroidsOfAllClasses, labelsOfAllClasses