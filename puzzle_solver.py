
from puzzle_position import PuzzlePosition, DBBase
from coordinate import Coordinate
from optparse import OptionParser
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import time
import os
import pdb


class PuzzleSolver:
    """Puzzle Solver class - does all of the heavy lifting in orchestrating
    puzzle solving"""

    def __init__(self, segments, info_depth, summary_file, db_session):
        self.segments = segments
        self.solutions = []
        self.info_depth = info_depth
        self.summary_file = summary_file
        self.db_session = db_session

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
        self.check_position(initial_position, 0, None)

    def print_and_write(text, newline=False):
        if newline:
            print(text)
            text = text + '\n'
        else:
            print(text,)
        self.summary_file.write(text)

    def check_position(self, position, legn, parent_id):
        """ This is at the heart of the solve method. It recurses through the
        valid moves and sets the position as a solution and """
        in_depth = legn < self.info_depth
        if in_depth:
            t0 = time.time()
            solutions_before = len(self.solutions)
            s = "  "
            print("Sols: {}, Depth: {}{}".format(len(self.solutions), s*legn, legn))
            position.depth = legn
            position.parent_id = parent_id
            position.coordinates = str(position.occupied_coordinates)
            self.db_session.add(position)
            self.db_session.commit()
        for move in position.valid_moves(self.segments[legn]):
            if legn == len(self.segments) - 1:
                self.solutions.append(move)
                self.print_and_write("Solution Found!!!!!")
                self.print_and_write(str(position.occupied_coordinates))
                self.print_and_write("\n"*2)
            else:
                self.check_position(move, legn + 1, position.id)
        if in_depth:
            t = time.time() - t0
            solutions = len(self.solutions) - solutions_before
            position.solutions = solutions
            position.time = t
            self.db_session.add(position)
            self.db_session.commit()

def process_data_file(filename):
    """This loads the data file, which is a numeric vector representing
    the lengths of block segments from one end of the puzzle the the other"""
    data = file(filename).read().rstrip().split()
    return map(int, data)

def parse_options():
    parser = OptionParser()
    parser.add_option('-d', '--depth', dest='info_depth', type='int', default=10,
            help = "Information depth - controls how deep to go with " +
            "infromation gathering and status display")
    parser.add_option('-f', '--file', dest='puzzle_file', default='puzzle',
            help = "Specifies the puzzle data file to load. This should " +
            "be a space seperated values file of block segment lengths. " +
            "The default is 'puzzle'.")
    parser.add_option('-o', '--output', dest='output_dir',
            default = 'run_{}'.format(time.time()),
            help = "Specify the directory where output data should be put " +
            "within the output_data directory. This defaults to a timestamped " +
            "'run' directory. Directory will be created if it does not exist")
    return parser.parse_args()


if __name__ == "__main__":
    """ This loads the data, starts the solution process and takes care of
    information display"""
    (options, args) = parse_options()
    print "Loading data from file"
    output_dir = 'output_data/' + options.output_dir
    os.mkdir(output_dir)
    engine = create_engine('sqlite:///{}/position_tree.db'.format(output_dir,
        echo=False))
    Session = sessionmaker(bind=engine)
    session = Session()
    DBBase.metadata.create_all(engine)
    summary_file = open(output_dir + '/summary_data', 'w')
    solver = PuzzleSolver(process_data_file(options.puzzle_file),
            options.info_depth, summary_file, session)
    print "About to attempt solution"
    t0 = time.time()
    solver.solve()
    solver.print_and_write("Problem solved in {} seconds".format(time.time() - t0))
    solver.print_and_write("Number of solutions is {}".format(len(solver.solutions)))

