import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from symbol_class import SymbolClass
import numpy as np


class Plot:
    def __init__(self):
        pass
    def show(self, symbolClasses, numberOfDifferentClasses):
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_xlim3d(0, 20)
        ax.set_ylim3d(0,20)
        ax.set_zlim3d(0,20)
        x,y,z, colors = [],[],[],[]
        for i in range(0, len(symbolClasses)):
            x.append(symbolClasses[i].characteristicsValues[0])
            y.append(symbolClasses[i].characteristicsValues[1])
            z.append(symbolClasses[i].characteristicsValues[2])
            colors.append(symbolClasses[i].color)
           
        ax.scatter(x,y,z,c=colors,s=4,linewidth='0',marker='o')
        ax.scatter(x[:numberOfDifferentClasses],
                   y[:numberOfDifferentClasses],
                   z[:numberOfDifferentClasses],
                   c='black',
                   s=40,
                   linewidth='0',
                   marker='o') 
        
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        x=np.cos(u)*np.sin(v)
        y=np.sin(u)*np.sin(v)
        z=np.cos(v)
        ax.plot_wireframe(x, y, z, color="r")
        
        plt.show()


    def show2(self, centroids, symbolClasses, numberOfDifferentClasses,
              mainLabel="Plot"):
        fig = plt.figure()
        ax = Axes3D(fig)
        x,y,z, colors = [],[],[],[]
        for i in range(0, len(symbolClasses)):
            x.append(symbolClasses[i].characteristicsValues[0])
            y.append(symbolClasses[i].characteristicsValues[1])
            z.append(symbolClasses[i].characteristicsValues[2])
            colors.append(symbolClasses[i].color)

        
        for centroid in centroids:
            ax.scatter(centroid[0],
                       centroid[1],
                       centroid[2],
                       c='black',
                       s=60,
                       linewidth='0',
                       marker='o')
        ax.scatter(x,y,z,c=colors,s=10,linewidth='0',marker='o')

        # Add 2D label of the plot
        labelPos = 0.95
        ax.text2D(0.02, labelPos , mainLabel, transform=ax.transAxes)

        for i in range(0,numberOfDifferentClasses):
            labelPos -= 0.05
            index = int((len(symbolClasses) / numberOfDifferentClasses) * i)
            color = symbolClasses[index].color
            name = symbolClasses[index].name

            label = ("Class: ", name, color)
            ax.text2D(0.02, labelPos, label, transform=ax.transAxes, 
                      color=color)
            

        plt.show()