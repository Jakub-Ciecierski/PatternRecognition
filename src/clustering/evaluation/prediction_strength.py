from clustering.cluster import Cluster
from gui.plot_3d import Plot3D
import random
import os
from numpy import sqrt
from symbols.symbol_class import SymbolClass

import clustering.kmeans as kmeans

import util.global_variables as global_v
from util.color_chooser import ColorChooser
import util.progress_bar as p_bar
import util.logger as logger

def compute(training_set, start_k=2, end_k=7):
    Results = []
    best_ks = []
    prediction_str = []

    max_ps = 0
    best_k = 1

    for k in range(start_k, end_k+1):
        p_bar.init(0, "ps(" + str(k) + ")")

        avg_ps = 0
        for j in range(0,global_v.MAX_ITER_CLUS_EVALUATION):
            ps = prediction_strength(training_set, k)
            avg_ps += ps
            prediction_str.append(ps)

        avg_ps /= global_v.MAX_ITER_CLUS_EVALUATION
        Results.append(avg_ps)

        p_bar.finish()

        if max_ps <= avg_ps:
            max_ps = avg_ps
            best_k = k

    best_ks.append(best_k)

    return Results

"""
    Computes a cluster evaluation of given data.
    Returns the best number of clusters fitting
    this data set

    Deprecated ! Use compute() instead
"""
def cluster_evaluation(max_k, symbolClasses):
    start_k = 2
    best_ks = []
    for cl in symbolClasses:
        prediction_str = []
        data = cl.learning_set

        logger.log("Symbol: " + str([cl.name]))

        max_ps = 0
        best_k = 1

        for k in range(start_k,max_k+1):
            p_bar.init(0, "ps(" + str(k) + ")")

            avg_ps = 0
            for j in range(0,global_v.MAX_ITER_CLUS_EVALUATION):
                ps = prediction_strength(data, k)
                avg_ps += ps
                prediction_str.append(ps)

            avg_ps /= global_v.MAX_ITER_CLUS_EVALUATION

            logger.log("prediction_strength("+str(k)+") = " + str(avg_ps))

            p_bar.finish()

            if max_ps <= avg_ps:
                max_ps = avg_ps
                best_k = k

        best_ks.append(best_k)

    return best_ks

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
    learningClusters = kmeans.compute(k, learning)
    testClusters = kmeans.compute(k, test)

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

        # Fast hack
        if divider == 0:
            divider = 1

        strength = sum / divider
        strengths.append(strength)

    # Find the minimal strength
    min = strengths[0]
    for i in range(0,len(strengths)):
        if min > strengths[i]:
            min = strengths[i]
    '''
    # find avg
    avg = 0
    for i in range(0,len(strengths)):
        avg += strengths[i]
    avg /= len(strengths)
    '''
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
                cluster_index_i = kmeans.__find_closest_cluster(data[i], clusters)

                cluster_index_j = kmeans.__find_closest_cluster(data[j], clusters)

                if(cluster_index_i == cluster_index_j):
                    m[i][j] = 1
                else:
                    m[i][j] = 0
    return m

def plot_clusters(learningClusters, testClusters):
    symbolLearn = SymbolClass("0", ColorChooser().get_color())
    symbolLearn.clusters = learningClusters

    symbolTest = SymbolClass("0", ColorChooser().get_color())
    symbolTest.clusters = testClusters
    symbols = [symbolLearn]
    Plot3D().renderPlot(symbols)
    symbols = [symbolTest]
    Plot3D().renderPlot(symbols)

def double_print(s, val, f, ending="%"):
    print("        ",s,val,ending)
    f.write(s + str(val) + ending + "\n")

def double_print2(s, f, ending="%"):
    print("        ",s,ending)
    f.write(s + ending + "\n")
