import util.console as console
import sys
import util.global_variables 
import data_calculations.synthetic_data_calc as synth_calc
from gui.plot_3d import Plot3D
from clustering.clusterer import Clusterer
from data_calculations.distorter import Distorter
import data_calculations.data_manager as data
import symbols.foreign_creator as f_creator
import util.loader as loader
import clustering.prediction_strength as ps
import data_calculations.matrices_batch as mb
from data_calculations.basic_membership import BasicMembership



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
    Distorter().create_k_clouds(util.global_variables.K_CLOUD_DISTORTION,symbolClasses)
    #Distorter().create_non_homogeneus_cloud(symbolClasses)
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
    '''
    for c in range(0, util.global_variables.CLASS_NUM):
        console.write_header("Computing Cluster Evaluation")
        best_k = ps.cluster_evaluation(util.global_variables.MAX_K_CLUS_EVALUATION, symbolClasses[c:c+1])
        console.write_header("Computing Clusters with K:", str(util.global_variables.K))
	'''
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
     
    for i in range(0,5):
        # Check foreign
        membership.check_foreign_ellipsoid(foreignClassesHomo)
        membership.check_foreign_ellipsoid(foreignClassesNonHomo)
        membership.check_foreign_cuboids(foreignClassesHomo)
        membership.check_foreign_cuboids(foreignClassesNonHomo)
        # Shrink
        if(i != 4):
            membership.shrink_ellipsoids(5)
            membership.shrink_cuboids(5)
            print("        >> Number of points per ellipsoid after shrinking:", len(membership.ellipsoids[0].points))
            print("        >> Number of points per cuboid after shrinking:", len(membership.cuboids[0].points))
            membership.recalculate_ellipsoids()
            membership.recalculate_cuboids()    
    
    
    
def semisynthetic_test_paper_1():
    print("semi_test") 
