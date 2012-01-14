from test_helper import *
from puzzle_position import PuzzlePosition
from coordinate import Coordinate

class PuzzlePositionTest(unittest.TestCase):

    def setUp(self):
        coordinates = [
                Coordinate((0,0,0)),
                Coordinate((1,0,0)),
                Coordinate((1,1,0))
            ]
        overlapping_coordinates = coordinates + [Coordinate((0,0,0))]
        out_of_bounds_coordinates = coordinates + [Coordinate((4,0,0))]
        self.valid_position = PuzzlePosition(coordinates)
        self.overlapping_position = PuzzlePosition(overlapping_coordinates)
        self.out_of_bounds_position = PuzzlePosition(out_of_bounds_coordinates)

    def test_last_coordinate(self):
        self.assertEqual(self.valid_position.last_coordinate(), Coordinate((1,1,0)))

    def test_validity(self):
        self.assertEqual(self.valid_position.valid(), True)
        self.assertEqual(self.overlapping_position.valid(), False)
        self.assertEqual(self.out_of_bounds_position.valid(), False)

    def test_last_direction(self):
        self.assertEqual(self.valid_position.last_direction(), (0,1,0))
        self.assertEqual(type(self.valid_position.last_direction()), Coordinate)

    def test_next_position(self):
        next_position = self.valid_position.next_position(2, Coordinate((0,0,1)))
        coordinates = next_position.occupied_coordinates
        self.assertTrue(coordinates.__contains__(Coordinate((1,1,2))))
        self.assertTrue(coordinates.__contains__(Coordinate((1,1,1))))
        self.assertEqual(len(coordinates),5)

    def test_valid_moves(self):
        coordinates = self.valid_position.occupied_coordinates
        coordinates.append(Coordinate((0,1,0)))
        position = PuzzlePosition(coordinates)
        def moves_contain(position, moves, coordinate):
            moves = position.valid_moves(moves)
            coordinate_sets = map((lambda pos: pos.occupied_coordinates), moves)
            coordinates = [coord for list in coordinate_sets for
                    coord in list]
            return coordinates.__contains__(coordinate)
        self.assertTrue(moves_contain(position, 2, Coordinate((0,1,1))))
        self.assertTrue(moves_contain(position, 2, Coordinate((0,1,2))))
        self.assertTrue(moves_contain(position, 2, Coordinate((0,1,-2))))
        # This one could only be obtained by moving through the very first
        # block
        self.assertFalse(moves_contain(position, 2, Coordinate((0,-1,0))))



if __name__ == "__main__":
    unittest.main()
