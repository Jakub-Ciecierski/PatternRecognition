class Cluster:
    """
    This class holds data about single cluster,
    its centroid and points around it
    """
    def __init__(self, centroid, points):
        self.centroid = centroid
        self.points = points