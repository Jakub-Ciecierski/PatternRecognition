import numpy as np
from elllipsoid import Ellipsoid

class Cluster:
    """
    This class holds data about single cluster,
    its centroid and points around it
    """
    def __init__(self, centroid, points, name, number):
        self.centroid = centroid
        self.points = points
        self.ellipsoid = Ellipsoid(self.points)
        self.pox, self.poy, self.poz = self.ellipsoid.is_point_in_ellipsoid(self.points[:]) 
        print('symbol:',name,'cluster:',number,'points in ellipsoid:',(1- len(self.pox)/len(self.points)) * 100,'%')

    