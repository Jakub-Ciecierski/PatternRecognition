import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
from symbol_class import SymbolClass
import numpy as np
from elllipsoid import Ellipsoid
import numpy.linalg as la

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
#         ax.set_xlim3d(0, 20)
#         ax.set_ylim3d(0,20)
#         ax.set_zlim3d(0,20)
        
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
#         ax.set_xlim3d(0, 20)
#         ax.set_ylim3d(0,20)
#         ax.set_zlim3d(0,20)

        x,y,z, colors = [],[],[],[]
        for i in range(0, len(symbolClasses)):
            symbolClass = symbolClasses[i]
            for j in range(0, len(symbolClass.clusters)):
                
                cluster = symbolClass.clusters[j]
                centroid = cluster.centroid
                
                # Gather points and colors
                for point in cluster.points:
                    x.append(point[0])
                    y.append(point[1])
                    z.append(point[2])
                    colors.append(symbolClass.color)
                    # Draw lines
                    tmp_x = [point[0],centroid[0]]
                    tmp_y = [point[1],centroid[1]]
                    tmp_z = [point[2],centroid[2]]
                    ax.plot(tmp_x, tmp_y, tmp_z, color='black', linewidth=0.1)
                    
                # Centroid
                ax.scatter(centroid[0],
                       centroid[1],
                       centroid[2],
                       c=symbolClass.color,
                       s=40,
                       marker='o')
                
                # Draw ellipsoid
                A, centroid = self.mvee(np.array(cluster.points))    
                U, D, V = la.svd(A)    
                rx, ry, rz = 1./np.sqrt(D)
                ellipsis = Ellipsoid(0 ,0 ,0, rx, ry,rz)
                
                print(A)
                
                E = np.dstack(ellipsis.get_points())
                E = np.dot(E,V) + centroid
                ex, ey, ez = np.rollaxis(E, axis = -1)
                
#                 for i in range(len(cluster.points)):
#                     print(ellipsis.is_point_inside(cluster.points[i])
#                           )
                
                ax.plot_wireframe(ex, ey, ez, color="black", alpha=0.04)
                tx,ty,tz = ellipsis.get_points()
#                 ax.plot_wireframe(tx, ty, tz, color="r", alpha=0.04)
#                 print('hej',ellipsis.x, ellipsis.y, ellipsis.z)

        ax.scatter(x,y,z,c=colors,s=10,linewidth='0',alpha = 0.45, marker='o')
        
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
        
    def mvee(self, points, tol = 0.001):
        """
        Finds the ellipse equation in "center form"
        (x-c).T * A * (x-c) = 1
        """
        
        N, d = points.shape
        Q = np.column_stack((points, np.ones(N))).T
        err = tol+1.0
        u = np.ones(N)/N
        while err > tol:
            # assert u.sum() == 1 # invariant
            X = np.dot(np.dot(Q, np.diag(u)), Q.T)
            M = np.diag(np.dot(np.dot(Q.T, la.inv(X)), Q))
            jdx = np.argmax(M)
            step_size = (M[jdx]-d-1.0)/((d+1)*(M[jdx]-1.0))
            new_u = (1-step_size)*u
            new_u[jdx] += step_size
            err = la.norm(new_u-u)
            u = new_u
        c = np.dot(u,points)        
        A = la.inv(np.dot(np.dot(points.T, np.diag(u)), points)
                   - np.multiply.outer(c,c))/d
        return A, c