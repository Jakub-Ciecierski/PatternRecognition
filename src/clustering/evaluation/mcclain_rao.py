import clustering.kmeans as kmeans

import util.progress_bar as p_bar
import util.logger as logger


"""
 Sw - the sum of the within-cluster distances

    For each cluster k
        For each two observations in cluster k, Oi, Oj.
            Sw += d(Oi, Oj),
            where d is the distance between two observations.

 Nw - Total number of distances between pairs of points belonging to the same cluster

---------------------------------------------------------------------------------------

 Sb - The sum of between-cluster dinstances
    For each distinct pair of clusters k, k'
        For each two observations Oi in k and Oj in k'
            Sb += d(Oi, Oj)

 Nb - Total number of distances between pairs of points which do not belong
 to the same cluster.

 Nb = N(N-1)/2 - Nw

---------------------------------------------------------------------------------------

Quotient between the mean within-cluster and between-cluster distances.

C = (Sw / Nw) / (Sb / Nb) = (Nb / Nw) * (Sw/Sb)

"""

'''
    Starts the computations for McClain Rao index.

    Data - the Training set
'''
def compute(training_set, start_k = 2, end_k = 7):
    Results = []

    # Main loop. Computes indices for different amount of clusters
    for k in range(start_k, end_k + 1):
        # 1) Compute clusters.
        clusters = kmeans.compute(k, training_set)

        # 2) Compute sum of distances of within clusters
        Sw, Nw = __sum_within(clusters)

        # 3) Sum of distances of between pairs of points
        Sb, Nb = __sum_between(clusters)
        N = len(training_set)
        Nb = ((N * (N - 1)) / 2 )- Nw

        # McClain-Rao Index
        C = (Sw/Nw) / (Sb/Nb)
        Results.append(C)

    return Results

'''
    Computes the sum of the within-cluster distances
'''
def __sum_within(clusters):
    Sum = 0
    Nw = 0

    # For each cluster
    for c in clusters:
        p_len = len(c.points)
        # For each distinct pair of points in cluster
        for i in range(0, p_len - 1):
            for j in range(i+1, p_len):
                Sum += kmeans.distance(c.points[i], c.points[j])
                Nw += 1

    return Sum, Nw

def __sum_between(clusters):
    Sum = 0
    Nb = 0

    cluster_len = len(clusters)

    # For each pair of distinct clusters
    for i in range(0, cluster_len - 1):
        for j in range(i+1, cluster_len):
            for p1 in clusters[i].points:
                for p2 in clusters[j].points:
                    Sum += kmeans.distance(p1, p2)
                    Nb += 1

    return Sum, Nb
