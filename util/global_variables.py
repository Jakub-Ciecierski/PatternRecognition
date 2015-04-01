'''
    Number of different symbol classes.
'''
CLASS_NUM = 5

'''
    Number of characteristics for each symbol class.
'''
CHAR_NUM = 3

'''
    Number of symbol classes displayed on the graph.
    When CLASS_DISPLAY_NUM = CLASS_NUM, graph displays all of them.
'''
CLASS_DISPLAY_NUM = 3

'''
    If set to True, classes will be distorted in non-homogeneus way.
    Otherwise it will be common gaussian distribution around center.
'''
NON_HOMO_CLASSES = False

'''
    If true scale of the graph's axes is <0,20>.
    Otherwise axes are scaled to data values.
'''
UNIFORM_SCALE = False; 

'''
    Number of points for each characteristic in learning set.
'''
N_LEARNING = 100

'''
    Number of points for each characteristic in test set.
'''
N_TEST = 50

'''
    Number of points which are randomly chose (using gaussian distribution)
    around N_LEARN/DIST_DIV points.
'''
DIST_DIV = 1

'''
    Number of clusters per symbol class.
'''
K = 5

'''
    Maximum number of iterations of the k-means algorithm to run.
'''
CLUS_MAX_ITER = 300

'''
    The relative increment in the results before declaring convergence.
'''
CLUS_TOL = 0.001

'''
    Each ellipsoid's semi-axis will be scaled by this factor.
'''
SEMI_AXIS_SCALE = 1.0
'''
    When checking the points membership to the ellipsoid, some error
    tolerance can be take. Default value is 1 and there is no need 
    to go below it. Really.
'''
ELLPSD_TRESH = 1.001

'''
    Accuracy of Minimum Volume Enclosing Ellipsoid method.
    Recommended settings:
    >>    0.00001
'''
MVEE_ERR = 0.001

'''
    Randomized values of all characteristics will be picked from
    this interval.
'''
CHAR_INTERVAL = [0,20]

'''
    Standard deviation for gaussian distribution used for
    generation of based points in the cloud around original value. 
'''
HOMO_STD_DEV = 1.5

'''
    Standard deviation for gaussian distribution used for
    generation of points surrounding base points in the cloud around original value. 
'''
NON_HOMO_STD_DEV = 0.5

'''
    The distance threshold between properly generated Foreign characteristics
    and Native characteristics.
    Distance greater than this threshold will be accepted.
'''
FOREIGN_CHAR_DIST_THRESH = 0

'''
    The number of clusters in non Homogeneous creation mode of Foreign classes
'''
FOREIGN_NON_HOMO_CLUSTER_COUNT = 5

'''
    Turns on/off loading bars.
'''
LOADING_BARS = False

'''
    If True Redirects stdout output to file, also turns off loading bars
'''
REDIRECT_TO_FILE = True
