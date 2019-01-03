from utils import vector2d


class Pose:
    """A simple class to store position (vector),
    and orientation (angle)."""

    def __init__(self, x=0.0, y=0.0, angle=0.0, pos=None):
        if pos == None:
            self.pos = vector2d.Vector2D(x, y)
        else:
            self.pos = pos
        self.angle = angle

    def __eq__(self, other):
        return (self.pos == other.pos) and (self.angle == other.angle)

    def __str__(self):
        return "({}, {}, {})".format(round(self.pos.x, 3), round(self.pos.y, 3), round(self.angle, 3))
