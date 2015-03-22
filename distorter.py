from numpy import random, sqrt, log, sin, cos, pi
from random import Random


class Distorter:
    def __init__(self):
        pass
    
    def boxMuller(self, uniform1, uniform2):
        z1 = sqrt(-2*log(uniform1))*cos(2*pi*uniform2)
        z2 = sqrt(-2*log(uniform1))*sin(2*pi*uniform2)
        return z1,z2
    
    # at least two characteristics !!!
    def generateDistortion(self, cloudCenterCoordinates, _random):
        distortedCenter = []
        for i in range(len(cloudCenterCoordinates)):
#             if(i == len(cloudCenterCoordinates)-1):
#                 distortedCenter.append(cloudCenterCoordinates[i] + random.rand())
#                 break;
#             if(i % 2 == 0):
#                 dis1, dis2 = self.boxMuller(self._random.random(),self._random.random())
#                 print(i,cloudCenterCoordinates[i] + dis1)
#                 distortedCenter.append(cloudCenterCoordinates[i] + dis1)
#             else:
#                 print(i,cloudCenterCoordinates[i] + dis2)
#                 distortedCenter.append(cloudCenterCoordinates[i] + dis2)
            distortedCenter.append(cloudCenterCoordinates[i]+ _random.gauss(0, 0.3))
        return distortedCenter