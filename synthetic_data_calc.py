from elllipsoid import Ellipsoid
import util.global_variables as global_v
from sklearn.metrics.metrics import confusion_matrix
from foreign_rejector import ForeignRejector

radiuses = [1, 0.95, 0.90, 0.85, 0.80]

def ambiguity_for_different_radiuses(symbolClasses, foreignSymbols = []):
    #
    # PREPARE CONFUSION MATRIX
    #
    confusion_matrix = []
    for i in range(0, global_v.CLASS_NUM):
        class_data = []
        confusion_matrix.append(class_data)
        
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
        # Check for ambiguity for each class
        #
        print("\n        MEMBERSHIP RESULTS [LEARN SET]")   
        for i in range(0, len(symbolClasses)):
            learn_amb   = []
            learn_unamb = []
            learn_not_class = []
            test_amb    = [] 
            test_unamb  = []
            
            #
            # Learning set
            #
            for point in symbolClasses[i].learning_set:
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
                if(in_how_many == 1 and in_corrected):
                    learn_unamb.append(point)
                elif(in_how_many > 1 and in_corrected):
                    learn_amb.append(point)
                else:
                    learn_not_class.append(point) 
                    
            # Save results in confusion matrix
            confusion_matrix[i].append(round(100 * len(learn_unamb)/len(symbolClasses[i].learning_set), 2))
            confusion_matrix[i].append(round(100 * len(learn_amb)/len(symbolClasses[i].learning_set), 2))
            confusion_matrix[i].append(round(100 * len(learn_not_class)/len(symbolClasses[i].learning_set), 2))
            
            # Print out results  
            print("        >> Symbol:", [symbolClasses[i].name])
            print("           Unambiguous points:                            ",100 * len(learn_unamb)/len(symbolClasses[i].learning_set),"%")
            print("           Ambiguous points:                              ",100 * len(learn_amb)/len(symbolClasses[i].learning_set),"%")
            print("           Not Classified points:                         ",100 * len(learn_not_class)/len(symbolClasses[i].learning_set),"%")
                
        print()
        
        # TESTING FOREIGN AMBIGUITY
        foreign_stric_class, foreign_amb_count, foreign_rejected_count = ForeignRejector().
                                            accuracy_of_rejecting_matrix(foreignClasses, symbolClasses)
        
        
    # DISPLAY CONF MATRIX
    print("    CONFUSION MATRIX [LEARN SET]\n") 
    print(11 * " ", end ="")  
    for r in radiuses:
        print(r,14 * " ", end ="")
    print()       
    for i in range(0,len(confusion_matrix)):
        print("   ", [i], " ", end="")
        for value in confusion_matrix[i]:
            print(value," ", end ="")
        print()
        
def prepare_data(symbolClasses):
    returnArray = []
    for cl in symbolClasses:
        returnArray.append(cl.characteristicsValues)
    return returnArray