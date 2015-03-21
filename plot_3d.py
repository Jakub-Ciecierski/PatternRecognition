import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from symbol_class import SymbolClass


class Plot:
    def __init__(self):
        pass
    def show(self, classes):
        fig = plt.figure()
        ax = Axes3D(fig)
        x,y,z = [],[],[]
        for i in range(0, len(classes)):
            x.append(classes[i].characteristicsValues[0])
            y.append(classes[i].characteristicsValues[1])
            z.append(classes[i].characteristicsValues[2])
            # put 0s on the y-axis, and put the y axis on the z-axis
        ax.scatter(x,y,z,c='b',marker='o')
        plt.show()