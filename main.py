import util.global_variables as global_v
from plot_3d import Plot3D
from clusterer import Clusterer
from distorter import Distorter
import data_manager as data
from foreign_creator import ForeignCreator
from foreign_rejector import ForeignRejector
from loader.xsl_loader import XslLoader

# CREATE CHAR_NUM CHARACTERISTICS
print("*" * 10 , "Creating:", global_v.CHAR_NUM, "Characteristics", "*" * 10 )
characteristics = []
data.generate_characteristic(characteristics)

# CREATE CLASS_NUM SYMBOL CLASSES
print("*" * 10 , "Creating: ", global_v.CLASS_NUM, " Symbol Classes", "*" * 10 )
symbolClasses = []
data.generate_symbol_classes(symbolClasses, characteristics)

# DISTORTION
print("*" * 10 , "Computing Distortion", "*" * 10 )
Distorter().create_cloud(symbolClasses[:])

# Read from file
#print("*" * 10 , "Loading from sample", "*" * 10 )
#loader =  XslLoader('test_samples\Test_set.xls', 3)
#symbolClasses = loader.read_symbols()

# CLUSTERING
print("*" * 10 , "Computing Clusters", "*" * 10 )
Clusterer().computeClusters(symbolClasses[:global_v.CLASS_NUM])
#Clusterer().computeClusters(symbolClasses)

# TEST SET CHECK
print("*" * 10 , "Checking Test Set", "*" * 10 )
data.cluster_membership_test(symbolClasses[:global_v.CLASS_NUM])
#data.cluster_membership_test(symbolClasses)

# DISPLAY
print("*" * 10 , "Displaying Plot", "*" * 10 )
#Plot3D().renderPlot(symbolClasses[:global_v.CLASS_DISPLAY_NUM])
#Plot3D().renderPlot(symbolClasses)

# GENERATING FOREIGN CLASSES
print("*" * 10 , "Generating Foreign classes" ,"*" * 10 )
foreignClasses = []
foreignClasses = ForeignCreator().createForeignClass(global_v.CLASS_NUM * (global_v.N_LEARNING + global_v.N_TEST),
                                  symbolClasses, characteristics)

# TESTING ACCURACY OF REJECTING FOREIGN CLASSES
print("*" * 10 , "Testing accuracy of rejecting Foreign classes:" ,"*" * 10 )
ForeignRejector().accuracy_of_rejecting(foreignClasses , symbolClasses)

print("*" * 10 , "Displaying Plot with Foreign symbols", "*" * 10 )
Plot3D().renderPlot(symbolClasses, foreignClasses)