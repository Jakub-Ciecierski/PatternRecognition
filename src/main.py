import util.global_variables as global_v
import util.console as console
import data_calculations.synthetic_data_calc as synth_calc
from gui.plot_3d import Plot3D
from clustering.clusterer import Clusterer
from data_calculations.distorter import Distorter
import data_calculations.data_manager as data
import sys
import symbols.foreign_creator as f_creator
import util.loader as loader
import clustering.prediction_strength as ps

# READ XSL FILE
#print("*" * 10 , "Loading from sample", "*" * 10 )
#loader =  XslLoader('test_samples\Test_set.xls', 3)
#symbolClasses = loader.read_symbols()

# CHECK ARGUMENTS
console.parse_argv(sys.argv[1:])

# REDIRECT OUTPUT
if global_v.REDIRECT_TO_FILE:
    console.redirect_stdout()

console.write_header("Run configuration")
console.print_config()

# CREATE CHAR_NUM CHARACTERISTICS
console.write_header("Creating Characteristics")
characteristics = []
data.generate_characteristic(characteristics)

# CREATE CLASS_NUM SYMBOL CLASSES
console.write_header(" Creating Symbol Classes")
symbolClasses = []
data.generate_symbol_classes(symbolClasses, characteristics)

# DISTORTIONS
if(global_v.NON_HOMO_CLASSES):
    console.write_header("Computing Non-Homogeneus Distortion")
    Distorter().create_non_homogeneus_cloud(symbolClasses[:])
else:
    console.write_header("Computing Homogeneus Distortion")
    Distorter().create_homogeneus_cloud(symbolClasses[:])

#console.write_header("Creating 2-cloud Distortion")
#Distorter().create_k_clouds(2,symbolClasses[:])

#console.write_header("Loading from sample")
#symbolClasses = loader.load_xsl('test_samples\Test_set.xls', 0, 3)
#symbolClasses = loader.load_txt('test_samples\native1.txt')

# Print symbol classes to save the generated symbols
if(global_v.PRINT_GENERATED_SYMBOLS):
    console.write_header("Printing generated Distortions")
    console.print_symbols(symbolClasses)

# Generating Foreign classes
console.write_header("Creating Non Homogeneous Foreign")
foreignClassesNonHomo = f_creator.create_non_homogeneous_foreign(symbolClasses)
console.write_header("Creating Homogeneous Foreign")
foreignClassesHomo = f_creator.create_homogeneous_foreign(symbolClasses, characteristics)

# CLUSTERING
console.write_header("Computing Clusters")
Clusterer().computeClusters(symbolClasses[:global_v.CLASS_NUM])

# CLUSTER EVALUATION
console.write_header("Evaluating clustering")
ps.cluster_evaluation(global_v.MAX_K_CLUS_EVALUATION, symbolClasses)

# TEST SET CHECK
console.write_header(" Checking Test Set")
data.cluster_membership_test(symbolClasses[:global_v.CLASS_NUM])
#data.cluster_membership_test(symbolClasses)

# DISPLAY
#console.write_header(" Displaying Plot")
#Plot3D().renderPlot(symbolClasses[:global_v.CLASS_NUM])
#Plot3D().renderPlot(symbolClasses)

# SYNTETIC DATA CALCULATIONS
console.write_header(" Synthetic Data Calculations")
synth_calc.ambiguity_for_different_radiuses(symbolClasses[:], foreignClassesHomo, foreignClassesNonHomo)

#console.write_header("Displaying plot with Non Homogeneous Foreign symbols")
#Plot3D().renderPlot(symbolClasses, foreignClassesNonHomo)

#console.write_header("Displaying plot with Homogeneous Foreign symbols")
#Plot3D().renderPlot(symbolClasses, foreignClassesHomo)