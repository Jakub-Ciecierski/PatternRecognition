import random
import matplotlib
import six

class ColorChooser:
    def __init__(self):
        # If a color does not look good on the plot, delete it from this list
        self.colors = ["dimgrey",
                        "lightslategray",
                        "lime",
                        "springgreen",
                        "red",
                        "olive",
                        "firebrick",
                        "seagreen",
                        "saddlebrown",
                        "indigo",
                        "mediumturquoise",
                        "crimson",
                        "darkolivegreen",
                        "mediumslateblue",
                        "lightseagreen",
                        "springgreen",
                        "lightsalmon",
                        "darkorchid",
                        "darkgoldenrod",
                        "sage",
                        "salmon"]
        #for name, hex in six.iteritems(matplotlib.colors.cnames):
            #self.colors.append(name)
    
    def getColor(self):
        _c = random.choice(self.colors)
        self.colors.remove(_c)
        return _c