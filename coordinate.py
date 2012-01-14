
class Coordinate(tuple):
    """This is the coordinate class. It basically just wraps tupes and gives
    us some convenient methods for subtracting them to find directions. 

    Really, we probably could have just done this with some kind of vector
    class, but it's somewhat valuable to have hacked it together ourselves for
    the sake of education."""

    # This returns a coordinate vector pointing from coordinate a to coordinate
    # b. XXXX We should think about rewriting this to use a lambda or mapping
    # of some sort.
    def sub(self, b):
        return Coordinate((self[0] - b[0], self[1] - b[1], self[2] - b[2]))

    def add(self, b):
        return Coordinate((self[0] + b[0], self[1] + b[1], self[2] + b[2]))

    def times(self, n):
        return Coordinate((self[0]*n, self[1]*n, self[2]*n))


    # This is a tad disingenuous, since really normalize should be thought of
    # not as acting on a coordinate, but as acting on a vector. But we'll just
    # talk out of both sides of our mouth on this one.
    def normalize(self):
        delta = lambda n : 0 if n == 0 else 1
        return Coordinate(map(delta, self))

    def moves(self):
        """ This method takes a normalized coordinate/vector and spits out an
        array of coordinate/vectors which represent the possible directions
        which can be moved to from that last_direction (as spit out by
        PuzzlePosition.last_direction)."""
        l = [i for i in self]
        this_index = l.index(1) if l.__contains__(1) else l.index(-1)
        indices = range(3)
        indices.remove(this_index)
        coordinates = []
        # import pdb; pdb.set_trace()
        for i in indices:
            delta = lambda j : 1 if i == j else 0
            coordinate = Coordinate([delta(j) for j in range(3)])
            coordinates.append(coordinate)
            coordinates.append(coordinate.times(-1))
        return coordinates
