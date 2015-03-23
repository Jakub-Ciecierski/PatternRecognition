import numpy as np
from cluster import Cluster
from sklearn.cluster import MiniBatchKMeans, KMeans

"""
Clusterer is used to for clustering computations
"""
class Clusterer:
    def __init__(self):
        pass

    # This method should be used to start computation on the set of symbolClasses
    def computeClustersOfSymbols(self, k, symbolClasses, distortedClasses, N):
        for i in range(0,len(symbolClasses)):
            # compute k clusters of each class
            distortedClassesOfSingleClass = distortedClasses[i*N:(N+N*i)]
    
            centroids, labels = self.computeClusters2(distortedClassesOfSingleClass, k)
            
            # distinguish k clusters
            for j in range(0,k):
                # points of this cluster
                points = []
                for c in range(0, len(distortedClassesOfSingleClass)):
                    if labels[c] == j:
                        points.append(distortedClassesOfSingleClass[c].characteristicsValues)
    
                cluster = Cluster(centroids[j],points)
                symbolClasses[i].clusters.append(cluster)


    # Computes k cluster by applying kmeans to given sample
    def computeKMeans(self,sample, k):
        k_means = KMeans(init='k-means++', n_clusters=k, n_init=10)
        X = [];
    
        k_means.fit(sample)
        return k_means.cluster_centers_, k_means.labels_

    # Computes k clusters of given sample of distortedClasses
    def computeClusters2(self,distortedClasses, k):
        X = []
    
        # compute clusters of each class
        for distoredClass in distortedClasses[:]:
            values = []
            for value in distoredClass.characteristicsValues[:]:
                values.append(value)
    
            X.append(values)
    
        centroids, points_labels = self.computeKMeans(X, k)
              
        return centroids, points_labels