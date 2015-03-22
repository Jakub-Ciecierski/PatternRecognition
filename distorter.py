import numpy as np

class Distorter:
    def __init__(self):
        pass
    def generateDistortion(self, cloudCenterCoordinates):
        distortedCenter = []
        for i in range(0, len(cloudCenterCoordinates)):
            distortion = np.random.normal(0, 0.2, 1)
            distortedCenter.append(cloudCenterCoordinates[i]+distortion) 
        return distortedCenter