import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import global_variables as global_v

'''
    In charge of plotting data onto 3D sketch.
'''
class Plot3D:
    '''
        The only point of the constructor is to set up the axis
        as a field of the class. It contributes to lack of 
        needles passing axes object via methods. 
    '''
    def __init__(self):
        self.axes = self.__create_axes()
        
    '''
        Checks if data is suitable for 3D rendering and plots
        (or not) information.        
    '''
    def renderPlot(self, symbolClasses):
        if(global_v.CHAR_NUM == 3):
            self.__render(symbolClasses)
        else:
            print("Cannot create 3D plot - number of characteristics != 3")
    
    '''
        Core of the class. It gathers all the information regarding data display from
        provided symbol classes list and renders it on a 3D plot.
    '''
    def __render(self,symbolClasses):
        x,y,z, colors = [],[],[],[]
        
        for symbolClass in symbolClasses:
            for cluster in symbolClass.clusters:
                centroid = cluster.center
                
                # Gather points and colors.
                for point in cluster.points:
                    x.append(point[0])
                    y.append(point[1])
                    z.append(point[2])
                    colors.append(symbolClass.color)
                    self.__connect_by_line(point, centroid)
                    
                # Draw centroid
                self.axes.scatter(centroid[0], centroid[1], centroid[2], c=symbolClass.color,
                       s=40, marker='o')
                
                # Draw points mark as rejected from ellipsoid
                self.axes.scatter(cluster.rejected_x, cluster.rejected_y, cluster.rejected_z, c='r',marker='x', s=50 )
                
                # Draw ellipsoid
                ex, ey, ez = cluster.ellipsoid.get_points()
                self.axes.plot_wireframe(ex, ey, ez, color="black", alpha=0.04)
        
        # Draw all points        
        self.axes.scatter(x, y, z, c=colors, s=10, linewidth='0', alpha = 0.45, marker='o')
        
        # Add 2D label of the plot
        self.__generate_labels(symbolClasses)
        
        plt.show()
        
    '''
        Creates and returns axes object.
        Scaling way is also check and applied if needed.
    '''
    def __create_axes(self):
        axes = Axes3D(plt.figure())

        if(global_v.UNIFORM_SCALE):
            axes.set_xlim3d(global_v.CHAR_INTERVAL[0], global_v.CHAR_INTERVAL[1])
            axes.set_ylim3d(global_v.CHAR_INTERVAL[0], global_v.CHAR_INTERVAL[1])
            axes.set_zlim3d(global_v.CHAR_INTERVAL[0], global_v.CHAR_INTERVAL[1])
        print("3D plot scale uniformed:", global_v.UNIFORM_SCALE)
        
        return axes
    
    '''
        Encapsulates process of rendering a line between given points.
    '''
    def __connect_by_line(self, point1, point2):
        line_x = [point1[0],point2[0]]
        line_y = [point1[1],point2[1]]
        line_z = [point1[2],point2[2]]
        self.axes.plot(line_x, line_y, line_z, color='black', linewidth=.1)
        
    '''
        Creates labels according to information provided in a list of symbol
        classes.
    '''    
    def __generate_labels(self, symbolClasses):
        labelPos = 0.95
        self.axes.text2D(0.02, labelPos , "Plot3D", transform=self.axes.transAxes)

        lenght = len(symbolClasses)
        for i in range(0,lenght):
            labelPos -= 0.05
            index = int((len(symbolClasses) / lenght) * i)
            color = symbolClasses[index].color
            name = symbolClasses[index].name

            label = ("Class: ", name, color)
            self.axes.text2D(0.02, labelPos, label, transform=self.axes.transAxes, 
                      color=color)    