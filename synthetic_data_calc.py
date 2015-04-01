from elllipsoid import Ellipsoid
import util.global_variables as global_v
import matrices_batch
from sklearn.metrics.metrics import confusion_matrix
from matrices_batch import MatricesBatch, DataInfo
from results_data import ResultsData
from foreign_rejector import ForeignRejector

radiuses = [1, 0.95, 0.90, 0.85, 0.80]
results_data = ResultsData(len(radiuses))

def ambiguity_for_different_radiuses(symbolClasses, foreignClassesHomo = [], foreignClassesNonHomo = []):

    for r in range(0,len(radiuses)):
        print("    RADIUS:", radiuses[r])
        #
        # Shrink each ellipsoid
        #
        print("        SHRINKING ELLIPSOIDS IN EACH CLUSTER")
        for cl in symbolClasses:
            for cluster in cl.clusters:
                # Check if there is need to recalculate
                if(radiuses[r] != global_v.SEMI_AXIS_SCALE):
                    cluster.ellipsoid = Ellipsoid(cluster.points,radiuses[r])
                    
                # list of point in current ellipsoid
                pointsInEllipsoid = cluster.ellipsoid.is_point_in_ellipsoid(cluster.points,False, True)
                print("           Symbol:",[cl.name]," Points in cluster:                ", 100 * len(pointsInEllipsoid)/len(cluster.points),"%")

        
        #
        # [LERN SET] Check for ambiguity for each class
        #
        # LEARNING SET
        print("\n        MEMBERSHIP RESULTS [LEARN SET]")   
        ambiguity_test(DataInfo.LEARN, r, symbolClasses)
        print("\n        MEMBERSHIP RESULTS [TEST SET]")   
        ambiguity_test(DataInfo.TEST, r, symbolClasses)
        
        #
        # Check ambiguity for each foreign set
        #
        print("\n\n        MEMBERSHIP RESULTS [HOMOGENEOUS FOREIGN SET]")
        foreign_ambiguity_test(foreignClassesHomo, symbolClasses)
        print("\n\n        MEMBERSHIP RESULTS [NON HOMOGENEOUS FOREIGN SET]")
        foreign_ambiguity_test(foreignClassesNonHomo, symbolClasses)

def ambiguity_test(set_type, radius, symbolClasses):
    for i in range(0, len(symbolClasses)):
        if(set_type == DataInfo.LEARN):
            set_to_test = symbolClasses[i].learning_set
        if(set_type == DataInfo.TEST):
            set_to_test = symbolClasses[i].test_set
            
        for point in set_to_test:
            # Count of clusters to which point belongs
            in_how_many = 0
            # Does point belong to the right one ?
            in_corrected = False
            
            for cl_check in symbolClasses:
                for check_cluster in cl_check.clusters:
                    rejected = check_cluster.ellipsoid.is_point_in_ellipsoid([point.characteristicsValues[:]], True)
                    if(rejected == 0):
                        in_how_many += 1
                        if(symbolClasses[i].name == cl_check.name):
                            in_corrected = True
                        break
   
            # Based on information we decide to which group assign our point
            group_assigment(radius, i, in_how_many, in_corrected, set_type)
        
        # Print out results  
        results_data.batch(radius).summarization(i, set_type, DataInfo.BASIC)  

def group_assigment(radius, class_n, in_how_many, in_corrected, set_type):
    if(in_how_many == 1 and in_corrected):
        results_data.batch(radius).data(1, class_n, DataInfo.SAVE, set_type, DataInfo.BASIC, 
                 DataInfo.NATIVE_CLASS, class_n)
    elif(in_how_many > 1 and in_corrected):
        results_data.batch(radius).data(1, class_n, DataInfo.SAVE, DataInfo.LEARN, DataInfo.BASIC, 
                 DataInfo.AMB)
    else:
        results_data.batch(radius).data(1, class_n, DataInfo.SAVE, DataInfo.LEARN, DataInfo.BASIC, 
                 DataInfo.NOT_CLASS)

def foreign_ambiguity_test(foreignClasses, symbolClasses):
    f_nonhomo_stric_class, f_nonhomo_amb_count, f_nonhomo_rejected_count = ForeignRejector().accuracy_of_rejecting_matrix(foreignClasses, symbolClasses)
    print("\n\n        MEMBERSHIP RESULTS [NON HOMOGENEOUS FOREIGN SET]")
    for f in range(0, len(f_nonhomo_stric_class)):
        print("        >> Symbol[",f,"]:                " , (f_nonhomo_stric_class[f] / len(foreignClasses))*100, "%")
    print("        >> Ambiguous:                    " , (f_nonhomo_amb_count / len(foreignClasses))*100, "%")
    print("        >> Rejected:                     " , (f_nonhomo_rejected_count / len(foreignClasses))*100, "% \n")