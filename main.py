import random
from characteristic import Characteristic
from symbol_class import SymbolClass
from color_chooser import ColorChooser
from plot_3d import Plot
import numpy as np
from cluster import computeCluster
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


for i in range(0,len(symbolClasses)):
    print("Symbol Class:",symbolClasses[i].name, "\n",
          "Characteristics: ", symbolClasses[i].characteristicsValues, "\n")
    

''' DISTORTION '''
print("*" * 10 , "Computing Distortion", "*" * 10 )
N = 100
distortedClasses = []
distorter = Distorter()
for cl in symbolClasses[:]:
    for i in range(0, N):
        distortedClass = SymbolClass(cl.name, cl.color)
        distortedClass.characteristicsValues = distorter.generateDistortion(cl.characteristicsValues[:])
        distortedClasses.append(distortedClass)

''' END OF DISTORTION '''

# for i in range(0, len(distortedClasses)):
#     print(distortedClasses[i].characteristicsValues)


############################
# Clustering
k = 3

plot = Plot()
# test for one class distortion
centroidsOfAllClasses = []
print("*" * 10 , "Computing Clusters", "*" * 10 ) 
for i in range(0,len(symbolClasses)):
    X = []
    print("From: ", i*N, "To: ", N+N*i)
    for distoredClass in distortedClasses[i*N:(N+N*i) - 1]: #i*N:N+N*i
        values = []
        for value in distoredClass.characteristicsValues[:]:
            values.append(value[0])
        X.append(values)
    centroids = computeCluster(X, k)
    plot.show2(centroids, distortedClasses[i*N:(N+N*i) - 1], len(symbolClasses))
    centroidsOfAllClasses.append(centroids)

#plot.show2(centroidsOfAllClasses, distortedClasses, len(symbolClasses))
############################

plot = Plot()
#plot.show(symbolClasses + distortedClasses, len(symbolClasses))