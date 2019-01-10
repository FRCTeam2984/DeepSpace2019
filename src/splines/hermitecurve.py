import math
from utils import vector2d, units


class HermiteCurve:
    """A cubic Hermite curve (https://en.wikipedia.org/wiki/Cubic_Hermite_spline) between just 2 poses."""

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.dx0 = 0
        self.dx1 = 0
        self.ax = 0
        self.bx = 0
        self.cx = 0
        self.dx = 0
        self.dy0 = 0
        self.dy1 = 0
        self.ay = 0
        self.by = 0
        self.cy = 0
        self.dy = 0
        self.computeCoefficients()

    def interpolatePoint(self, t):
        """Interpolate a point along the generated curve where 0 <= t <= 1."""
        y = (self.ay * t ** 3) + (self.by * t ** 2) + (self.cy * t) + (self.dy)
        x = (self.ax * t ** 3) + (self.bx * t ** 2) + (self.cx * t) + (self.dx)
        return vector2d.Vector2D(x, y)

    def interpolateDerivative(self, t):
        """Interpolate a derivative along the generated curve where 0 <= t <= 1."""
        dy = (3 * self.ay * t ** 2) + (2 * self.by * t) + (self.cy)
        dx = (3 * self.ax * t ** 2) + (2 * self.bx * t) + (self.cx)
        return vector2d.Vector2D(dx, dy)

    def interpolate2ndDerivative(self, t):
        """Interpolate a 2nd derivative along the generated curve where 0 <= t <= 1."""
        ddx = (6 * self.ax * t) + (2 * self.bx)
        ddy = (6 * self.ay * t) + (2 * self.by)
        return vector2d.Vector2D(ddx, ddy)

    def interpolateCurvature(self, t):
        """Interpolate a curvature along the generated curve where 0 <= t <= 1."""
        dx = self.interpolateDerivative(t).x
        dy = self.interpolateDerivative(t).y
        ddx = self.interpolate2ndDerivative(t).x
        ddy = self.interpolate2ndDerivative(t).y
        return (dx*ddy - dy*ddx) / ((dx*dx + dy*dy) * math.hypot(dx, dy))

    def computeCoefficients(self):
        """Compute the coefficients of the curve equations. This must be called inorder to make interpolations."""
        scale = 2 * math.hypot(self.end.pos.x - self.start.pos.x,
                               self.end.pos.y - self.start.pos.y)
        self.dx0 = scale * math.cos(units.degreesToRadians(-self.start.angle))
        self.dx1 = scale * math.cos(units.degreesToRadians(-self.end.angle))
        self.ax = self.dx0 + self.dx1 + 2 * self.start.pos.x - 2 * self.end.pos.x
        self.bx = -2 * self.dx0 - self.dx1 - 3 * self.start.pos.x + 3 * self.end.pos.x
        self.cx = self.dx0
        self.dx = self.start.pos.x
        self.dy0 = scale * math.sin(units.degreesToRadians(-self.start.angle))
        self.dy1 = scale * math.sin(units.degreesToRadians(-self.end.angle))
        self.ay = self.dy0 + self.dy1 + 2 * self.start.pos.y - 2 * self.end.pos.y
        self.by = -2 * self.dy0 - self.dy1 - 3 * self.start.pos.y + 3 * self.end.pos.y
        self.cy = self.dy0
        self.dy = self.start.pos.y

    def __str__(self):
        return "[{}, {}]".format(self.start, self.end)
