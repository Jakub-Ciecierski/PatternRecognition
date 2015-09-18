"""
 Sw - the sum of the within-cluster distances

    For each cluster k
        For each two observations in cluster k, Oi, Oj.
            Sw += d(Oi, Oj),
            where d is the distance between two observations.

 Nw - Total number of distances between pairs of points belonging to the same cluster
"""
