import random
from characteristic import Characteristic
from symbol_class import SymbolClass
from plot_3d import Plot
import numpy as np

# CREATE 20 CHARACTERISTICS
characteristics = []
for i in range(0,3):
    characteristics.append(Characteristic())

# CREATE 10 SYMBOL CLASSES
symbolClasses = []
for i in range(0,10):
    # Store newly created symbol class in the list
    symbolClasses.append(SymbolClass(i))
    # Randomize value for each characteristic of the symbol
    for j in range(0,len(characteristics)):
        symbolClasses[i].characteristicsValues.append(
            random.uniform(characteristics[j].interval.lowerBound, 
                           characteristics[j].interval.upperBound))


for i in range(0,len(symbolClasses)):
    print(symbolClasses[i].characteristicsValues)

sep = "*" * 30
print(sep,)

''' DISTORTION '''

N = 100
distortedClasses = []
for cl in symbolClasses[:]:
    # this is not safe, the cl values will be changes too
    characteristicsValues = cl.characteristicsValues[:]
    for i in range(0, N):
        for j in range(0, len(characteristicsValues)):
            distortion = np.random.normal(0, 5, 1)
            print(distortion[0])
            characteristicsValues[j] += distortion[0]

        sc = SymbolClass(cl.name)
        for k in range(0,len(characteristicsValues)):
            sc.characteristicsValues.append(characteristicsValues[k])

        distortedClasses.append(sc);

''' END OF DISTORTION '''

for i in range(0, len(distortedClasses)):
    print(distortedClasses[i].characteristicsValues)

plot = Plot()
plot.show(distortedClasses)