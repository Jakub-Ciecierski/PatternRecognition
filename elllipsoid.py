import numpy as np

class Ellipsoid:
    def __init__(self, x, y, z, r_x, r_y, r_z):
        self.u, self.v = np.mgrid[0:2*np.pi:20j, 0:np.pi:20j]
        self.center_x = x
        self.center_y = y
        self.center_z = z
        self.r_x = r_x
        self.r_y = r_y
        self.r_z = r_z
        self.x = r_x * np.cos(self.u)*np.sin(self.v) + x
        self.y = r_y * np.sin(self.u)*np.sin(self.v) + y
        self.z = r_z * np.cos(self.v) + z
    
    def get_points(self):
        return self.x, self.y, self.z
    
    def is_point_inside(self, point):
        ellipsisFormula = (np.power((point[0]-self.center_x)/self.r_x,2)  +
                            np.power((point[1]-self.center_y)/self.r_y,2)  +
                            np.power((point[2]-self.center_z)/self.r_z,2))
        if(ellipsisFormula <= 1):
            return True
        else:
            return False