from enum import Enum
#from sklearn.learning_curve import learning_curve

class SymbolType(Enum):
    '''
       Represents of what type a given SymbolClass is
    '''
    NATIVE_BASE = 1         # The Native base classes, e.g. symbols 0, 1, ..., 9
    NATIVE_LEARNING = 2     # The Learning set of symbols
    NATIVE_TESTING = 3      # The Testing set of symbols
    FOREIGN = 4             # The Foreign set of symbols
