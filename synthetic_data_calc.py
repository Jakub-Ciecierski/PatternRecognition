from elllipsoid import Ellipsoid
import util.global_variables as global_v

radiuses = [1, 0.95, 0.90, 0.85, 0.80]

def ambiguity_for_different_radiuses(symbolClasses):
    for radius in radiuses:
        print("    RADIUS:", radius)
        #
        # Shrink each ellipsoid
        #
        print("        SHRINKING ELLIPSOIDS IN EACH CLUSTER")
        for cl in symbolClasses:
            for cluster in cl.clusters:
                # Check if there is need to recalculate
                if(radius != global_v.SEMI_AXIS_SCALE):
                    cluster.ellipsoid = Ellipsoid(cluster.points,radius)
                    
                # list of point in current ellipsoid
                pointsInEllipsoid = cluster.ellipsoid.is_point_in_ellipsoid(cluster.points,False, True)
                print("           Symbol:",[cl.name]," Points in cluster:                ", 100 * len(pointsInEllipsoid)/len(cluster.points),"%")

        
        #
        # Check for ambiguity for each class
        #
        print("        MEMBERSHIP RESULTS")   
        for cl in symbolClasses:
            learn_amb   = []
            learn_unamb = []
            learn_not_class = []
            test_amb    = [] 
            test_unamb  = []
            
            #
            # Learning set
            #
            for point in cl.learning_set:
                # Count of clusters to which point belongs
                in_how_many = 0
                # Does point belong to the right one ?
                in_corrected = False
                
                for cl_check in symbolClasses:
                    for check_cluster in cl_check.clusters:
                        rejected = check_cluster.ellipsoid.is_point_in_ellipsoid([point.characteristicsValues[:]], True)
                        if(rejected == 0):
                            in_how_many += 1
                            if(cl.name == cl_check.name):
                                in_corrected = True
                            break
       
                # Based on information we decide to which group assign our point
                if(in_how_many == 1 and in_corrected):
                    learn_unamb.append(point)
                elif(in_how_many > 1 and in_corrected):
                    learn_amb.append(point)
                else:
                    learn_not_class.append(point)   
            print("        >> Symbol:", [cl.name])
            print("           Unambiguous points:                            ",100 * len(learn_unamb)/len(cl.learning_set),"%")
            print("           Ambiguous points:                              ",100 * len(learn_amb)/len(cl.learning_set),"%")
            print("           Not Classified points:                         ",100 * len(learn_not_class)/len(cl.learning_set),"%")

        print()

def prepare_data(symbolClasses):
    returnArray = []
    for cl in symbolClasses:
        returnArray.append(cl.characteristicsValues)
    return returnArray