from clustering.elllipsoid import Ellipsoid
import util.global_variables as global_v
import numpy as np
from data_calculations.matrices_batch import DataInfo
from data_calculations.results_data import ResultsData
import data_calculations.foreign_rejector as f_rej
import os

radiuses = [1, 0.95, 0.90, 0.85, 0.80]
results_data = ResultsData(radiuses)

def ambiguity_for_different_radiuses(symbolClasses, foreignClassesHomo= [], foreignClassesNonHomo= []):

    for r in range(0,len(radiuses)):
        print("    RADIUS:", radiuses[r])
        
        #
        # Shrink each ellipsoid
        #
        path = os.path.join("..","log",global_v.DIR_NAME,"r"+str(radiuses[r]))
        os.makedirs(path, exist_ok=True)
        file = open(os.path.join(path,"r" + str(radiuses[r])+"_shrinking.txt"), 'a')  
        print("        SHRINKING ELLIPSOIDS IN EACH CLUSTER")
        for cl in symbolClasses:
            for cluster in cl.clusters:
                # Check if there is need to recalculate
                if(radiuses[r] != global_v.SEMI_AXIS_SCALE):
                    cluster.ellipsoid = Ellipsoid(cluster.points,radiuses[r])
                    
                # list of point in current ellipsoid
                pointsInEllipsoid = cluster.ellipsoid.is_point_in_ellipsoid(cluster.points,False, True)
                print("           Symbol:",[cl.name]," Points in cluster:                ", 100 * len(pointsInEllipsoid)/len(cluster.points),"%")
                file.write("Symbol:" + str([cl.name]) + " Points in cluster:                "+ str(100 * len(pointsInEllipsoid)/len(cluster.points))+"%\n")
        file.close()
                
        #
        # TESTS FOR DIFFERENT SETS
        #
        print("\n        MEMBERSHIP RESULTS [LEARN SET]")   
        ambiguity_test(DataInfo.LEARN, r, symbolClasses)
        print("\n        MEMBERSHIP RESULTS [TEST SET]")   
        ambiguity_test(DataInfo.TEST, r, symbolClasses)

        #
        # Check ambiguity for each foreign set
        #
        print("\n\n        MEMBERSHIP RESULTS [FOREIGN HOMO]")
        foreign_ambiguity_test(DataInfo.HOMO, r, foreignClassesHomo, symbolClasses)
        results_data.batch(r).print_matrix(DataInfo.FOREIGN, DataInfo.HOMO)
        print("\n\n        MEMBERSHIP RESULTS [FOREIGN NON-HOMO]")
        foreign_ambiguity_test(DataInfo.NONHOMO, r, foreignClassesNonHomo, symbolClasses)
        results_data.batch(r).print_matrix(DataInfo.FOREIGN, DataInfo.NONHOMO)

'''
    TODO
'''
def ambiguity_test(set_type, radius, symbolClasses):
    for i in range(0, len(symbolClasses)):
        if(set_type == DataInfo.LEARN):
            set_to_test = symbolClasses[i].learning_set
        if(set_type == DataInfo.TEST):
            set_to_test = symbolClasses[i].test_set
            
        for point in set_to_test:
            # Does point belong to the right one ?
            in_corrected = False
            ambiguous_ellipsoids =[]
            
            for cl_check in symbolClasses:
                for check_cluster in cl_check.clusters:
                    rejected = check_cluster.ellipsoid.is_point_in_ellipsoid([point.characteristicsValues[:]], True)
                    if(rejected == 0):
                        ambiguous_ellipsoids.append(EuclidianData(int(cl_check.name), check_cluster.ellipsoid.center))
                        if(symbolClasses[i].name == cl_check.name):
                            in_corrected = True
                        
   
            # Based on information we decide to which group assign our point
            group_assigment(radius, i,DataInfo.BASIC, ambiguous_ellipsoids, in_corrected, set_type, point.characteristicsValues[:])
            group_assigment(radius, i,DataInfo.EUCL, ambiguous_ellipsoids, in_corrected, set_type,point.characteristicsValues[:])
        
        # Print out results  
        results_data.batch(radius).summarization(i, set_type, DataInfo.BASIC) 
         
    results_data.batch(radius).print_matrix(set_type, DataInfo.BASIC)
    results_data.batch(radius).print_matrix(set_type, DataInfo.EUCL)    
'''
    TODO
'''
def group_assigment(radius, class_n,m_type , ambiguous_ellipsoids, in_corrected, set_type, point):
    if(len(ambiguous_ellipsoids) == 1 and in_corrected):
        results_data.batch(radius).data(1, class_n, DataInfo.SAVE, set_type, m_type, 
                 DataInfo.NATIVE_CLASS, class_n)
    elif(len(ambiguous_ellipsoids) > 1 and in_corrected):
        if(m_type == DataInfo.BASIC):
            results_data.batch(radius).data(1, class_n, DataInfo.SAVE, set_type, m_type, 
                     DataInfo.AMB)
        elif(m_type == DataInfo.EUCL):
            closest_center_class = determine_closer_ellipsoid(ambiguous_ellipsoids, point)
            results_data.batch(radius).data(1, class_n, DataInfo.SAVE, set_type, m_type, 
                 DataInfo.NATIVE_CLASS, closest_center_class)
    else:
        results_data.batch(radius).data(1, class_n, DataInfo.SAVE, set_type, m_type, 
                 DataInfo.NOT_CLASS)
'''
    TODO
'''
class EuclidianData:
    def __init__(self, class_n, ellipsoid_center):
        self.class_n = class_n
        self.ellipsoid_center = ellipsoid_center
        
'''
    TODO
'''
def euclidian_distance(point1, point2):
    result = 0
    for i in range(0, len(point1)):
        result += np.power((point1[i]-point2[i]), 2)
    return np.sqrt(result)

'''
    TODO
'''
def determine_closer_ellipsoid(ambiguous_ellipsoids, point):
    closest = 500
    return_class = ambiguous_ellipsoids[0].class_n
    for ellipsoid in ambiguous_ellipsoids:
        tmp = euclidian_distance(point, ellipsoid.ellipsoid_center)
        if(tmp < closest):
            closest = tmp
            return_class = ellipsoid.class_n

    return return_class

'''
    Process of ambiguity test for foreign symbols.
'''
def foreign_ambiguity_test(m_type, radius, foreignClasses, symbolClasses):
    # compute Strict classification, ambiguous count, and rejection count
    stric_class, amb_count, rejected_count = f_rej.accuracy_of_rejecting_confusion(foreignClasses, symbolClasses)

    # safe results to batch
    results_data.batch(radius).data(amb_count, 0, DataInfo.SAVE, DataInfo.FOREIGN, m_type, 
                     DataInfo.AMB)
    results_data.batch(radius).data(rejected_count, 0, DataInfo.SAVE, DataInfo.FOREIGN, m_type, 
                     DataInfo.NOT_CLASS)
    for i in range(0, len(stric_class)):
        results_data.batch(radius).data(stric_class[i], 0, DataInfo.SAVE, DataInfo.FOREIGN, m_type, 
                     DataInfo.NATIVE_CLASS, i)

    # If directory is not existing - create it. Next, save results to file.
    path = os.path.join("..","log",global_v.DIR_NAME,"r"+str(radiuses[radius]))
    os.makedirs(path, exist_ok=True)
    file = open(os.path.join(path,"r" + str(radius)+"_"+str(m_type.name)+"_summary.txt"), 'a')
    for f in range(0, len(stric_class)):
        results_data.batch(radius).double_print(">> Symbol["+str(f)+"]:                " , (stric_class[f] / len(foreignClasses))*100,file)
    results_data.batch(radius).double_print(">> Ambiguous:                " , (amb_count / len(foreignClasses))*100,file)
    results_data.batch(radius).double_print(">> Rejected:                " , (rejected_count / len(foreignClasses))*100,file)
    file.close()