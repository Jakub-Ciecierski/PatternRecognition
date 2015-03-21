import random
from characteristic import Characteristic
from symbol_class import SymbolClass
from plot_3d import Plot
##################

##################


# CREATE 20 CHARACTERISTICS
characteristics = []
for i in range(0,3):
    characteristics.append(Characteristic())

# CREATE 10 SYMBOL CLASSES
classes = []
for i in range(0,10):
    # Store newly created symbol class in the list
    classes.append(SymbolClass(i))
    # Randomize value for each characteristic of the symbol
    for j in range(0,len(characteristics)):
        classes[i].characteristicsValues.append(
            random.uniform(characteristics[j].interval.lowerBound, 
                           characteristics[j].interval.upperBound))


for i in range(0,len(classes)):
    print(classes[i].characteristicsValues)

plot = Plot()
plot.show(classes)
