import numpy as np
from clustering.elllipsoid import Ellipsoid
import util.global_variables as global_v

'''
    Structure which holds all needed information about cluster.
'''
class Cluster:
    """
    This class holds data about single cluster,
    its center and points around it
    """
    def __init__(self, centroid, points, name, number, give_info = True, do_ellipsoid = True):
        self.center = centroid
        self.points = points
        if do_ellipsoid:
            self.ellipsoid = Ellipsoid(self.points, global_v.SEMI_AXIS_SCALE)
            if(global_v.CHAR_NUM == 3):    
                self.rejected_x, self.rejected_y, self.rejected_z = self.ellipsoid.is_point_in_ellipsoid(self.points[:])
            else:
                self.rejected_x, self.rejected_y = self.ellipsoid.is_point_in_ellipsoid(self.points[:])
            if give_info:
                self.__info(name, number)
                print('        >> points in ellipsoid:',(1- len(self.rejected_x)/len(self.points)) * 100,'%','\n')

    '''
        Prints out info about created cluster.
    '''
    def __info(self, name, number):
        print('    SYMBOL:',[name],'CLUSTER #',number,'\n'
              '        >> ellipsoid radius reduced to:', global_v.SEMI_AXIS_SCALE * 100,'%\n',
              '       >> minimum volume enclosing ellipsoid error:',global_v.MVEE_ERR)
