import random
import matplotlib
import six

class ColorChooser:
    def __init__(self):
        self.colors = []
        for name, hex in six.iteritems(matplotlib.colors.cnames):
            self.colors.append(name)
    
    def getColor(self):
        _c = random.choice(self.colors)
        self.colors.remove(_c)
        return _c