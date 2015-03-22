from numpy import random, sqrt, log, sin, cos, pi

class Distorter:
    def __init__(self):
        self.z1 = 0
        self.z2 = 0
        pass
    
    def boxMuller(self, uniform1, uniform2):
        z1 = sqrt(-2*log(uniform1))*cos(2*pi*uniform2)
        z2 = sqrt(-2*log(uniform1))*sin(2*pi*uniform2)
        return z1,z2
    # at least two characteristics !!!
    def generateDistortion(self, cloudCenterCoordinates):
        distortedCenter = []
        rangeS = len(cloudCenterCoordinates);
        for i in range(0, rangeS):
#             if(i == (rangeS-1)):
#                 self.z1, self.z2 = self.boxMuller(random.rand(1), 
#                                                   random.rand(1))
#                 print('last one',self.z1*20,self.z2*20)
#                 distortion = self.z1 * 20
#                 distortedCenter.append(cloudCenterCoordinates[i]+distortion) 
#                 break;
#             
#             if(i % 2 == 0):
#                 self.z1,self.z2 = self.boxMuller(random.rand(1), 
#                                                   random.rand(1))
#                 distortion = self.z1 *20
#                 distortedCenter.append(cloudCenterCoordinates[i]+distortion) 
#                 print('normal ones', self.z1*20, self.z2*20)
#                 
#             if(i % 2 == 1):
#                 distortion = self.z2 * 20;    
#                 print('odd one', self.z2 * 20)
#                 distortedCenter.append(random.rand(1)) 
            distortion = random.normal(0,0.4, 1)
            if(i == 0):
                print(distortion)
            distortedCenter.append(cloudCenterCoordinates[i]+distortion) 
        return distortedCenter