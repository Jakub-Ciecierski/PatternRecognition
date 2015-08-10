import numpy as np
import numpy.linalg as la
import util.global_variables as global_v
import sys
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
    def __init__(self, points, ratio=1):
        # (x-c).T * A * (x-c) <= 1 with min(log(det A))
        self.M, self.center = self.__mvee(np.array(points))

        # If scaling factor on semi-axes plays some role
        # we applied it.
        if(ratio != 1):
            self.M = self.__scale_semi_axes(self.M, ratio)

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

    def __create_2d_representation(self):
        # Points to representing the shape(ellipsoid)
        u,v = np.mgrid[0:2*np.pi:100j, 0:np.pi:100j]

        # Calculate each semi-axis
        s_a_x, s_a_y = 1./np.sqrt(self.E)

        # Ellipsoid centered at origin; not rotated
        origin_x = s_a_x * np.cos(u)
        origin_y = s_a_y * np.sin(u)

        # Rotate and move to the center
        ellipsoid = np.dstack([origin_x, origin_y])
        ellipsoid = np.dot(ellipsoid,self.V) + self.center
        x, y = np.rollaxis(ellipsoid, axis = -1)

        return x, y

    '''
        When scaling factor of semi-axes comes into game,
        this method perform all indispensable operations and
        returns modified matrix of the ellipsoid.
    '''
    def __scale_semi_axes(self, M,ratio):
        # Decompose matrix A using Single Variable Decomposition
        # to get more information about ellipsoid
        U, E, V = la.svd(self.M, compute_uv=1)

        # Inverse and raise to power 2 global coefficient
        # Why? To get value of each semi-axis from sigma matrix after Singular
        # Value Decomposition, we need to inverse and take square root
        # of each of its diagonal coefficients. So we adapt our scale factor to this
        # procedure.
        scale_coefficient = 100/(np.power(ratio*10, 2))
        # Modify and return semi-axes
        return np.dot(U, np.dot(np.diag(scale_coefficient*E),V))

    '''
        Decide if data is in 3D form and returns set of points
        (or not).
    '''
    def get_points(self):
        if(global_v.CHAR_NUM == 3):
            return self.__create_3d_representation()
        elif(global_v.CHAR_NUM == 2):
            return self.__create_2d_representation()
        else:
            print("Dimensions of data are not equal to 3 or 2.")

    '''
        Check  whether a give point belongs to the ellipsoid or not.
        What's more, it returns 3 vectors of coordinates(X, Y, Z),
        containing points, which does not belong to the shape.
        If data dimension is 2D it returns only X and Y vectors.
        What's more one can set that only number of rejected points
        will be returned.
    '''
    def is_point_in_ellipsoid(self, points, just_number = False, accepted_list= False):
        # BASED ON (x-c)^T * A * (x-c) <= 1 we check if point
        # belongs to ellipsoid/ellipse
        pointsOutX = []
        pointsOutY = []

        resultPoints = []

        rejected_count = 0;
        if(global_v.CHAR_NUM == 3):
            pointsOutZ = []

        #R = np.matrix(self.V[:])
        c = np.matrix(self.center[:])
        n_A = np.matrix(self.M[:])

        for i in range(0, len(points)):
            # Gather n-dim points in matrix
            tmp_point =[]
            for j in range(0, global_v.CHAR_NUM):
                tmp_point.append(points[i][j])

            # Plug points into ellipsoid equation
            p = np.matrix(tmp_point)
            result = (p-c)  * n_A * (p-c).T

            # Gather points which are not belonging to ellipsoid/ellipse
            if(result  > global_v.ELLPSD_TRESH):
                if(not just_number):
                    pointsOutX.append(points[i][0])
                    pointsOutY.append(points[i][1])
                    if(global_v.CHAR_NUM == 3):
                        pointsOutZ.append(points[i][2])
                else:
                    rejected_count+=1
            else:
                resultPoints.append(tmp_point)

        if(not just_number):
            # List of accepted
            if(accepted_list):
                return resultPoints
            # Points for 2/3d plot
            if(global_v.CHAR_NUM == 3):
                return pointsOutX, pointsOutY, pointsOutZ
            else:
                return pointsOutX, pointsOutY
        else:
            return rejected_count


    '''
        Minimum Volume Enclosing Ellipsoid method.
        It returns matrix with ellipsoid features and center point.
    '''
    def __mvee(self, points, tol = global_v.MVEE_ERR):
        if(global_v.LOADING_BARS):
            percentage = 0
            i = global_v.MVEE_ERR * 100
        N_LEARN, d = points.shape
        Q = np.column_stack((points, np.ones(N_LEARN))).T
        err = tol+1.0
        u = np.ones(N_LEARN)/N_LEARN
        while err > tol:
            X = np.dot(np.dot(Q, np.diag(u)), Q.T)
            M = np.diag(np.dot(np.dot(Q.T, la.inv(X)), Q))
            jdx = np.argmax(M)
            step_size = (M[jdx]-d-1.0)/((d+1)*(M[jdx]-1.0))
            new_u = (1-step_size)*u
            new_u[jdx] += step_size
            err = la.norm(new_u-u)
            u = new_u
            # assert u.sum() == 1 # invariant
            if(err < i and global_v.LOADING_BARS):
                percentage += 0.01
                hashes = '#' * int(round(percentage * 20))
                spaces = ' ' * (20 - len(hashes))
                sys.stdout.write("\r        >> minimum volume enclosing ellipsoid calculation: [{0}] {1}%".format(hashes + spaces, int(round(percentage * 100))))
                sys.stdout.flush()
                i -= global_v.MVEE_ERR
        if(global_v.LOADING_BARS):
            print()
        c = np.dot(u,points)
        A = la.inv(np.dot(np.dot(points.T, np.diag(u)), points)
                   - np.multiply.outer(c,c))/d
        return A, c
