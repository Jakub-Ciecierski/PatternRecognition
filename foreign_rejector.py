from numpy import sqrt
'''
    Computes tests of accuracy of rejecting Foreign classes
'''
from scipy.spatial.kdtree import distance_matrix
class ForeignRejector:
    def __init__(self):
        pass

    '''
        Computes accuracy of rejecting given set of Foreign classes
        based on the clusters of Native classes
    '''
    def accuracy_of_rejecting(self, foreignClasses, nativeClasses):
        # counts number of rejected foreign classes
        rejectedCount = 0

        # for each foreign class
        for fc in foreignClasses:
            # get its point
            point = []
            point.append(fc.characteristicsValues)
            # save the clusters that accepted this Foreign,
            # later choose the closest one
            acceptedClusters = []
            isRejected = True;
            # check if that point belongs to some cluster
            for nc in nativeClasses:
                for cluster in nc.clusters:
                    ellipsoid = cluster.ellipsoid
                    rejected = ellipsoid.is_point_in_ellipsoid(point)
                    # belongs to cluster
                    if not rejected[0]:
                        isRejected = False
                        acceptedClusters.append(cluster) 
            if isRejected:
                rejectedCount += 1
                # Find the cluster which center is the closest to Foreign point
            else:
                fc.clusters.append(self.__find_closest_cluster(fc.characteristicsValues, acceptedClusters))
        print(">> Result of rejection: " ,
                        rejectedCount / (len(foreignClasses)) * 100, "%")


    def __find_closest_cluster(self, foreignPoint, clusters):
        min_dist = 0
        min_cluster = clusters[0]
        for i in range(len(clusters[0].center)):
            min_dist += (clusters[0].center[i] - foreignPoint[i])**2
        min_dist = sqrt(min_dist)

        for cluster in clusters:
            distance = 0
            for i in range(len(cluster.center)):
                center = cluster.center
                distance += (center[i] - foreignPoint[i])**2
            distance = sqrt(distance)
            if min_dist > distance:
                min_dist = distance
                min_cluster = cluster
        return min_cluster