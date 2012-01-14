
from puzzle_position import PuzzlePosition
from coordinate import Coordinate

class PuzzleSolver:
    """Puzzle Solver class - does all of the heavy lifting in orchestrating
    puzzle solving"""

    def __init__(self, segments):
        self.segments = segments
        self.solutions = []

    def solve(self):
        """ This actually solves the puzzle """
        # We are popping these segments out because it allows the
        # check_position method to work more elegantly
        a, b = self.segments.pop(0), self.segments.pop(0)
        first_leg_coordinates = map((lambda n: Coordinate((n,0,0))), range(0,a))
        last_leg_coordinates = map((lambda n: Coordinate((a,n+1,0))), range(0,b))
        coordinates = first_leg_coordinates + last_leg_coordinates
        # We start from this initial position because it takes care of the 16
        # isomorphic initial move sets that we could work from. Still possibly
        # a little bit of wiggle room for uncaught isomorphisms, but much less.
        initial_position = PuzzlePosition(coordinates)
        self.check_position(initial_position, 0)

    def check_position(self, position, legn):
        if legn < 10:
            print("Sols: {}, Depth: {}{}".format(len(self.solutions), "  "*legn, legn))
        for move in position.valid_moves(self.segments[legn]):
            if legn == len(self.segments) - 1:
                self.solutions.append(move)
            else:
                self.check_position(move, legn + 1)

def process_data_file(filename):
    data = file(filename).read().rstrip().split()
    return map(int, data)


if __name__ == "__main__":
    import time
    print "Loading data from file 'data'"
    solver = PuzzleSolver(process_data_file("data"))
    print "About to attempt solution"
    t0 = time.time()
    solver.solve()
    print "Problem solved in {} seconds".format(time.time() - t0)
    print "Number of solutions is {}".format(len(solver.solutions))
    # Load data file and run the solve method on it
