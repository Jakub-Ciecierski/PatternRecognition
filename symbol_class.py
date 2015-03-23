import random

class SymbolClass:
    """
    SymbolClass represents a single symbol e.g. 0, 1 or 2
    It contains a list of clusters of its sub-classes obtained by applying
    distortion of the original characteristic values.
    """
    def __init__(self, name, color):
        self.name = name
        self.characteristicsValues = []
        self.color = color
        self.clusters = []