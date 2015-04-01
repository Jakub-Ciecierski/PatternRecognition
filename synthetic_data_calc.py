from elllipsoid import Ellipsoid
import util.global_variables as global_v
import matrices_batch
from sklearn.metrics.metrics import confusion_matrix
from matrices_batch import MatricesBatch, DataInfo

radiuses = [1, 0.95, 0.90, 0.85, 0.80]

def ambiguity_for_different_radiuses(symbolClasses):

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
        print("\n        MEMBERSHIP RESULTS [LEARN SET]")   
        m_batch = MatricesBatch()
        for i in range(0, len(symbolClasses)):
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
                    m_batch.data(1, i, DataInfo.SAVE, DataInfo.LEARN, DataInfo.BASIC, 
                                 DataInfo.NATIVE_CLASS, i)
                elif(in_how_many > 1 and in_corrected):
                    m_batch.data(1, i, DataInfo.SAVE, DataInfo.LEARN, DataInfo.BASIC, 
                                 DataInfo.AMB)
                else:
                    m_batch.data(1, i, DataInfo.SAVE, DataInfo.LEARN, DataInfo.BASIC, 
                                 DataInfo.NOT_CLASS)
            
            # Print out results  
            m_batch.summarization(i, DataInfo.LEARN, DataInfo.BASIC)    

        m_batch.print_matrix(DataInfo.LEARN, DataInfo.BASIC)    
        print()
    
    # DISPLAY CONF MATRIX
    
def prepare_data(symbolClasses):
    returnArray = []
    for cl in symbolClasses:
        returnArray.append(cl.characteristicsValues)
    return returnArray