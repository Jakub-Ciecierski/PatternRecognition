from util.random_generator import RandomGenerator
import util.global_variables as global_v
from characteristic import Characteristic
from symbol_class import SymbolClass
from symbol_types import SymbolType
from util.color_chooser import ColorChooser

'''
    To make main.py more transparent whole process of initialization
    starting data and performing tests on generated sets takes place here.
'''

'''
    Creation of CHAR_NUM characteristics, each with random subinterval 
    of [0,20]. Uniform distribution is used.
'''
def generate_characteristic(characteristics):
    for i in range(0,global_v.CHAR_NUM):
        characteristics.append(Characteristic())
        print("Characterestic #",i,"Interval: From:",characteristics[i].interval.lowerBound,
                    "To:",characteristics[i].interval.upperBound)
'''
    Initialization of CLASS_NUM symbol classes, each with CHAR_NUM
    characteristics. Values of each characteristic is randomized.
    Uniform distribution is used.
'''        
def generate_symbol_classes(symbolClasses, characteristics):
    for i in range(0,global_v.CLASS_NUM):
        # Store newly created symbol class in the list
        symbolClasses.append(SymbolClass(i, ColorChooser().get_color(), type = SymbolType.NATIVE_BASE))
        # Randomize value for each characteristic of the symbol
        for j in range(0,len(characteristics)):
            symbolClasses[i].characteristicsValues.append(
                            RandomGenerator().generateRandom(characteristics[j].interval.lowerBound, 
                                                             characteristics[j].interval.upperBound))
    # INFO
    for symbolClass in symbolClasses:
        print("Symbol Class:",symbolClass.name, "\n",
              "Characteristics: ", symbolClass.characteristicsValues, "\n")
'''
    Using provided subset of generated distorted classes function performs
    cluster-membership test, determining how many points from test set belongs
    to clusters.
    Appropriate info is displayed.
'''
def cluster_membership_test(symbolClasses):
    for symbol_class in symbolClasses:
        number_of_accepted = 0
        for distorted_class in symbol_class.distortedClasses[global_v.N_LEARNING:]:
            for cluster in symbol_class.clusters:
                # Check if a given point is rejected
                result = cluster.ellipsoid.is_point_in_ellipsoid([distorted_class.characteristicsValues[:]], True)
                # If point was not rejected increment number of accepted ad stop checking
                if(result == 0):
                    number_of_accepted += 1
                    break
        print("% of test points accepted by",[symbol_class.name],"symbol class: ",
               100*number_of_accepted/global_v.N_TEST,"%")
