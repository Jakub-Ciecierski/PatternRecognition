import numpy as np

class Ellipsoid:
    def __init__(self, x, y, z, r_x, r_y, r_z):
        self.u, self.v = np.mgrid[0:2*np.pi:20j, 0:np.pi:20j]
        self.x = r_x * np.cos(self.u)*np.sin(self.v) + x
        self.y = r_y * np.sin(self.u)*np.sin(self.v) + y
        self.z = r_z * np.cos(self.v) + z
    
    def get_points(self):
        return self.x, self.y, self.z