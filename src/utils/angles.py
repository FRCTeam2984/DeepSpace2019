import math

def wrapPositiveAngle(in_angle: float):
    """Wrap positive angle to 0-360 degrees."""
    return abs(math.fmod(in_angle, 360.0))

def positiveAngleToMixedAngle(in_angle: float):
    """Convert an angle from 0-360 to -180-180"""
    in_angle = wrapPositiveAngle(in_angle)
    if in_angle > 180 and in_angle < 360:
        in_angle -= 180
        in_angle = 180 - in_angle
        in_angle *= -1
    return in_angle