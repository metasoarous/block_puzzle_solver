import unittest
import puzzle_solver


class PuzzleSolverTest(unittest.TestCase):

    def setUp(self):
        self.solver = PuzzleSolver("test_data")

    def test_file_loading(self):
        
