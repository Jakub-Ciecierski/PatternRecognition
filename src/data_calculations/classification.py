import util.logger as logger
import util.progress_bar as p_bar
import sys

'''
    Geometry classification
'''
CLASSIFY_ELLIPSOID = 0
CLASSIFY_CUBOID = 1

"""
    Computes classification for Native symbols.
    Classification of Testing symbols are checked against
    clusters of Training symbols.
"""
def compute_training_vs_testing(nativeElements, classify_geometry):
    # Classification counters
    total_count = 0
    belongs_count = 0

    # Print string
    if classify_geometry == CLASSIFY_ELLIPSOID:
        which_classifier_str = "Classification with Ellipsoids"
    elif classify_geometry == CLASSIFY_CUBOID:
        which_classifier_str = "Classification with Cuboids"

    # Progress Bar
    p_bar.init(len(nativeElements.test_set),
                "Training vs Testing: " + which_classifier_str)

    # Classification
    for test_symbol in nativeElements.test_set:
        if _belongs_to_native(test_symbol, nativeElements, classify_geometry):
            belongs_count += 1
        total_count += 1

        p_bar.update()

    # Results
    TP = (belongs_count / total_count ) * 100
    FN = 100 - TP

    TPstr = "True Positive (TP) = " + str(round(TP,2)) + "%" + "(" + str(belongs_count) +"/" +str(total_count) + ")"
    FNstr = "False Negative (FN) = " + str(round(FN,2)) + "%" + "(" + str(total_count - belongs_count) +"/" + str(total_count) + ")"

    logger.log(which_classifier_str)
    logger.log(TPstr)
    logger.log(FNstr)

    p_bar.finish()

    return TP, FN

"""
    Computes classification for Foreign elements.
    Classification of Forein symbols are checked against
    clusters of Native Training symbols.
"""
def compute_native_vs_foreign(nativeElements, foreignElements, classify_geometry):
    total_count = 0
    rejected_count = 0

    # Print string
    if classify_geometry == CLASSIFY_ELLIPSOID:
        which_classifier_str = "Classification with Ellipsoids"
    elif classify_geometry == CLASSIFY_CUBOID:
        which_classifier_str = "Classification with Cuboids"

    # Progress Bar
    p_bar.init(len(foreignElements),
                "Native vs Foreign: " + which_classifier_str)

    for foreign in foreignElements:
        if not _belongs_to_native(foreign, nativeElements, classify_geometry):
            rejected_count += 1
        total_count += 1

        p_bar.update()

    TN = (rejected_count / total_count) * 100
    FP = 100 - TN

    TNstr = "True Negatives (TN) = " + str(round(TN, 2)) + "%" + "(" + str(rejected_count )+"/"+ str(total_count) + ") \n"
    FPstr = "False Positives (FP) = " + str(round(FP, 2)) + "%" + "(" + str(total_count - rejected_count)+"/"+str(total_count) + ") \n"

    logger.log(which_classifier_str)
    logger.log(TNstr)
    logger.log(FPstr)

    p_bar.finish()

    return TN, FP

"""
    Computes Accuracy, Sensitivity, Precision and F-Measure
"""
def compute_measurements(TP, FN, TN, FP):
    accuracy = (TP + TN) / (TP + FN + FP + TN)

    sensitivity = TP / (TP + FN)

    precision = TP / (TP + FP)

    f_measure = 2 * ((precision * sensitivity) / (precision + sensitivity))

    return accuracy, sensitivity, precision, f_measure

"""
    Returns true if point belongs to native symbols.
    False otherwise.

    classify_geometry determines wheter CLASSIFY_ELLIPSOID
    or CLASSIFY_CUBOID should be used.
"""
def _belongs_to_native(point, nativeElements, classify_geometry):
    if classify_geometry == CLASSIFY_CUBOID:
        return _belongs_to_cuboid(point, nativeElements)
    elif classify_geometry == CLASSIFY_ELLIPSOID:
        return _belongs_to_ellipsoid(point, nativeElements)
    else:
        logger.log("No such test, shutting down...")
        sys.exit()

"""
    Returns true if point belongs to native symbols.
    Ellipsoid classification is used.
    False other wise
"""
def _belongs_to_ellipsoid(point, nativeElements):
    for cluster in nativeElements.clusters:
        if cluster.ellipsoid.is_point_in_ellipsoid([point.characteristicsValues[:]], True) == 0:
            return True
    return False

"""
    Returns true if point belongs to native symbols.
    Cuboid classification is used.
    False other wise
"""
def _belongs_to_cuboid(point, nativeElements):
    for cluster in nativeElements.clusters:
        if cluster.cuboid.is_point_in_cuboid(point.characteristicsValues[:]):
            return True
    return False
