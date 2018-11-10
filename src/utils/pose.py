class Pose:
    """A simple class to store position (x and y values),
    and orientation (angle)"""

    def __init__(self, x=0.0, y=0.0, angle=0.0):
        self.x = x
        self.y = y
        self.angle = angle