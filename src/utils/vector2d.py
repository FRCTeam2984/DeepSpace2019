import math


class Vector2D:
    """A simple 2D vector."""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def getMagnitude(self):
        return math.hypot(self.x, self.y)

    def getArgument(self):
        return math.atan2(self.x, self.y)

    def getNormal(self):
        return self / self.getMagnitude()

    def getDistance(self, other):
        """Compute the distance between 2 vectors."""
        other = self - other
        return other.getMagnitude()

    def getRotated(self, theta):
        x = self.x * math.cos(theta) + self.y * math.sin(theta)
        y = -self.x * math.sin(theta) + self.y * math.cos(theta)
        return Vector2D(x, y)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and (self.x == other.x) and (self.y == other.y)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            x = self.x + other.x
            y = self.y + other.y
        elif isinstance(other, int) or isinstance(other, float):
            x = self.x + other
            y = self.y + other
        return Vector2D(x, y)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            x = self.x * other.x
            y = self.y * other.y
            return x + y
        elif isinstance(other, int) or isinstance(other, float):
            x = self.x * other
            y = self.y * other
            return Vector2D(x, y)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            x = self.x / other
            y = self.y / other
            return Vector2D(x, y)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __str__(self):
        return "({}, {})".format(round(self.x, 3), round(self.y, 3))
