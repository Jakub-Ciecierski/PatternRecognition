from symbols.symbol_types import SymbolType
"""
    SymbolClass represents a single symbol e.g. 0, 1 or 2
    It contains a list of clusters of its sub-classes obtained by applying
    distortion of the original characteristic values.
"""
class SymbolClass:
    def __init__(self, name, color, type = SymbolType.NATIVE_BASE):
        self.name = name
        self.type = type
        self.characteristicsValues = []
        self.color = color
        self.clusters = []
        self.learning_set = []
        self.test_set = []

    def __str__(self):
        header_str = "Element"
        name_str = "Name: " + str(self.name)
        type_str = "Type: " + str(self.type)
        training_str = "Training #: " + str(len(self.learning_set))
        test_str = "Testing #: " + str(len(self.test_set))
        character_str = "Characteristics Values: " + str(self.characteristicsValues)

        full_str = "\n".join([header_str, name_str, type_str,
                            training_str, test_str,character_str]);

        return full_str
