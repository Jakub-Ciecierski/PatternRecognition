import util.global_variables as global_v
import console as console
import synthetic_data_calc as synth_calc
from plot_3d import Plot3D
from clusterer import Clusterer
from distorter import Distorter
import data_manager as data
import sys
from foreign_creator import ForeignCreator
from foreign_rejector import ForeignRejector
from loader.xsl_loader import XslLoader

# CHECK ARGUMENTS
console.parse_argv(sys.argv[1:])

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

# READ XSL FILE
#print("*" * 10 , "Loading from sample", "*" * 10 )
#loader =  XslLoader('test_samples\Test_set.xls', 3)
#symbolClasses = loader.read_symbols()

# CLUSTERING
console.write_header("Computing Clusters")
Clusterer().computeClusters(symbolClasses[:global_v.CLASS_NUM])

# TEST SET CHECK
console.write_header(" Checking Test Set")
data.cluster_membership_test(symbolClasses[:global_v.CLASS_NUM])
#data.cluster_membership_test(symbolClasses)

# DISPLAY
console.write_header(" Displaying Plot")
Plot3D().renderPlot(symbolClasses[:global_v.CLASS_NUM])
#Plot3D().renderPlot(symbolClasses)

# SYNTETIC DATA CALCULATIONS
console.write_header(" Synthetic Data Calculations")
synth_calc.ambiguity_for_different_radiuses(symbolClasses[:])

# GENERATING FOREIGN CLASSES
console.write_header("Generating Foreign classes")
foreignClasses = []
foreignClasses = ForeignCreator().createForeignClass(global_v.CLASS_NUM * (global_v.N_LEARNING + global_v.N_TEST),
                                  symbolClasses, characteristics)

# TESTING ACCURACY OF REJECTING FOREIGN CLASSES
console.write_header(" Testing accuracy of rejecting Foreign classes")
ForeignRejector().accuracy_of_rejecting(foreignClasses , symbolClasses)

# print("*" * 10 , "Displaying Plot with Foreign symbols", "*" * 10 )
Plot3D().renderPlot(symbolClasses, foreignClasses)