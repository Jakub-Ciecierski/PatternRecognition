import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from symbol_class import SymbolClass
import numpy as np
from elllipsoid import Ellipsoid

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
        
#         u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
#         x=np.cos(u)*np.sin(v)
#         y=np.sin(u)*np.sin(v)
#         z=np.cos(v)
#         ax.plot_wireframe(x, y, z, color="r")
        
        plt.show()


    def show2(self, centroids,labelsPerPoint, symbolClasses, numberOfDifferentClasses,
              mainLabel="Plot"):
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

        
        for centroid in centroids:
            ax.scatter(centroid[0],
                       centroid[1],
                       centroid[2],
                       c='black',
                       s=40,
                       linewidth='0',
                       marker='o')
            ellipsoid = Ellipsoid(centroid[0], centroid[1],centroid[2], 1, 1, 1)
            e_x, e_y, e_z = ellipsoid.get_points()
            ax.plot_wireframe(e_x, e_y, e_z, color="black", alpha=0.04)
        ax.scatter(x,y,z,c=colors,s=10,linewidth='0',alpha = 0.3, marker='o')
        
        
        # Add lines
        labels_tmp = labelsPerPoint[:]
        centroids_tmp = centroids[:]
        connected_x, connected_y, connected_z = [], [], []
        for i in range(0, numberOfDifferentClasses):
            for j in range(0,len(labelsPerPoint[i])):
                centroid_coord = centroids_tmp[labelsPerPoint[i][j] + i*5]
                connected_x.append(centroid_coord[0])
                connected_y.append(centroid_coord[1])
                connected_z.append(centroid_coord[2])
#       
        
        for i in range(0, len(x)):
            temp_x, temp_y, temp_z = [], [], [] 
            temp_x.append(x[i])
            temp_x.append(connected_x[i])
            temp_y.append(y[i])
            temp_y.append(connected_y[i])
            temp_z.append(z[i])
            temp_z.append(connected_z[i])
            ax.plot(temp_x, temp_y, temp_z, color='black', linewidth=0.1)
            
        ##################################################    
        
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
        
        
        
        
    def showAllClusters(self,symbolClasses):
        fig = plt.figure()
        ax = Axes3D(fig)

        ax.set_xlim3d(0, 20)
        ax.set_ylim3d(0,20)
        ax.set_zlim3d(0,20)

        x,y,z, colors = [],[],[],[]
        for i in range(0, len(symbolClasses)):
            symbolClass = symbolClasses[i]
            for j in range(0, len(symbolClass.clusters)):
                cluster = symbolClass.clusters[j]
                
                for point in cluster.points:
                    x.append(point[0])
                    y.append(point[1])
                    z.append(point[2])
                centroid = cluster.centroid

                ax.scatter(centroid[0],
                       centroid[1],
                       centroid[2],
                       c='black',
                       s=40,
                       linewidth='0',
                       marker='o')

            colors.append(symbolClass.color)

        ax.scatter(x,y,z,c=colors,s=10,linewidth='0',alpha = 0.3, marker='o')
        
        # Add 2D label of the plot
        labelPos = 0.95
        ax.text2D(0.02, labelPos , "Plot", transform=ax.transAxes)

        lenght = len(symbolClasses)
        for i in range(0,lenght):
            labelPos -= 0.05
            index = int((len(symbolClasses) / lenght) * i)
            color = symbolClasses[index].color
            name = symbolClasses[index].name

            label = ("Class: ", name, color)
            ax.text2D(0.02, labelPos, label, transform=ax.transAxes, 
                      color=color)
        plt.show()