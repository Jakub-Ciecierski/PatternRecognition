from enum import Enum

'''
    Number of different symbol classes.
'''
CLASS_NUM = 1

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
NON_HOMO_CLASSES = True

'''
    If true scale of the graph's axes is <0,20>.
    Otherwise axes are scaled to data values.
'''
UNIFORM_SCALE = False; 

'''
    Number of points for each characteristic in learning set.
'''
N_LEARNING = 1000

'''
    Number of points for each characteristic in test set.
'''
N_TEST = 500

'''
    Number of points which are randomly chose (using gaussian distribution)
    around N_LEARN/DIST_DIV points.
'''
DIST_DIV = 1

'''
    Number of clusters per symbol class.
'''
K = 3

'''
    Minimum distance between centers of every symbol(euclidian)
'''
EUCL_MIN_D = 0.5

'''
    Maximum number of iterations of the k-means algorithm to run.
'''
CLUS_MAX_ITER = 1000

'''
    The relative increment in the results before declaring convergence.
'''
CLUS_TOL = 0.0001

'''
    The maximum amout of clusters (k) for cluster evaluation
'''
MAX_K_CLUS_EVALUATION = 7

'''
    The number of iteration that cluster evaluation for each k should
    be repeated.
'''
MAX_ITER_CLUS_EVALUATION = 10

'''
    Number of clouds in native distortion
'''
K_CLOUD_DISTORTION = 4

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
HOMO_STD_DEV = 0.6

'''
    Standard deviation for gaussian distribution used for
    generation of points surrounding base points in the cloud around original value. 
'''
NON_HOMO_STD_DEV = 0.7

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
LOADING_BARS = True

'''
    If True Redirects stdout output to file, also turns off loading bars
'''
REDIRECT_TO_FILE = True

'''
    The prefix name of log file.
'''
LOG_FILE_PREFIX_NAME = ""

'''
	If set to true will print generated native symbols 
'''
PRINT_GENERATED_SYMBOLS = False

'''
    To control, which type of test is conducted Pair Enum type and global variable
    has been created. By default we perform only test1 i.e. homogeneous native symbols
    and homogeneous foreign symbols.
'''
TestType = Enum('TestType','SYNTHETIC_HOMO_NATIVE GROUPING_ASSESSMENT FULL REAL_DATA REAL_DATA_STATIC_K SYNTHETIC_PAPER_1') 
TEST_TYPE = TestType.REAL_DATA

'''
    Global name is useful for referencing a proper directory.
'''
DIR_NAME = "temp"

'''
    The path to native symbols sample
'''
NATIVE_FILE_PATH = ""

'''
    The path to foreign symbols sample
'''
FOREIGN_FILE_PATH = ""

'''
    Which row to start from
'''
XLS_START_ROW = 2

'''
    How many columns to read, values bellow 0 means all column will be read
'''
XLS_MAX_COL = -1