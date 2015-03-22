import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from symbol_class import SymbolClass


class Plot:
    def __init__(self):
        pass
    def show(self, symbolClasses):
        fig = plt.figure()
        ax = Axes3D(fig)
        x,y,z, colors = [],[],[], []
        for i in range(0, len(symbolClasses)):
            x.append(symbolClasses[i].characteristicsValues[0])
            y.append(symbolClasses[i].characteristicsValues[1])
            z.append(symbolClasses[i].characteristicsValues[2])
            colors.append(symbolClasses[i].color)
            # put 0s on the y-axis, and put the y axis on the z-axis
            
        
        ax.scatter(x,y,z,c=colors,s = 1.5,linewidth='0',marker='o')
        plt.show()