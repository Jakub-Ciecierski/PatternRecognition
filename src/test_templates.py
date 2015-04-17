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
    
    for c in range(0, util.global_variables.CLASS_NUM):
        console.write_header("Computing Cluster Evaluation")
        best_k = ps.cluster_evaluation(util.global_variables.MAX_K_CLUS_EVALUATION, symbolClasses[c:c+1])
        console.write_header("Computing Clusters with K:", str(util.global_variables.K))
        Clusterer().computeClusters(symbolClasses[c:c+1])
        
    console.write_header(" Synthetic Data Calculations")
    synth_calc.ambiguity_for_different_radiuses_real_data(symbolClasses[:], foreignClasses)