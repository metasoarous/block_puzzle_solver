from test_helper import *
from coordinate import Coordinate

class CoordinateTestCase(unittest.TestCase):

    def setUp(self):
        self.coord_a = Coordinate((1,2,3))
        self.coord_b = Coordinate((3,2,1))

    def test_subtraction(self):
        result = self.coord_a.sub(self.coord_b)
        self.assertEqual(result, (-2,0,2))
        self.assertEqual(type(result), Coordinate)

    def test_normalize(self):
        self.assertEqual(Coordinate((2,-3,0)).normalize(), (1,1,0))

    def test_moves(self):
        coordinate = Coordinate((1,0,0))
        moves = coordinate.moves()
        self.assertTrue(not moves.__contains__(coordinate))
        self.assertEqual(len(moves), 4)
        self.assertTrue(moves.__contains__(Coordinate((0,1,0))))
        self.assertTrue(moves.__contains__(Coordinate((0,-1,0))))

    def test_negative_moves(self):
        coordinate = Coordinate((-1,0,0))
        self.assertTrue(coordinate.moves().__contains__(Coordinate((0,1,0))))




if __name__ == "__main__":
    unittest.main()
