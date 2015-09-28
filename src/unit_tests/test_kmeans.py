#import sys
#sys.path.append("~/programming/pattern_recognition/src/")

import unittest
import clustering.kmeans as kmeans
import util.logger as logger
import symbols.characteristic as char
import experiments.paper2 as p
#import clustering.kmeans as kmeans

class TestKMeans(unittest.TestCase):

    def test_distance(self):

        point1 = [1, 2, 3]
        point2 = [1, 2, 3]

        dist = kmeans.distance(point1, point2)

        self.assertEqual(dist, 0)

    def test_sum(self):
        point1 = [1, 2, 3]
        point2 = [2, 2, 5]

        sum_p = kmeans.sum(point1, point2)

        self.assertEqual(sum_p, [3, 4, 8])

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
