from wpilib import joystick


class Joystick(joystick.Joystick):
    """A wraper for the wpilib joystick library that allows you to easily modify x, y, and z axis values."""

    def __init__(self, port, x_modifier, y_modifier, z_modifier):
        super().__init__(port)
        self.x_modifier = x_modifier
        self.y_modifier = y_modifier
        self.z_modifier = z_modifier

    def getX(self):
        """Get the modified X axis."""
        return self.x_modifier * super().getX()

    def getY(self):
        """Get the modified Y axis."""
        return self.y_modifier * super().getY()

    def getZ(self):
        """Get the modified Z axis."""
        return self.z_modifier * super().getZ()
