import numpy as np
from elllipsoid import Ellipsoid

class Cluster:
    """
    This class holds data about single cluster,
    its centroid and points around it
    """
    def __init__(self, centroid, points):
        self.centroid = centroid
        self.points = points
        self.ellipsoid = self.generate_ellipsoid()
    def generate_ellipsoid(self):
        return Ellipsoid(0,0,0,0,0,0)
    