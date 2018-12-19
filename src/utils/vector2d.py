import math


class Vector2D:
    """A simple 2D vector."""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def getDistance(self, vec):
        """Compute the distance between 2 vectors."""
        return math.hypot(vec.x-self.x, vec.y-self.y)

    def __str__(self):
        return "({}, {})".format(round(self.x, 3), round(self.y, 3))
