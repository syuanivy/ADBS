class Ship:
    """
    Representation of a ship for the game.
    """
    DIRECTION_HORIZONTAL = "horizontal"
    DIRECTION_VERTICAL = "vertical"
    DIRECTIONS = [
        DIRECTION_HORIZONTAL,
        DIRECTION_VERTICAL
    ]
    LENGTH_MIN = 3
    LENGTH_MAX = 5

    def __init__(self, x, y, direction, length):
        """
        Create a ship with the specfied characteristics. A ValueError is raised
        if any of the arguments are invalid.
        """
        if direction not in Ship.DIRECTIONS:
            raise ValueError("Invalid ship direction: %s" % direction)
        length = int(length)
        if length < Ship.LENGTH_MIN or length > Ship.LENGTH_MAX:
            raise ValueError("Invalid ship length: %i" % length)
        self.x = int(x)
        self.y = int(y)
        self.direction = direction
        self.length = length

    def get_coordinates(self):
        """
        Returns the ship's position as a list of (x, y) tuples.
        """
        if self.direction == Ship.DIRECTION_HORIZONTAL:
            coordinates = [(x, self.y) for x in range(self.x, (self.x + self.length))]
        else:
            coordinates = [(self.x, y) for y in range((self.y + 1 - self.length), (self.y + 1))]
        return coordinates

