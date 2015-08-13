from symbols.symbol_class import SymbolClass

from clustering.clusterer import Clusterer
import clustering.evaluation.prediction_strength as ps

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
def run():
    # 1) Load symbols
    nativeElements, foreignElements = __load_symbols()

    # 2) Choose classes
    nativeElements = __choose_native_classes(nativeElements)

    # 3) Compute clusters
    # 3.1) Compute Ellipsoids and cuboids
    __compute_clusters(nativeElements)

    # 4) Cluster evaluation
    __compute_cluster_evaluation(nativeElements)

    # 5) Compute Classifier quality
    __compute_classifier_quality(nativeElements, foreignElements)

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
    nativeElements = loader.load_native_xls()

    # Load Foreign symbols
    logger.log_header("Loading Foreign symbols")
    foreignElements = loader.load_foreign_xls()

    global_v.CLASS_NUM = len(nativeElements)
    global_v.CHAR_NUM = len(nativeElements[0].learning_set[0].characteristicsValues)

    return nativeElements, foreignElements

#------------------------------------------------------------------------------------

"""
    2) SELECT AND GROUP CLASSES FROM NATIVE SET
"""
def __choose_native_classes(nativeElements):
    logger.log_header("Choosing Native elements")
    chosenNativeElements = SymbolClass("Chosen of Classes: ",
                                        ColorChooser().get_color())

    # Go through all symbols classes and choose the classes we want
    for i in range(0, len(nativeElements)):
        if (nativeElements[i].name in global_v.NATIVE_CLASSES or
                len(global_v.NATIVE_CLASSES) == 0):
            chosenNativeElements.learning_set += nativeElements[i].learning_set
            chosenNativeElements.test_set += nativeElements[i].test_set

            chosenNativeElements.name += str(nativeElements[i].name) + ", "

    # Log
    logger.log(str(chosenNativeElements))

    return chosenNativeElements

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

'''
    4) CLUSTER EVALUATION
    TODO: Add different algorithms
'''
def __compute_cluster_evaluation(nativeElements):
    logger.log_header("Cluster Evaluation")

    logger.log_header("Prediction Strength",
                        styles=[logger.LogHeaderStyle.SUB_HEADER])
    # Legacy function, requirs a list as input
    tmp_list = [nativeElements]
    best_k = ps.cluster_evaluation(global_v.MAX_K_CLUS_EVALUATION,
                                    tmp_list)

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
