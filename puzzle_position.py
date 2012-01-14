
# Some helper list methods. Should probably move these into some kind of list
# helper file at some point...

import collections
import pdb

def duplicates(xs):
    """ Wraps the collections module functionality a bit to tell us which
    elements are duplicates. Used in the no_overlapping verification method"""
    y = collections.Counter(xs)
    return [i for i in y if y[i] > 1]


class PuzzlePosition(object):
    """The PuzzlePosition class represents a specific position of the
    block puzzle"""

    def __init__(self, occupied_coordinates):
        self.occupied_coordinates = occupied_coordinates

    def valid_moves(self, number_of_blocks):
        directions = self.last_direction().moves()
        return (self.next_position(number_of_blocks, direction) for direction in
                directions if self.next_position(number_of_blocks,
                    direction).valid())

    def next_position(self, number_of_blocks, direction):
        """Returns a position objects given by passing in the numbers of blocks
        to add and the direction in which to add them"""
        coordinates = self.occupied_coordinates
        add_coordinate = lambda n : self.last_coordinate().add(direction.times(n))
        new_coordinates = map(add_coordinate, range(1, number_of_blocks+1))
        return PuzzlePosition(coordinates + new_coordinates)

    def last_coordinate(self):
        """ Simple - last coordinate..."""
        return self.occupied_coordinates[-1]

    def last_direction(self):
        """This method subtracts the last two coordinates from each other in
        order to find what the last of motion was, and returns this direction
        as a 'normalized' coordinate object"""
        return self.last_coordinate().sub(self.occupied_coordinates[-2])

    def valid(self):
        """This method applies the no_overlapping and in_bounds validity
        methods in order to make sure that the position is a valid one"""
        return self.no_overlapping() and self.in_bounds()

    def no_overlapping(self):
        """This method checks for validity with regards to blocks overlapping
        each other"""
        return len(duplicates(self.occupied_coordinates)) == 0

    def in_bounds(self):
        """This method checks to see whether the coordinates are in bounds in
        the sense of satisfying the condition of being contained within a 4x4
        cube."""
        for i in range(3):
            dim_min, dim_max = 2*[self.occupied_coordinates[0][i]]
            for coord in self.occupied_coordinates:
                dim_min = min(dim_min, coord[i])
                dim_max = max(dim_max, coord[i])
                if dim_max - dim_min > 3:
                    return False
        return True


