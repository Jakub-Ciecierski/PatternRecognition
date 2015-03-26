'''
    Computes tests of accuracy of rejecting Foreign classes
'''
class ForeignRejector:
    def __init__(self):
        pass

    '''
        Computes accuracy of rejecting given set of Foreign classes
        based on the clusters of Native classes
    '''
    def accuracy_of_rejecting(self, foreignClasses, nativeClasses):
        # counts number of rejected foreign classes
        rejectedCount = 0

        # for each foreign class
        for fc in foreignClasses:
            # get its point
            point = []
            point.append(fc.characteristicsValues)
            isRejected = True;
            # check if that point belongs to some cluster
            for nc in nativeClasses:
                for cluster in nc.clusters:
                    ellipsoid = cluster.ellipsoid
                    rejected = ellipsoid.is_point_in_ellipsoid(point)
                    if not rejected[0]:
                        # belongs to cluster
                        isRejected = False
                        #foreignCluster = 
                        #print(fc.name, "has been ACCEPTED by", nc.name)
                    #else:
                        
                        #print(fc.name, "has been REJECTED by", nc.name)
            if isRejected:
                rejectedCount += 1
        print(">> Result of rejection: " ,
                        rejectedCount / (len(foreignClasses)) * 100, "%")
