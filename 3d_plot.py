from pylab import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)

x = [6,3,6,9,12,24]
y = [3,5,78,12,23,56]
# put 0s on the y-axis, and put the y axis on the z-axis
ax.plot(xs=x, ys=[0]*len(x), zs=y, zdir='z', label='ys=0, zdir=z')
plt.show()