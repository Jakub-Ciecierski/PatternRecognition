from symbols.symbol_class import SymbolClass
import sys

from clustering.clusterer import Clusterer

import clustering.evaluation.prediction_strength as ps
import clustering.evaluation.mcclain_rao as mc_r
import clustering.evaluation.pbm as pbm
import clustering.evaluation.ratkowsky_lance as rat_l

from util.color_chooser import ColorChooser
import util.loader as loader
import util.global_variables as global_v
import util.logger as logger
import util.progress_bar as p_bar

import data_calculations.classification as classifier

"""
0. Compute for original values of characteristics and for its normalization [0,1].
    x_norm = (x-min)/(max-min).

1. Native class is split into Training and Testing set

2. Choose few classes and group them into one set (classes are represented by digits):
    a) 0, 1, 2
    b) 4, 5 ,6
    c) 6, 8, 9
    d) all

3. Group Training set with 2, 3, 4, ..., c clusters using k-means.
All native classes are treated as one big class. Thus their Training sets are treated
as one big set.

3.1. Create the ellipsoid and hyper rectangle encapsulating all elements of clusters

4. Compute cluster evaluation
    a) Prediction strength
    b)
    c)
    d)

5) Classifier Quality:
    a) Training vs Testing
    b) Foriegn rejecting
"""

'''
    Should the cluster evaluation be computed
'''
CLUSTER_EVALUATION = False

def run():
    # 1), 2) Load symbols
    nativeElements, foreignElements = __load_symbols()

    # 0) Normalize the characterstic values
    if global_v.NORMALIZE:
        __normalize(nativeElements, foreignElements)

    # 3) Compute clusters
    # 3.1) Compute Ellipsoids and cuboids
    __compute_clusters(nativeElements)

    # 4) Cluster evaluation
    if CLUSTER_EVALUATION:
        __compute_cluster_evaluation(nativeElements.learning_set)

    # 5) Compute Classifier quality
    __compute_classifier_quality(nativeElements, foreignElements)

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

"""
    0) Normalize the characterstic values to [0,1].
    x_norm = (x-min)/(max-min).

    TODO How to find min max...
"""
def __normalize(nativeElements, foreignElements):
    logger.log_header("Normalization")

    MIN_INDEX = 0
    MAX_INDEX = 1

    # Find MIN / MAX For native elements
    min_max_values = __min_max(nativeElements, MIN_INDEX, MAX_INDEX)

    for nativeClass in nativeElements:

        for element in nativeClass.learning_set:
            for i in range(0, len(element.characteristicsValues)):
                charValue = element.characteristicsValues[i]
                element.characteristicsValues[i] = __norm(charValue,
                                                    min_max_values[i][MIN_INDEX],
                                                    min_max_values[i][MAX_INDEX])

        for element in nativeClass.test_set:
            for i in range(0, len(element.characteristicsValues)):
                charValue = element.characteristicsValues[i]
                element.characteristicsValues[i] = __norm(charValue,
                                                        min_max_values[i][MIN_INDEX],
                                                        min_max_values[i][MAX_INDEX])

    # Find MIN / MAX For foreign elements
    """
    min_max_values = __min_max(foreignElements, MIN_INDEX, MAX_INDEX)

    for element in foreignElements:
        for i in range(0, len(element.characteristicsValues)):
            charValue = element.characteristicsValues[i]
            element.characteristicsValues[i] = __norm(charValue,
                                                min_max_values[i][MIN_INDEX],
                                                min_max_values[i][MAX_INDEX])
    """

#------------------------------------------------------------------------------------

def __norm(x, min, max):

    x_norm = (x - min) / (max - min)

    if x_norm > 1.0 or x_norm < 0.0:
        logger.log("Normalization failed. Exiting...")
        sys.exit()

    return x_norm

#------------------------------------------------------------------------------------

def __min_max(nativeElements, MIN_INDEX=0, MAX_INDEX=1):

    # Get the dimension
    dim = len(nativeElements[0].learning_set[0].characteristicsValues)

    # Set up min max values of each characterstic
    min_max_values = [[0]*2 for x in range(dim)]
    for min_max_value in min_max_values:
        min_max_value[MIN_INDEX] = 99999
        min_max_value[MAX_INDEX] = -99999

    logger.log_header("Normalizing Native",
                        styles=[logger.LogHeaderStyle.SUB_HEADER])

    for nativeClass in nativeElements:

        # Find max and min of each characterstic
        for element in nativeClass.learning_set:
            # Dimensions must fit
            if len(element.characteristicsValues) != dim:
                logger.log("Incorrect dimensions. Exiting...")
                sys.exit()

            # Find min max
            for i in range(0, dim):
                charValue = element.characteristicsValues[i]
                # Min
                if min_max_values[i][MIN_INDEX] >= charValue:
                    min_max_values[i][MIN_INDEX] = charValue
                # Max
                if min_max_values[i][MAX_INDEX] <= charValue:
                    min_max_values[i][MAX_INDEX] = charValue

        # Find max and min of each characterstic
        for element in nativeClass.test_set:
            # Dimensions must fit
            if len(element.characteristicsValues) != dim:
                logger.log("Incorrect dimensions. Exiting...")
                sys.exit()

            # Find min max
            for i in range(0, dim):
                charValue = element.characteristicsValues[i]
                # Min
                if min_max_values[i][MIN_INDEX] >= charValue:
                    min_max_values[i][MIN_INDEX] = charValue
                # Max
                if min_max_values[i][MAX_INDEX] <= charValue:
                    min_max_values[i][MAX_INDEX] = charValue
    """
    for i in range(0, dim):
        logger.log("Value #" + str(i), filename="test.txt")
        logger.log(min_max_values[i][MIN_INDEX],
                    filename="test.txt",
                    styles=[logger.LogStyle.NONE])
        logger.log(min_max_values[i][MAX_INDEX],
                    filename="test.txt",
                    styles=[logger.LogStyle.NONE])
    """
    return min_max_values

#------------------------------------------------------------------------------------

def __compute_normalization():
    pass

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

"""
    1) SPLIT NATIVE CLASS INTO TRAINING AND TESTING sets
    TODO: separate loading and spliting from 'loader' module
    TODO: save the split configuration and use the same one accross all test instances
"""
def __load_symbols():
    # Load Native symbols
    logger.log_header("Loading Native symbols")
    nativeElements = loader.deserialize_native()

    # Load Foreign symbols
    logger.log_header("Loading Foreign symbols")
    foreignElements = loader.load_foreign_xls()

    global_v.CLASS_NUM = 1
    global_v.CHAR_NUM = len(nativeElements.learning_set[0].characteristicsValues)

    return nativeElements, foreignElements

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

"""
    3) CLUSERING
    3.1) CREATING ELLIPSOIDS AND CUBOIDS
"""
def __compute_clusters(nativeElements):
    logger.log_header("Clustering K = " + str(global_v.K))

    # Init the progress bar
    p_bar.init(1, "Clustering")

    # Legacy function, requirs a list as input
    tmp_list = [nativeElements]
    Clusterer().computeClusters(tmp_list)

    # Finish the progress bar
    p_bar.finish()

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

'''
    4) CLUSTER EVALUATION
'''
def __compute_cluster_evaluation(training_set):
    start_k = 2
    end_k   = global_v.MAX_K_CLUS_EVALUATION

    __ps_evaluation(training_set, start_k, end_k)

    __mc_r_evaluation(training_set, start_k, end_k)

    __pbm_evaluation(training_set, start_k, end_k)

    __rat_l_evaluation(training_set, start_k, end_k)

#-------------------------------------------------------------------------------

def __ps_evaluation(training_set, start_k, end_k):
    logger.log_header("Prediction Strength",
                        filename=logger.LOG_CLUSTER_FILE_NAME,
                        styles=[logger.LogHeaderStyle.SUB_HEADER])

    Results = ps.compute(training_set,
                start_k, end_k)

    for i in range(0, len(Results)):
        logger.log("ps(" + str(i+start_k) + ") = " + str(Results[i]),
                    filename=logger.LOG_CLUSTER_FILE_NAME,
                    styles=[logger.LogStyle.NONE])


#-------------------------------------------------------------------------------

def __mc_r_evaluation(training_set, start_k, end_k):
    logger.log_header("McClain-Rao",
                        filename=logger.LOG_CLUSTER_FILE_NAME,
                        styles=[logger.LogHeaderStyle.SUB_HEADER])

    Results = mc_r.compute(training_set,
                            start_k, end_k)

    for i in range(0, len(Results)):
        logger.log("mc_r(" + str(i+start_k) + ") = " + str(Results[i]),
                    filename=logger.LOG_CLUSTER_FILE_NAME,
                    styles=[logger.LogStyle.NONE])

#-------------------------------------------------------------------------------

def __pbm_evaluation(training_set, start_k, end_k):
    logger.log_header("PBM",
                        filename=logger.LOG_CLUSTER_FILE_NAME,
                        styles=[logger.LogHeaderStyle.SUB_HEADER])

    Results = pbm.compute(training_set,
                            start_k, end_k)

    for i in range(0, len(Results)):
        logger.log("pbm(" + str(i+start_k) + ") = " + str(Results[i]),
                    filename=logger.LOG_CLUSTER_FILE_NAME,
                    styles=[logger.LogStyle.NONE])

#-------------------------------------------------------------------------------

def __rat_l_evaluation(training_set, start_k, end_k):
    logger.log_header("Ratkowsky-Lance",
                        filename=logger.LOG_CLUSTER_FILE_NAME,
                        styles=[logger.LogHeaderStyle.SUB_HEADER])

    Results = rat_l.compute(training_set,
                                start_k, end_k)

    for i in range(0, len(Results)):
        logger.log("rat_l(" + str(i+start_k) + ") = " + str(Results[i]),
                    filename=logger.LOG_CLUSTER_FILE_NAME,
                    styles=[logger.LogStyle.NONE])

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

"""
    5) CLASSIFIER QUALITY
"""
def __compute_classifier_quality(nativeElements, foreignElements):
    # Ellipsoids
    __compute_classifier_quality_ellipsoids(nativeElements, foreignElements)

    # Cuboids
    __compute_classifier_quality_cuboids(nativeElements, foreignElements)

#------------------------------------------------------------------------------------

"""
    5.1) Classifier Quality - Ellipsoids
"""
def __compute_classifier_quality_ellipsoids(nativeElements, foreignElements):
    logger.log_header("Classification. Ellipsoids")

    # Training vs Test, Ellipsoids
    logger.log_header("Classification Training vs Testing. Ellipsoids",
                        styles=[logger.LogHeaderStyle.SUB_HEADER])
    TP, FN = classifier.compute_training_vs_testing(nativeElements,
                                                    classifier.CLASSIFY_ELLIPSOID)

    # Native vs Foreign, Ellipsoids
    logger.log_header("Classification Native vs Foreign. Ellipsoids",
                        styles=[logger.LogHeaderStyle.SUB_HEADER])
    TN, FP = classifier.compute_native_vs_foreign(nativeElements,
                                                    foreignElements,
                                                    classifier.CLASSIFY_ELLIPSOID)

    # Classifier Measurements
    (accuracy, sensitivity,
        precision, f_measure) = classifier.compute_measurements(TP, FN, TN, FP)

    # Print results
    __print_results(accuracy, sensitivity,
                    precision, f_measure,
                    TP, FN, TN, FP,
                    classifier.CLASSIFY_ELLIPSOID)

#------------------------------------------------------------------------------------

"""
    5.2) Classifier Quality - Cuboids
"""
def __compute_classifier_quality_cuboids(nativeElements, foreignElements):
    logger.log_header("Classification. Cuboids")

    # Training vs Test, Cuboids
    logger.log_header("Classification Training vs Testing. Cuboids",
                        styles=[logger.LogHeaderStyle.SUB_HEADER])
    TP, FN = classifier.compute_training_vs_testing(nativeElements,
                                                    classifier.CLASSIFY_CUBOID)

    # Native vs Foreign, Cuboids
    logger.log_header("Classification Native vs Foreign. Cuboids",
                        styles=[logger.LogHeaderStyle.SUB_HEADER])
    TN, FP = classifier.compute_native_vs_foreign(nativeElements,
                                                    foreignElements,
                                                    classifier.CLASSIFY_CUBOID)

    # Classifier Measurements
    (accuracy, sensitivity,
        precision, f_measure) = classifier.compute_measurements(TP, FN, TN, FP)

    # Print results
    __print_results(accuracy, sensitivity,
                    precision, f_measure,
                    TP, FN, TN, FP,
                    classifier.CLASSIFY_CUBOID)

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

"""
    Prints final results
"""
def __print_results(accuracy, sensitivity, precision, f_measure,
                    TP, FN, TN, FP,
                    classify_geometry):

    # Choose the file for results
    if classify_geometry == classifier.CLASSIFY_ELLIPSOID:
        filename = logger.LOG_RESULTS_ELLIPSOIDS_FILE_NAME
        header = "Ellipsoids"
    elif classify_geometry == classifier.CLASSIFY_CUBOID:
        filename = logger.LOG_RESULTS_CUBOIDS_FILE_NAME
        header = "Cuboids"

    # The decimel to round to for logging results
    round_decimel = 2

    # Main Header
    logger.log_header("Results: " + header, filename)

    # SubHeader: Classifier Quality
    logger.log_header("Classifier Quality: " + header,
                        filename, styles=[logger.LogHeaderStyle.SUB_HEADER])

    logger.log("TP: " + str(round(TP, round_decimel)),
                filename,
                styles=[logger.LogStyle.NONE])
    logger.log("FN: " + str(round(FN, round_decimel)),
                filename,
                styles=[logger.LogStyle.NONE])
    logger.log("TN: " + str(round(TN, round_decimel)),
                filename,
                styles=[logger.LogStyle.NONE])
    logger.log("FP: " + str(round(FP, round_decimel)),
                filename,
                styles=[logger.LogStyle.NONE])

    # SubHeader: Classifier Measurements
    logger.log_header("Classifier Measurements: " + header,
                        filename, styles=[logger.LogHeaderStyle.SUB_HEADER])

    logger.log("Accuracy: " + str(round(accuracy, round_decimel)),
                filename,
                styles=[logger.LogStyle.NONE])
    logger.log("Sensitivity: " + str(round(sensitivity, round_decimel)),
                filename,
                styles=[logger.LogStyle.NONE])
    logger.log("Precision: " + str(round(precision, round_decimel)),
                filename,
                styles=[logger.LogStyle.NONE])
    logger.log("F-Measure: " + str(round(f_measure,round_decimel)),
                filename,
                styles=[logger.LogStyle.NONE])
