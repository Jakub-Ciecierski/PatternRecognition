import clustering.kmeans as kmeans

import util.progress_bar as p_bar
import util.logger as logger

"""
 Compute the mean of quatients between BGSS and TSS for each dimension
 of data (i.e. each column  of matrix A)

 BGSS (Between-Group Dispersion) measures the dispersion of the clusters between each otherwise

 TSS (Total Sum of Squares) - Measrues the variance of each column
 vector of matrix A i.e. the vector of a variable for all observations.
"""

def compute(training_set, start_k=2, end_k=7):
    Results = []

    # Main loop. Computes indices for different amount of clusters
    for k in range(start_k, end_k + 1):
        p_bar.init(0, "rat_l(" + str(k) + ")")

        # 1) Compute clusters.
        clusters = kmeans.compute(k, training_set)

        center = __compute_barycenter(clusters)

        p = len(center)
        R = 0

        for j in range(0, p):
            BGSS_j +=


#-------------------------------------------------------------------------------

'''
    Computes the BGSS for j-th dimension (feature) of dataset
'''
def __compute_bgss_j(j, clusters, center):
    BGSSj = 0

    for c in clusters
        c_center = c.center
        nk = len(c.points)

        BGSSj += nk * ((c_center[j] - center[j])**2)

    return BGSSj

#-------------------------------------------------------------------------------
'''
    Computes the TSS for j-th dimension (feature) of dataset
'''
def __compute_tss_j(j, clusters, center):
    TSSj = 0
    # For all points in dataset
    for c in clusters:
        for p in c.points:
            TSSj += (p[j] - center[j])**2

    return TSSj

#-------------------------------------------------------------------------------

'''
    Computes barycenter of entire dataset
'''
def __compute_barycenter(clusters):
    dim = len(clusters[0].points[0])
    center = []

    for i in range(0, dim):
        center.append(0)

    divider = 0

    for cluster in clusters:
        for point in cluster.points:
            center = kmeans.sum(point, center)
            divider += 1

    for i in range(0, dim):
        center[i] /= divider

    return center
