import util.console as console
import sys
import util.global_variables
import data_calculations.synthetic_data_calc as synth_calc
from gui.plot_3d import Plot3D
#from gui.plot_2d import Plot2D
from clustering.clusterer import Clusterer
from data_calculations.distorter import Distorter
import data_calculations.data_manager as data
import symbols.foreign_creator as f_creator
import util.loader as loader
import clustering.prediction_strength as ps
import data_calculations.matrices_batch as mb
from data_calculations.basic_membership import BasicMembership
from data_calculations.basic_membership import ObjectType
import data_calculations.paper2_calc as paper2

import util.logger as logger
import util.progress_bar as p_bar

'''
    Chooses which test should be ran based on input test id
'''
def choose_test():
    if util.global_variables.TEST_TYPE_ID == 1:
        util.global_variables.TEST_TYPE = util.global_variables.TestType.SYNTHETIC_HOMO_NATIVE
    elif util.global_variables.TEST_TYPE_ID == 2:
        util.global_variables.TEST_TYPE = util.global_variables.TestType.GROUPING_ASSESSMENT
    elif util.global_variables.TEST_TYPE_ID == 3:
        util.global_variables.TEST_TYPE = util.global_variables.TestType.FULL
    elif util.global_variables.TEST_TYPE_ID == 4:
        util.global_variables.TEST_TYPE = util.global_variables.TestType.REAL_DATA
    elif util.global_variables.TEST_TYPE_ID == 5:
        util.global_variables.TEST_TYPE = util.global_variables.TestType.STATIC_K_SEMISYNTHETIC_PAPER_2
    elif util.global_variables.TEST_TYPE_ID == 6:
        util.global_variables.TEST_TYPE = util.global_variables.TestType.SYNTHETIC_PAPER_1
    elif util.global_variables.TEST_TYPE_ID == 7:
        util.global_variables.TEST_TYPE = util.global_variables.TestType.SEMISYNTHETIC_PAPER_1
    elif util.global_variables.TEST_TYPE_ID == 8:
        util.global_variables.TEST_TYPE = util.global_variables.TestType.SYNTHETIC_PAPER_2
    elif util.global_variables.TEST_TYPE_ID == 9:
        util.global_variables.TEST_TYPE = util.global_variables.TestType.SEMISYNTHETIC_PAPER_2
    elif util.global_variables.TEST_TYPE_ID == 10:
        util.global_variables.TEST_TYPE = util.global_variables.TestType.PAPER_2

    else:
        util.global_variables.TEST_TYPE = util.global_variables.TestType.NONE

'''
    Native symbols: synthetic; homogeneous;
    Foreign symbols: synthetic; homogeneous and non-homogeneous
'''
def synthetic_homo_native():
    # CREATE CHAR_NUM CHARACTERISTICS
    console.write_header("Creating Characteristics")
    characteristics = []
    data.generate_characteristic(characteristics)

    # CREATE CLASS_NUM SYMBOL CLASSES
    console.write_header(" Creating Symbol Classes")
    symbolClasses = []
    data.generate_symbol_classes(symbolClasses, characteristics)

    # Distortion
    console.write_header("Computing Homogeneous Distortion")
    Distorter().create_homogeneus_cloud(symbolClasses)
    # Clustering
    console.write_header("Computing Clusters")
    Clusterer().computeClusters(symbolClasses[:util.global_variables.CLASS_NUM])
    # Plot3D
    console.write_header(" Displaying Plot")
    Plot3D().renderPlot(symbolClasses[:util.global_variables.CLASS_NUM])
    # Generating Foreign classes
    console.write_header("Creating Non Homogeneous Foreign")
    foreignClassesNonHomo = f_creator.create_non_homogeneous_foreign(symbolClasses)
    console.write_header("Creating Homogeneous Foreign")
    foreignClassesHomo = f_creator.create_homogeneous_foreign(symbolClasses, characteristics)
    # Radiuses
    console.write_header(" Synthetic Data Calculations")
    synth_calc.ambiguity_for_different_radiuses(symbolClasses[:], foreignClassesHomo, foreignClassesNonHomo)


def grouping_assessment():
    # CREATE CHAR_NUM CHARACTERISTICS
    console.write_header("Creating Characteristics")
    characteristics = []
    data.generate_characteristic(characteristics)

    # CREATE CLASS_NUM SYMBOL CLASSES
    console.write_header(" Creating Symbol Classes")
    symbolClasses = []
    data.generate_symbol_classes(symbolClasses, characteristics)

    console.write_header("Computing K cloud Distortion")
    #Distorter().create_k_clouds(util.global_variables.K_CLOUD_DISTORTION,symbolClasses)
    Distorter().create_non_homogeneus_cloud(symbolClasses)
    console.write_header("Computing Cluster Evaluation")
    ps.cluster_evaluation(util.global_variables.MAX_K_CLUS_EVALUATION,symbolClasses)


def full_test():
    # CREATE CHAR_NUM CHARACTERISTICS
    console.write_header("Creating Characteristics")
    characteristics = []
    data.generate_characteristic(characteristics)

    # CREATE CLASS_NUM SYMBOL CLASSES
    console.write_header(" Creating Symbol Classes")
    symbolClasses = []
    data.generate_symbol_classes(symbolClasses, characteristics)

    console.write_header("Computing Homogeneous Distortion")
    Distorter().create_homogeneus_cloud(symbolClasses)

    for c in range(0, util.global_variables.CLASS_NUM):
        console.write_header("Computing Cluster Evaluation")
        best_k = ps.cluster_evaluation(util.global_variables.MAX_K_CLUS_EVALUATION, symbolClasses[c:c+1])
        util.global_variables.K = best_k[0]
        console.write_header("Computing Clusters with K:", str(util.global_variables.K))
        Clusterer().computeClusters(symbolClasses[c:c+1])

    console.write_header("Creating Non Homogeneous Foreign")
    foreignClassesNonHomo = f_creator.create_non_homogeneous_foreign(symbolClasses)
    console.write_header("Creating Homogeneous Foreign")
    foreignClassesHomo = f_creator.create_homogeneous_foreign(symbolClasses, characteristics)
    console.write_header(" Synthetic Data Calculations")
    synth_calc.ambiguity_for_different_radiuses(symbolClasses[:], foreignClassesHomo, foreignClassesNonHomo)

def real_data():
    console.write_header("Loading Native symbols")
    symbolClasses = loader.load_native_xls()
    console.write_header("Loading Foreign symbols")
    foreignClasses = loader.load_foreign_xls()

    util.global_variables.CLASS_NUM = len(symbolClasses)
    util.global_variables.CHAR_NUM = len(symbolClasses[0].learning_set[0].characteristicsValues)

    for c in range(0, util.global_variables.CLASS_NUM):
        console.write_header("Computing Cluster Evaluation")
        best_k = ps.cluster_evaluation(util.global_variables.MAX_K_CLUS_EVALUATION, symbolClasses[c:c+1])
        util.global_variables.K = best_k[0]
        console.write_header("Computing Clusters with K:", str(util.global_variables.K))
        Clusterer().computeClusters(symbolClasses[c:c+1])

    console.write_header(" Synthetic Data Calculations")
    synth_calc.ambiguity_for_different_radiuses_real_data(symbolClasses[:], foreignClasses)


def real_data_static_k():
    console.write_header("Loading Native symbols")
    symbolClasses = loader.load_native_xls()
    console.write_header("Loading Foreign symbols")
    foreignClasses = loader.load_foreign_xls()

    util.global_variables.CLASS_NUM = len(symbolClasses)
    util.global_variables.CHAR_NUM = len(symbolClasses[0].learning_set[0].characteristicsValues)

    #for c in range(0, util.global_variables.CLASS_NUM):
    #    console.write_header("Computing Cluster Evaluation")
    #    best_k = ps.cluster_evaluation(util.global_variables.MAX_K_CLUS_EVALUATION, symbolClasses[c:c+1])
    #    console.write_header("Computing Clusters with K:", str(util.global_variables.K))

    console.write_header("Clustering")
    Clusterer().computeClusters(symbolClasses[:])

    console.write_header(" Synthetic Data Calculations")
    synth_calc.ambiguity_for_different_radiuses_real_data(symbolClasses[:], foreignClasses)

'''
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % SYNTHETIC TEST FOR PAPER 1 %
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    1) Generate characteristics with random intervals(uniform distribution)
    2) Generate 10 class with 1500 elements in each(Training set - 1000, Testing set - 5000)
       (classes - uniform distribution; 1500 distorted elements - normal distribution)
    3) Generate 10 000 homogeneous foreign elements
    4) Generate 10 000 non-homogeneous foreign elements
    5) For each Training set create an ellipsoid
    6) For each Training set create a cuboid
    7) For 6 times:
        >> For each ellipsoid:
            >> Check how many homogeneous foreign are outside
            >> Check how many non-homogeneous foreign are outside
        >> For each cuboid:
            >> Check how many homogeneous foreign are outside
            >> Check how many non-homogeneous foreign are outside
        if(it is not 6th time)
            >> Remove 5% of points in Testing set
            >> Create new(smaller) ellipsoid
            >> Create new(smaller) cuboid
        else
            >> break
'''
def synthetic_test_paper_1():
    # CREATE CHAR_NUM CHARACTERISTICS
    console.write_header("Creating Characteristics")
    characteristics = []
    data.generate_characteristic(characteristics)

    # CREATE CLASS_NUM SYMBOL CLASSES
    console.write_header(" Creating Symbol Classes")
    symbolClasses = []
    data.generate_symbol_classes(symbolClasses, characteristics)

    # DISTORTION (UNIFORM)
    console.write_header("Computing Homogeneous Distortion")
    Distorter().create_homogeneus_cloud(symbolClasses)

    # FOREIGN HOMOGENEOUS
    console.write_header("Creating Homogeneous Foreign")
    foreignClassesHomo = f_creator.create_homogeneous_foreign(symbolClasses, characteristics)

    # FOREIGN NON-HOMOGENEOUS
    console.write_header("Creating Non Homogeneous Foreign")
    foreignClassesNonHomo = f_creator.create_non_homogeneous_foreign(symbolClasses)

    # CREATE ELLIPSOIDS AND CUBOIDS FOR EACH LEARNING SET
    console.write_header("Generating Convex and Compact Sets")
    membership = BasicMembership(symbolClasses)
    membership.shrink_objects(0)  # just to write to he file

    plot = Plot2D()
    plot.renderPlot(symbolClasses, membership, ObjectType.ELLIPSOID)
    plot.renderPlot(symbolClasses, membership, ObjectType.CUBOID)

    for i in range(0,5):
        # Check native
        membership.check_natives_ellipsoid_proper(symbolClasses[:],"foreign_homo","foreign_non_homo")
        membership.check_natives_cuboid_proper(symbolClasses[:],"foreign_homo","foreign_non_homo")
        # Check foreign
        membership.check_foreign_ellipsoid(foreignClassesHomo,      "foreign_homo")
        membership.check_foreign_ellipsoid(foreignClassesNonHomo,   "foreign_non_homo")
        membership.check_foreign_cuboids(foreignClassesHomo,        "foreign_homo")
        membership.check_foreign_cuboids(foreignClassesNonHomo,     "foreign_non_homo")
        # Shrink
        if i != 4:
            membership.shrink_objects(5)
            plot.renderPlot(symbolClasses, membership, ObjectType.ELLIPSOID)
            plot.renderPlot(symbolClasses, membership, ObjectType.CUBOID)

def semisynthetic_test_paper_1():
    console.write_header("Loading Native symbols")
    symbolClasses = loader.load_native_xls()
    console.write_header("Loading Foreign symbols")
    foreignClasses = loader.load_foreign_xls()

    util.global_variables.CLASS_NUM = len(symbolClasses)
    util.global_variables.CHAR_NUM = len(symbolClasses[0].learning_set[0].characteristicsValues)

    # CREATE ELLIPSOIDS AND CUBOIDS FOR EACH LEARNING SET
    console.write_header("Generating Convex and Compact Sets")
    membership = BasicMembership(symbolClasses, False)
    membership.shrink_objects(0)  # just to write to he file



    for i in range(0,5):
        # Check native
        membership.check_natives_ellipsoid_proper(symbolClasses[:],"foreign_REAL","foreign_REAL")
        membership.check_natives_cuboid_proper(symbolClasses[:],"foreign_REAL","foreign_REAL")
        # Check foreign
        membership.check_foreign_ellipsoid(foreignClasses,      "foreign_REAL")
        membership.check_foreign_cuboids(foreignClasses,     "foreign_REAL")
        # Shrink
        if i != 4:
            membership.shrink_objects(5)

def synthetic_test_paper_2():
    # CREATE CHAR_NUM CHARACTERISTICS
    console.write_header("Creating Characteristics")
    characteristics = []
    data.generate_characteristic(characteristics)

    # CREATE CLASS_NUM SYMBOL CLASSES
    console.write_header(" Creating Symbol Classes")
    symbolClasses = []
    data.generate_symbol_classes(symbolClasses, characteristics)

    # CREATE CLOUD DISTORTION IN NATIVE SET
    console.write_header("Computing K cloud Distortion")
    Distorter().create_cluster_assessment_cloud(util.global_variables.K_CLOUD_DISTORTION,symbolClasses)
    #Distorter().create_k_clouds(util.global_variables.K_CLOUD_DISTORTION,symbolClasses)

    util.global_variables.K = 2

    Clusterer().computeClusters(symbolClasses[:])
    Plot3D().renderPlot(symbolClasses)

    util.global_variables.K = 1

    Clusterer().computeClusters(symbolClasses[:])
    Plot3D().renderPlot(symbolClasses)

    util.global_variables.K = 3

    Clusterer().computeClusters(symbolClasses[:])
    Plot3D().renderPlot(symbolClasses)

    # COMPUTE CLUSTER EVALUATION
    #console.write_header("Computing Cluster Evaluation")
    #ps.cluster_evaluation(util.global_variables.MAX_K_CLUS_EVALUATION,symbolClasses)


def synthetic_test_paper_2_old():
    # CREATE CHAR_NUM CHARACTERISTICS
    console.write_header("Creating Characteristics")
    characteristics = []
    data.generate_characteristic(characteristics)

    # CREATE CLASS_NUM SYMBOL CLASSES
    console.write_header(" Creating Symbol Classes")
    symbolClasses = []
    data.generate_symbol_classes(symbolClasses, characteristics)

    # CREATE CLOUD DISTORTION IN NATIVE SET
    console.write_header("Computing K cloud Distortion")
    Distorter().create_cluster_assessment_cloud(util.global_variables.K_CLOUD_DISTORTION,symbolClasses)
    #Distorter().create_k_clouds(util.global_variables.K_CLOUD_DISTORTION,symbolClasses)

    Clusterer().computeClusters(symbolClasses[:])
    Plot3D().renderPlot(symbolClasses)


    # COMPUTE CLUSTER EVALUATION
    console.write_header("Computing Cluster Evaluation")
    ps.cluster_evaluation(util.global_variables.MAX_K_CLUS_EVALUATION,symbolClasses)


def semisynthetic_test_paper_2():
    console.write_header("Loading Native symbols")
    symbolClasses = loader.load_native_xls()
    console.write_header("Loading Foreign symbols")
    foreignClasses = loader.load_foreign_xls()

    util.global_variables.CLASS_NUM = len(symbolClasses)
    util.global_variables.CHAR_NUM = len(symbolClasses[0].learning_set[0].characteristicsValues)

    # COMPUTE CLUSTER EVALUATION
    for c in range(0, util.global_variables.CLASS_NUM):
        console.write_header("Computing Cluster Evaluation")
        best_k = ps.cluster_evaluation(util.global_variables.MAX_K_CLUS_EVALUATION, symbolClasses[c:c+1])
        util.global_variables.K = best_k[0]
        console.write_header("Computing Clusters with K:", str(util.global_variables.K))
        Clusterer().computeClusters(symbolClasses[c:c+1])

    paper2.compute(symbolClasses, foreignClasses)

def static_k_semisynthetic_test_paper_2():
    console.write_header("Loading Native symbols")
    symbolClasses = loader.load_native_xls()
    console.write_header("Loading Foreign symbols")
    foreignClasses = loader.load_foreign_xls()

    util.global_variables.CLASS_NUM = len(symbolClasses)
    util.global_variables.CHAR_NUM = len(symbolClasses[0].learning_set[0].characteristicsValues)


    Clusterer().computeClusters(symbolClasses)

    paper2.compute(symbolClasses, foreignClasses)

"""
0. Compute for original values of characteristics and for its normalization [0,1].
    x_norm = (x-min)/(max-min).

1. Native class is split into Training and Testing set

2. Choose few classes and group them into one set (classes are represented by digits):
    a) 0, 1, 2
    b) 4, 5 ,6
    c) 6, 8, 9
    d) all

3. Group Testing set with 2, 3, 4, ..., c clusters using k-means.
All native classes are treated as one big class. Thus their Training sets are treated
as one big set.

4. Compute cluster evaluation
    a) Prediction strength
    b)
    c)
    d)

5) Create the ellipsoid and hyper rectangle encapsulating all elements of clusters

6) Classifier Quality:
    a) Training vs Testing
    b) Foriegn rejecting
"""
def paper_2():
    logger.log_header("Paper2 Test")

    logger.log_header("Loading Native symbols")


    i_size = 1000
    j_size = 100
    problem_size = i_size * j_size

    p_bar.init_progress_bar(problem_size, "Test Bar")

    for i in range(0, i_size):
        for j in range(0, j_size):
            p_bar.update_progress_bar()

    p_bar.finish_progress_bar()

    symbolClasses = loader.load_native_xls()

    for i in range(0, 10):
        logger.log(str(symbolClasses[i]), "symbols.txt")

    #foreignClasses = loader.load_foreign_xls()
