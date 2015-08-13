import numpy as np
from clustering.elllipsoid import Ellipsoid
import util.global_variables as global_v
from clustering.cuboid import Cuboid
import util.logger as logger
import util.progress_bar as p_bar

'''
    Structure which holds all needed information about cluster.
'''
class Cluster:
    """
    This class holds data about single cluster,
    its center and points around it
    """
    def __init__(self, centroid, points, name, number, give_info = True, do_ellipsoid = True, do_cuboid = True):
        if give_info:
            logger.log_header("Created Cluster: " + str([name]) + " Number: #" + str(number),
                                styles=[logger.LogHeaderStyle.SUB_HEADER])

        self.center = centroid
        self.points = points
        if do_cuboid:
            logger.log("Creating Cuboid in Cluster")
            self.cuboid = Cuboid(self.points)
        if do_ellipsoid:
            logger.log("Creating Ellipsoid in Cluster")
            self.ellipsoid = Ellipsoid(self.points, global_v.SEMI_AXIS_SCALE)
            if(global_v.CHAR_NUM == 3):
                self.rejected_x, self.rejected_y, self.rejected_z = self.ellipsoid.is_point_in_ellipsoid(self.points[:])
            else:
                self.rejected_x, self.rejected_y = self.ellipsoid.is_point_in_ellipsoid(self.points[:])
            if give_info:
                self.__info(name, number)
                logger.log('Points in ellipsoid: '
                                + str((1- len(self.rejected_x)/len(self.points)) * 100)
                                + '%')

    '''
        Prints out info about created cluster.
    '''
    def __info(self, name, number):
        logger.log("Name: " + str([name]) + " Number #" + str(number) + "\n"
                        + 'ellipsoid radius reduced to:'
                        + str(global_v.SEMI_AXIS_SCALE * 100)
                        + '%\n'
                        + 'minimum volume enclosing ellipsoid error:'
                        + str(global_v.MVEE_ERR))
