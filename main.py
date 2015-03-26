import util.global_variables as global_v
from plot_3d import Plot3D
from clusterer import Clusterer
from distorter import Distorter
from init_data_randomizer import InitDataRandomizer
from foreign_creator import ForeignCreator

# CREATE CHAR_NUM CHARACTERISTICS
print("*" * 10 , "Creating:", global_v.CHAR_NUM, "Characteristics", "*" * 10 )
characteristics = []
InitDataRandomizer().generate_characteristic(characteristics)

# CREATE CLASS_NUM SYMBOL CLASSES
print("*" * 10 , "Creating: ", global_v.CLASS_NUM, " Symbol Classes", "*" * 10 )
symbolClasses = []
InitDataRandomizer().generate_symbol_classes(symbolClasses, characteristics)

# DISTORTION
print("*" * 10 , "Computing Distortion", "*" * 10 )
Distorter().create_cloud(symbolClasses[:])

# CLUSTERING
print("*" * 10 , "Computing Clusters", "*" * 10 )
Clusterer().computeClusters(symbolClasses[:global_v.CLASS_DISPLAY_NUM])

print("*" * 10 , "Displaying Plot", "*" * 10 )
Plot3D().renderPlot(symbolClasses[:global_v.CLASS_DISPLAY_NUM])
################################
### Generate Foreign classes ###
foreignClasses = []
foreignClasses = ForeignCreator().createForeignClass(global_v.CLASS_NUM * global_v.N,
                                  symbolClasses, characteristics)
#for i in range(0,N):

################################