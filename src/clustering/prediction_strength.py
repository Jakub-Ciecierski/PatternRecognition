from src.clustering.cluster import Cluster
from sklearn.cluster import MiniBatchKMeans, KMeans
import src.util.global_variables as global_v
from src.gui.plot_3d import Plot3D
import random
from src.symbols.symbol_class import SymbolClass
from src.util.color_chooser import ColorChooser

"""
    Computes a cluster evaluation of given data.
    Returns the best number of clusters fitting 
    this data set 
"""
def cluster_evaluation(max_k, symbolClasses):
    for cl in symbolClasses:
        print('\n    SYMBOL:',[cl.name])
        data = cl.learning_set
        max = 0
        best_k = 1
        for k in range(1,max_k+1):
            ps = prediction_strength(data, k)
            print("        >> prediction_strength(",k,") = ", ps)
            if max < ps:
                max = ps
                best_k = k
    print('        >> The True k:',best_k, "\n")
    return best_k

"""
    Computes the prediction strength
    
    Split data into: Learning and Test sets
    Compute k-means for both sets.

    Computes the co-membership of each Test cluster
    in respect to Learnings clusters.
    
    Compute strength of each Test cluster and 
    find the minimum value
"""
def prediction_strength(data, k):
    # Split data into two sets
    learning = []
    test = []
    
    for i in range(0,int(len(data))):
        random.choice((learning,test)).append(data[i])

    # Compute k-clustering of both sets
    learningClusters = computeClusters(k, learning)
    testClusters = computeClusters(k, test)
    
    # PLOT
    #plot_clusters(learningClusters, testClusters)

    #
    # Take set of points of each Test cluster and 
    # compute its co-membership matrix with respect to
    # the set of Learning clusters.
    #
    # Do it for each Test cluster (check of Test points)
    # while computing its strength.
    # The min of strengths of all clusters will be the
    # Predictions strength
    #
    strengths = []
    for i in range(0,k):
        # Compute sum of elements in co_membership matrix
        sum = 0
        co_memb = co_membership(learningClusters, testClusters[i].points)

        # Compute strength of each Test cluster    
        for r in range(0,len(co_memb)):
            for c in range(0, len(co_memb[r])):
                sum += co_memb[r][c]
        n = len(testClusters[i].points)
        divider = n*(n-1)
        strength = sum / divider
        strengths.append(strength)
    
    # Find the minimal strength
    min = strengths[0]
    for i in range(0,len(strengths)):
        if min > strengths[i]:
            min = strengths[i]

    return min

'''
    Let data be a set of n elements, then co-membership 
    is an n by n matrix with (i,j)th element equal to 1
    if i and j fall into the same cluster from the clusters set,
    0 otherwise.
    The clusters and data can come from different samples (of the same population) 
'''
def co_membership(clusters, data):
    # creating co_membership matrix
    m = [[0 for x in range(len(data))] for x in range(len(data))]
    
    # check if each pair of points belong
    # to the same cluster
    for i in range(0,len(data)):
        for j in range(0,len(data)):
            if(i != j):
                for cluster in clusters:
                    # both must belong to the same cluster
                    i_belongs = False
                    j_belongs = False

                    # return 0 if point belongs to cluster
                    point = []
                    point.append(data[i])
                    count = cluster.ellipsoid.is_point_in_ellipsoid(
                                    point, just_number = True)
                    if count == 0:
                        i_belongs = True
                    
                    point = []
                    point.append(data[j])
                    count = cluster.ellipsoid.is_point_in_ellipsoid(
                                    point, just_number = True)
                    if count == 0:
                        j_belongs = True
                    
                    if i_belongs and j_belongs:
                        m[i][j] = 1
                        break
                    else:
                        m[i][j] = 0
    return m

def computeClusters(k, data):
    clusters = []
    centroids, labels = __computeClusters(k, data)

    # distinguish k clusters
    for j in range(0,k):
        # points of this cluster
        points = []
        for c in range(0, len(data)):
            if labels[c] == j:
                points.append(data[c].characteristicsValues)

        cluster = Cluster(centroids[j],points, data[c].name, j, False)
        clusters.append(cluster)
    return clusters

'''
    Computes k cluster by applying kmeans to given sample.
'''
def __computeKMeans( k, sample):
    k_means = KMeans(init='k-means++', n_clusters=k, n_init=10
                        , max_iter=global_v.CLUS_MAX_ITER, tol=global_v.CLUS_TOL, random_state=4444)
    k_means.fit(sample)
    return k_means.cluster_centers_, k_means.labels_

'''
    Computes k clusters of given sample of learning_set.
'''
def __computeClusters(k, distortedClasses):
    X = []

    # compute clusters of each class
    for distoredClass in distortedClasses[:]:
        values = []
        for value in distoredClass.characteristicsValues[:]:
            values.append(value)

        X.append(values)

    centroids, points_labels = __computeKMeans(k, X)
          
    return centroids, points_labels

def plot_clusters(learningClusters, testClusters):
    symbolLearn = SymbolClass("0", ColorChooser().get_color())
    symbolLearn.clusters = learningClusters
    
    symbolTest = SymbolClass("0", ColorChooser().get_color())
    symbolTest.clusters = testClusters
    symbols = [symbolLearn]
    Plot3D().renderPlot(symbols)
    symbols = [symbolTest]
    Plot3D().renderPlot(symbols)