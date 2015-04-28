import random
import util.global_variables as global_v

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
    
    def get_color(self):
        if global_v.WHICH_COLOR == 0:
            global_v.WHICH_COLOR += 1
            return "red"
        else:
            return "indigo"
        
        _c = random.choice(self.colors)
        self.colors.remove(_c)
        return _c

    
    def getForeignColor(self):
        return "black"