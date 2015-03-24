import numpy as np
import numpy.linalg as la

class Ellipsoid:
    def __init__(self, points):
        # Points to representing the shape(ellipsoid)
        u,v = np.mgrid[0:2*np.pi:20j, 0:np.pi:20j]
        
        # (x-c).T * A * (x-c) <= 1 with min(log(det A))
        self.A, self.centroid = self.mvee(np.array(points))
        
        # Decompose matrix A using Single Variable Decomposition
        # to get more information about ellipsoid    
        U, D, self.V = la.svd(self.A)
        
        # Calculate each radius in 3D    
        rx, ry, rz = 1./np.sqrt(D)
        
        # Ellipsoid centered at origin; not rotated 
        origin_x = rx * np.cos(u) * np.sin(v)
        origin_y = ry * np.sin(u) * np.sin(v)
        origin_z = rz * np.cos(v)
        
        # Rotate and move to the center
        E = np.dstack([origin_x, origin_y, origin_z])
        
        E = np.dot(E,self.V) + self.centroid
        
        # Save final set of points for further rendering       
        self.x, self.y, self.z = np.rollaxis(E, axis = -1)
            
    def get_points(self):
        return self.x, self.y, self.z
    
    def is_point_in_ellipsoid(self, points):
        # BASED ON (x-c)^T * R^T * A * R * (x-c) <= 1 we check if point
        # belongs to sphere
        pointsOutX = []
        pointsOutY = []
        pointsOutZ = []
        R = np.matrix(self.V[:])
        c = np.matrix(self.centroid[:]) 
        n_A = np.matrix(self.A[:]) 
        
        for i in range(0, len(points)):
            p = np.matrix([points[i][0],points[i][1],points[i][2]])
            result = (p-c)  * n_A * (p-c).T
             
            if(result  > 1.05):
                pointsOutX.append(points[i][0])
                pointsOutY.append(points[i][1])
                pointsOutZ.append(points[i][2])
#             print('result', result)
            
#             print([points[i][0],points[i][0],points[i][0]])

        return pointsOutX, pointsOutY, pointsOutZ
    
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