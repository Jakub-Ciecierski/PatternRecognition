import random

'''
    Simple class for random color picking.
'''
class ColorChooser:
    colors = ["dimgrey",
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
    
    def getColor(self):
        _c = random.choice(self.colors)
        self.colors.remove(_c)
        return _c
    
    def getForeignColor(self):
        return "black"