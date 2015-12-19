class Board:
    """
    Representation of ships and their positions on a map.
    """
    def __init__(self, xsize, ysize):
        """
        Create a rectangular board with integer coordinates that range from
        (0, 0) to (xsize-1, ysize-1).
        """
        xsize = int(xsize)
        ysize = int(ysize)
        if xsize < 0 or ysize < 0:
            raise ValueError("Invalid board size: %s", ((xsize, ysize),))
        self.xsize = xsize
        self.ysize = ysize
        self._grid = [[None for y in range(ysize)] for x in range(xsize)]

    def add_ship(self, ship):
        """
        Add a ship to the board. Raises an IndexError if the ship falls out of
        bounds.
        """
        if ship.x < 0 or ship.x >= self.xsize or ship.y < 0 or ship.y >= self.ysize:
            raise IndexError("Ship start position is not on board: %s" % ((ship.x, ship.y),))
        # Start with highest coordinate to get IndexError if out of bounds
        for x, y in reversed(sorted(ship.get_coordinates())):
            self._grid[x][y] = ship

    def query_coordinate(self, x, y):
        """
        Returns the ship that exists at the (x, y) coordinate on the board or
        None if there is no ship. Raises an IndexError if the coordinates fall
        out of bounds or a ValueError if the coordinates are not valid.
        """
        x = int(x)
        y = int(y)
        if x < 0 or x >= self.xsize or y < 0 or y >= self.ysize:
            raise IndexError("Position is not on board: %s" % ((x, y),))
        return self._grid[x][y]