import random
from characteristic import Characteristic
from symbol_class import SymbolClass
from color_chooser import ColorChooser
from cluster import Cluster
from plot_3d import Plot
import numpy as np
from clusterer import Clusterer
from distorter import Distorter
from random import Random

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


for i in range(0,len(symbolClasses)):
    print("Symbol Class:",symbolClasses[i].name, "\n",
          "Characteristics: ", symbolClasses[i].characteristicsValues, "\n")
    

#DISTORTION
print("*" * 10 , "Computing Distortion", "*" * 10 )
N = 100
distortedClasses = Distorter(N).create_cloud(symbolClasses[:])

############################
# Clustering
print("*" * 10 , "Computing Clusters", "*" * 10 )
plot = Plot()
clusterer = Clusterer()
MAX_K = 5
for k in range(5,MAX_K + 1):
    centroidsOfAllClasses = []
    labelsOfAllClasses = []
    print("Clusters [k]:", k)

    # old method to check if the new method is correct
    centroidsOfAllClasses, labelsOfAllClasses = clusterer.computeClusters(distortedClasses, k, classCount, N)
     
    # new aproach
    clusterer.computeClustersOfSymbols(k, symbolClasses, distortedClasses, N)

    # show plot for each class
   
    for i in range(0,classCount):
        plot.show2(centroidsOfAllClasses[k*i:k+k*i],labelsOfAllClasses[k*i:k+k*i], distortedClasses[i*N:(N+N*i)], 
                   1, ("Clusters [k] :", k))
#         plot.show2(centroidsOfAllClasses[k*i:k+k*i],labelsOfAllClasses[k*i:k+k*i], distortedClasses[i*N:(N+N*i)], 
    # show plot for all classes
    plot.showAllClusters(symbolClasses)
#     plot.show2(centroidsOfAllClasses,labelsOfAllClasses, distortedClasses, classCount)
