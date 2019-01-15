from wpilib import joystick
from wpilib.buttons import joystickbutton


class Joystick(joystick.Joystick):
    """A wraper for the wpilib joystick library that allows you
       to easily modify x, y, and z axis values."""

    def __init__(self, port, x_modifier, y_modifier, z_modifier, deadzone=0.05):
        super().__init__(port)
        self.x_modifier = x_modifier
        self.y_modifier = y_modifier
        self.z_modifier = z_modifier
        self.deadzone = deadzone

    def getX(self):
        """Get the modified X axis."""
        value = super().getX()
        if abs(value) < self.deadzone:
            return 0
        return self.x_modifier * value

    def getY(self):
        """Get the modified Y axis."""
        value = super().getY()
        if abs(value) < self.deadzone:
            return 0
        return self.y_modifier * value

    def getZ(self):
        """Get the modified Z axis."""
        value = super().getZ()
        if abs(value) < self.deadzone:
            return 0
        return self.z_modifier * value
