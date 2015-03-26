import numpy as np
import numpy.linalg as la
import util.global_variables as global_v

'''
    Class manages all operations regarding ellipsoid.
'''
class Ellipsoid:
    '''
        Computes smallest ellipsoid based on points attribute.
        For this purpose Minimum Volume Enclosing Ellipsoid method is used.
        In addition matrix M describing newly created shape is saved along 
        with its center.
        If needed - semi-axes are scaled by some predefined factor.
        Matrices of Singular Value Decomposition operation are saved for 
        further usage.
    '''
    def __init__(self, points):
        # (x-c).T * A * (x-c) <= 1 with min(log(det A))
        self.M, self.center = self.__mvee(np.array(points))
        
        # If scaling facor os semi-axes plays some role
        # we applied it.
        if(global_v.SEMI_AXIS_SCALE != 1):
            self.M = self.__scale_semi_axes(self.M)
        
        # Decompose matrix A using Single Variable Decomposition
        # to get more information about ellipsoid  
        # U - don't matter
        # E - from diagonal values we get semi-axes
        # V - rotation matrix       
        self.U, self.E, self.V = la.svd(self.M, compute_uv=1)
    
    '''
        Using information calculated in __init__() method,
        it computes set of points, which can be easily used
        to render the shape.
    '''
    def __create_3d_representation(self):
        # Points to representing the shape(ellipsoid)
        u,v = np.mgrid[0:2*np.pi:20j, 0:np.pi:20j]
        
        # Calculate each semi-axis   
        s_a_x, s_a_y, s_a_z = 1./np.sqrt(self.E)
        
        # Ellipsoid centered at origin; not rotated 
        origin_x = s_a_x * np.cos(u) * np.sin(v)
        origin_y = s_a_y * np.sin(u) * np.sin(v)
        origin_z = s_a_z * np.cos(v)
        
        # Rotate and move to the center
        ellipsoid = np.dstack([origin_x, origin_y, origin_z])
        ellipsoid = np.dot(ellipsoid,self.V) + self.center
        x, y, z = np.rollaxis(ellipsoid, axis = -1)
        
        return x, y, z
    
    '''
        When scaling factor of semi-axes comes into game, 
        this method perform all indispensable operations and
        returns modified matrix of the ellipsoid.
    '''    
    def __scale_semi_axes(self, M):
        # Decompose matrix A using Single Variable Decomposition
        # to get more information about ellipsoid    
        U, E, V = la.svd(self.M, compute_uv=1)
        
        # Inverse and raise to power 2 global coefficient
        # Why? To get value of each semi-axis from sigma matrix after Singular
        # Value Decomposition, we need to inverse and take square root
        # of each of its diagonal coefficients. So we adapt our scale factor to this
        # procedure.
        scale_coefficient = 100/(np.power(global_v.SEMI_AXIS_SCALE*10, 2))
        # Modify and return semi-axes 
        return np.dot(U, np.dot(np.diag(scale_coefficient*E),V))
        
    '''
        Decide if data is in 3D form and returns set of points
        (or not).
    '''       
    def get_points(self):
        if(global_v.CHAR_NUM == 3):
            return self.__create_3d_representation()
        else:
            print("Dimensions of data are not equal to 3.")
            
    '''
        Check  whether a give point belongs to the ellipsoid or not.
        What's more, it returns 3 vectors of coordinates(X, Y, Z),
        containing points, which does not belong to the shape.
    '''
    def is_point_in_ellipsoid(self, points):
        # BASED ON (x-c)^T * A * (x-c) <= 1 we check if point
        # belongs to ellipsoid/ellipse
        pointsOutX = []
        pointsOutY = []
        if(global_v.CHAR_NUM == 3):
            pointsOutZ = []
        
        R = np.matrix(self.V[:])
        c = np.matrix(self.center[:]) 
        n_A = np.matrix(self.M[:]) 
        
        for i in range(0, len(points)):
            # Gather n-dim points in matrix
            tmp_points =[]
            for j in range(0, global_v.CHAR_NUM):
                tmp_points.append(points[i][j])
            
            # Plug points into ellipsoid equation    
            p = np.matrix(tmp_points)
            result = (p-c)  * n_A * (p-c).T
            
            # Gather points which are not belonging to ellipsoid/ellipse 
            if(result  > global_v.ELLPSD_TRESH):
                pointsOutX.append(points[i][0])
                pointsOutY.append(points[i][1])
                if(global_v.CHAR_NUM == 3):
                    pointsOutZ.append(points[i][2])
        
        if(global_v.CHAR_NUM == 3):    
            return pointsOutX, pointsOutY, pointsOutZ
        else:
            return pointsOutX, pointsOutY
    '''
        Minimum Volume Enclosing Ellipsoid method.
        It returns matrix with ellipsoid features and center point.
    '''
    def __mvee(self, points, tol = global_v.MVEE_ERR):
        
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