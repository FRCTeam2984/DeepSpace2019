import math
from constants import Constants


class PurePursuit():
    """An implementation of the Pure Pursuit path tracking algorithm."""

    def __init__(self, spline):

        self.spline = spline
        self.points = self.spline.getPoints()
        self.curvatures = self.spline.getCurvatures()
        self.lookahead_dist = Constants.LOOKAHEAD_DIST
        self.velocities = []

    def computeVelocities(self):
        # Compute the velocities along the path using the curvature and Constants.CURVE_VELOCITY_MOD
        for curvature in self.curvatures:
            if curvature == 0:
                velocity = Constants.MAX_VELOCITY
            else:
                velocity = min(Constants.MAX_VELOCITY,
                               Constants.CURVE_VELOCITY_MOD/curvature)
            self.velocities.append(velocity)
        # Limit the acceleration of the velocities
        for i in reversed(range(0, len(self.velocities)-1)):
            distance = self.points[i].getDistance(self.points[i+1])
            new_velocity = math.sqrt(
                self.velocities[i+1]**2 + (2 * Constants.MAX_ACCELERATION * distance))
            new_velocity = min(self.velocities[i], new_velocity)
            self.velocities[i] = new_velocity

    def getLookheadPoint(self, state):
        """Get the lookahead point given the current robot state. Finds a point on the path at least self.lookhead_dist distance away from the current robot state."""
        px = [p.y for p in self.points]
        py = [p.y for p in self.points]
        dx = [state.x - x for x in px]
        dy = [state.y - y for y in py]
        d = [abs(math.sqrt(idx ** 2 + idy ** 2)) for (idx, idy) in zip(dx, dy)]
        index = d.index(min(d))
        lookahead_cur = 0
        while lookahead_cur < self.lookahead_dist and (index+1) < len(self.points):
            dx = px[index+1] - px[index]
            dy = py[index+1] - py[index]
            lookahead_cur += math.hypot(dx, dy)
            index += 1
        return self.points[index]

    def isDone(self):
        return False
