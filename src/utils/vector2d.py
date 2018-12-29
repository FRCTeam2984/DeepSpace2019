import math


class Vector2D:
    """A simple 2D vector."""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def getDistance(self, vec):
        """Compute the distance between 2 vectors."""
        return math.hypot(vec.x-self.x, vec.y-self.y)

    # TODO remove
    # def getCurvature(self, p0, p1):
    #     if self.x == p0.x:
    #         p0.x += 0.0001

    #     k1 = 0.5 * (self.x**2 + self.y**2 - p0.x**2 - p0.y**2)/(self.x - p0.x)
    #     k2 = (self.y - p0.y)/(self.x - p0.x)
    #     denom = ((p1.x * k2) - p1.y + p0.y - (p0.x * k2))
    #     if denom == 0:
    #         return 0
    #     b = 0.5 * (p0.x**2 - (2 * p0.x * k1) + p0.y**2 - p1.x**2 + (2 *
    #                                                                 p1.x * k1) - p1.y**2)/denom
    #     a = k1 - (k2 * b)
    #     r = math.hypot(self.x - a, self.y - b)
    #     return 1/r

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return "({}, {})".format(round(self.x, 3), round(self.y, 3))
