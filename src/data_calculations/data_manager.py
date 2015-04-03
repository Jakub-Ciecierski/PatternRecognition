from src.util.random_generator import RandomGenerator
import src.util.global_variables as global_v
from src.symbols.characteristic import Characteristic
from src.symbols.symbol_class import SymbolClass
from src.symbols.symbol_types import SymbolType
from src.util.color_chooser import ColorChooser
import src.util.console as console

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
        console.write_interval(i, characteristics[i].interval.lowerBound,
                                characteristics[i].interval.upperBound,
                                "Characterestic #", "Interval:", "From:", "To:")
        
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
        console.write_point_name(symbolClass.name,text="Symbol Class:", )
        console.write_point_list(symbolClass.characteristicsValues, "Characteristics:")
#
'''
    Using provided subset of generated distorted classes function performs
    cluster-membership test, determining how many points from test set belongs
    to clusters.
    Appropriate info is displayed.
'''
def cluster_membership_test(symbolClasses):
    for symbol_class in symbolClasses:
        number_of_accepted = 0
        for distorted_class in symbol_class.test_set:
            for cluster in symbol_class.clusters:
                # Check if a given point is rejected
                result = cluster.ellipsoid.is_point_in_ellipsoid([distorted_class.characteristicsValues[:]], True)
                # If point was not rejected increment number of accepted ad stop checking
                if(result == 0):
                    number_of_accepted += 1
                    break
        console.write_name_number(symbol_class.name, 100*number_of_accepted/global_v.N_TEST, 
                                  text="% of test points accepted by symbol")
