import math
from constants import Constants


class PurePursuit():
    """An implementation of the Pure Pursuit path tracking algorithm."""

    def __init__(self, points):

        self.points = points
        self.lookahead_dist = Constants.LOOKAHEAD_DIST
        self.curvatures = [0]
        self.velocities = []

    def computeCurvatures(self):
        self.curvatures = [0]
        for i in range(1, len(self.points)-1):
            self.curvatures.append(self.points[i].getCurvature(
                self.points[i-1], self.points[i+1]))
        self.curvatures.append(0)

    def computeVelocities(self):
        self.computeCurvatures()
        for c in self.curvatures:
            if c == 0:
                v = Constants.MAX_VELOCITY
            else:
                v = min(Constants.MAX_VELOCITY, Constants.CURVE_VELOCITY_MOD/c)
            self.velocities.append(v)

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
