import random
from characteristic import Characteristic
from symbol_class import SymbolClass
from color_chooser import ColorChooser
from plot_3d import Plot
from clusterer import Clusterer
from distorter import Distorter

# CREATE M CHARACTERISTICS
M = 3
print("*" * 10 , "Creating: ", M, " Characteristics", "*" * 10 )
characteristics = []
for i in range(0,M):
    characteristics.append(Characteristic())
    print("Characterestic #",i,"Interval: From:",characteristics[i].interval.lowerBound,
                        "To:",characteristics[i].interval.upperBound)

# CREATE classCount SYMBOL CLASSES
classCount = 10
print("*" * 10 , "Creating: ", classCount, " Symbol Classes", "*" * 10 )
symbolClasses = []
colorChooser = ColorChooser()
for i in range(0,classCount):
    # Store newly created symbol class in the list
    symbolClasses.append(SymbolClass(i, colorChooser.getColor()))
    # Randomize value for each characteristic of the symbol
    for j in range(0,len(characteristics)):
        symbolClasses[i].characteristicsValues.append(
            random.uniform(characteristics[j].interval.lowerBound, 
                           characteristics[j].interval.upperBound))

# INFO
for i in range(0,len(symbolClasses)):
    print("Symbol Class:",symbolClasses[i].name, "\n",
          "Characteristics: ", symbolClasses[i].characteristicsValues, "\n")
    

#DISTORTION
print("*" * 10 , "Computing Distortion", "*" * 10 )
N = 100
Distorter(N).create_cloud(symbolClasses[:])

############################
# Clustering
print("*" * 10 , "Computing Clusters", "*" * 10 )
plot = Plot()
clusterer = Clusterer()
MAX_K = 5
for k in range(MAX_K,MAX_K + 1):
    print("Clusters [k]:", k)
    clusterer.computeClusters(k, symbolClasses[:2])
##############################

# DISPLAY    
plot.showAllClusters(symbolClasses[:2])

