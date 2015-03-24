import numpy as np
from cluster import Cluster
from sklearn.cluster import MiniBatchKMeans, KMeans

"""
Clusterer is used to for clustering computations
"""
class Clusterer:
    def __init__(self):
        pass

    """
    This method should be used to start computation on the set of symbolClasses.
        k - number of clusters.
        symbolClasses - the classes for which the distortions should be clusterized.
    """
    def computeClusters(self, k, symbolClasses):
        for cl in symbolClasses:
            # compute k clusters of each class
            distortedClassesOfSingleClass = cl.distortedClasses
    
            centroids, labels = self.__computeClusters(distortedClassesOfSingleClass, k)
            
            # distinguish k clusters
            for j in range(0,k):
                # points of this cluster
                points = []
                for c in range(0, len(distortedClassesOfSingleClass)):
                    if labels[c] == j:
                        points.append(distortedClassesOfSingleClass[c].characteristicsValues)
    
                cluster = Cluster(centroids[j],points)
                cl.clusters.append(cluster)


    # Computes k cluster by applying kmeans to given sample
    def __computeKMeans(self,sample, k):
        k_means = KMeans(init='k-means++', n_clusters=k, n_init=10)
        X = [];
    
        k_means.fit(sample)
        return k_means.cluster_centers_, k_means.labels_

    # Computes k clusters of given sample of distortedClasses
    def __computeClusters(self,distortedClasses, k):
        X = []
    
        # compute clusters of each class
        for distoredClass in distortedClasses[:]:
            values = []
            for value in distoredClass.characteristicsValues[:]:
                values.append(value)
    
            X.append(values)
    
        centroids, points_labels = self.__computeKMeans(X, k)
              
        return centroids, points_labels