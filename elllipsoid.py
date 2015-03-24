import numpy as np
import numpy.linalg as la

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
    
    def mvee(self, points, tol = 0.001):
        """
        Finds the ellipse equation in "center form"
        (x-c).T * A * (x-c) = 1
        """
        
        N, d = points.shape
        Q = np.column_stack((points, np.ones(N))).T
        err = tol+1.0
        u = np.ones(N)/N
        while err > tol:
            # assert u.sum() == 1 # invariant
            X = np.dot(np.dot(Q, np.diag(u)), Q.T)
            M = np.diag(np.dot(np.dot(Q.T, la.inv(X)), Q))
            jdx = np.argmax(M)
            step_size = (M[jdx]-d-1.0)/((d+1)*(M[jdx]-1.0))
            new_u = (1-step_size)*u
            new_u[jdx] += step_size
            err = la.norm(new_u-u)
            u = new_u
        c = np.dot(u,points)        
        A = la.inv(np.dot(np.dot(points.T, np.diag(u)), points)
                   - np.multiply.outer(c,c))/d
        return A, c    