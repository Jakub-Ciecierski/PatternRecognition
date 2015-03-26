'''
    Number of different symbol classes.
'''
CLASS_NUM = 10

'''
    Number of characteristics for each symbol class.
'''
CHAR_NUM = 3

'''
    Number of symbol classes displayed on the graph.
    When CLASS_DISPLAY_NUM = CLASS_NUM, graph displays all of them.
'''
CLASS_DISPLAY_NUM = 1

'''
    If true scale of the graph's axes is <0,20>.
    Otherwise axes are scaled to data values.
'''
UNIFORM_SCALE = False; 

'''
    Number of points for each characteristic.
'''
N = 100
'''
    Number of points which are randomly chose (using gaussian distribution)
    around N/DIST_DIV points.
'''
DIST_DIV = 1

'''
    Number of clusters per symbol class.
'''
K = 3

'''
    Each ellipsoid's semi-axis will be scaled by this factor.
'''
SEMI_AXIS_SCALE = 0.85

'''
    When checking the points membership to the ellipsoid, some error
    tolerance can be take. Default value is 1 and there is no need 
    to go below it. Really.
'''
ELLPSD_TRESH = 1.00

'''
    Accuracy of Minimum Volume Enclosing Ellipsoid method.
    Recommended settings:
    >> for 3D:    0.001 
    >> for 10D: 0.00001
'''
MVEE_ERR = 0.0001

'''
    Randomized values of all characteristics will be picked from
    this interval.
'''
CHAR_INTERVAL = [0,20]

'''
    Standard deviation for gaussian distribution used for
    generation of based points in the cloud around original value. 
'''
DIST_BASE_P_SD = 0.6

'''
    Standard deviation for gaussian distribution used for
    generation of points surrounding base points in the cloud around original value. 
'''
DIST_CLOUD_P_SD = 0.3


'''
    The distance threshold between properly generated Foreign characteristics
    and Native characteristics.
    Distance greater than this threshold will be accepted.
'''
FOREIGN_CHAR_DIST_THRESH = 0