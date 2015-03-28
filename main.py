import util.global_variables as global_v
import console_writer as console
from plot_3d import Plot3D
from clusterer import Clusterer
from distorter import Distorter
import data_manager as data
from foreign_creator import ForeignCreator
from foreign_rejector import ForeignRejector
from loader.xsl_loader import XslLoader

# CREATE CHAR_NUM CHARACTERISTICS
console.write_header("Creating Characteristics")
characteristics = []
data.generate_characteristic(characteristics)

# CREATE CLASS_NUM SYMBOL CLASSES
console.write_header(" Creating Symbol Classes")
symbolClasses = []
data.generate_symbol_classes(symbolClasses, characteristics)

# DISTORTION
console.write_header("Computing Distortion")
Distorter().create_cloud(symbolClasses[:])

# READ XSL FILE
#print("*" * 10 , "Loading from sample", "*" * 10 )
#loader =  XslLoader('test_samples\Test_set.xls', 3)
#symbolClasses = loader.read_symbols()

# CLUSTERING
console.write_header("Computing Clusters")
Clusterer().computeClusters(symbolClasses[:global_v.CLASS_NUM])
#Clusterer().computeClusters(symbolClasses)

# TEST SET CHECK
console.write_header(" Checking Test Set")
data.cluster_membership_test(symbolClasses[:global_v.CLASS_NUM])
#data.cluster_membership_test(symbolClasses)

# DISPLAY
console.write_header(" Displaying Plot")
Plot3D().renderPlot(symbolClasses[:global_v.CLASS_NUM])
#Plot3D().renderPlot(symbolClasses)

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