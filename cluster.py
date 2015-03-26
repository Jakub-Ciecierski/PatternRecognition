import numpy as np
from elllipsoid import Ellipsoid
import util.global_variables as global_v

'''
    Structure which holds all needed information about cluster.
'''
class Cluster:
    """
    This class holds data about single cluster,
    its center and points around it
    """
    def __init__(self, centroid, points, name, number):
        self.center = centroid
        self.points = points
        self.ellipsoid = Ellipsoid(self.points)
        if(global_v.CHAR_NUM == 3):    
            self.rejected_x, self.rejected_y, self.rejected_z = self.ellipsoid.is_point_in_ellipsoid(self.points[:])
        else:
            self.rejected_x, self.rejected_y = self.ellipsoid.is_point_in_ellipsoid(self.points[:])

        self.__info(name, number)
        
    '''
        Prints out info about created cluster.
    '''
    def __info(self, name, number):
        print('symbol:',name,'cluster #',number,'\n'
              '>> ellipsoid radius reduced to:', global_v.SEMI_AXIS_SCALE * 100,'%\n'
              '>> points in ellipsoid:',(1- len(self.rejected_x)/len(self.points)) * 100,'%')