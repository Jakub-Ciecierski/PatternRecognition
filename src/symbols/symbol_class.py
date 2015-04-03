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