import math
from constants import Constants
from utils import vector2d


class PurePursuit():
    """An implementation of the Pure Pursuit path tracking algorithm."""

    def __init__(self, path):

        self.path = path
        self.points = self.path.getPoints()
        self.curvatures = self.path.getCurvatures()
        self.lookahead_dist = Constants.LOOKAHEAD_DIST
        self.velocities = []
        self.last_lookahead = 0

    def computeVelocities(self):
        """Compute the velocities along the path."""
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

    # TODO - test old function
    # def getLookaheadPoint(self, state):
    #     """Get the lookahead point given the current robot state. Finds a point on the path at least self.lookhead_dist distance away from the current robot state."""
    #     px = [p.x for p in self.points]
    #     py = [p.y for p in self.points]
    #     dx = [state.pos.x - x for x in px]
    #     dy = [state.pos.y - y for y in py]
    #     d = [abs(math.sqrt(idx ** 2 + idy ** 2)) for (idx, idy) in zip(dx, dy)]
    #     index = d.index(min(d))
    #     lookahead_cur = 0
    #     while lookahead_cur < self.lookahead_dist and (index+1) < len(self.points):
    #         dx = px[index+1] - px[index]
    #         dy = py[index+1] - py[index]
    #         lookahead_cur += math.hypot(dx, dy)
    #         index += 1
    #     return self.points[index]

    def getLookaheadPoint(self, state):
        """Loop over the points in the path to get the lookahead point given the current robot state."""
        for i in range(self.last_lookahead, len(self.points)-1):
            lookahead = self.computeLookaheadPoint(
                self.points[i], self.points[i+1], state)
            if lookahead != None:
                self.last_lookahead = i
                return self.points[i]

    def computeLookaheadPoint(self, start, end, center):
        """Compute the lookahead point given the current robot state. Finds a point on the path at least self.lookhead_dist distance away from the current robot state."""
        pstate = center
        state = vector2d.Vector2D(pstate.x, pstate.y)
        segment_direction = end - start
        center_to_start = start - state

        a = segment_direction * segment_direction
        b = 2 * (center_to_start * segment_direction)
        c = (center_to_start * center_to_start) - self.lookahead_dist ** 2
        discriminant = b**2 - (4 * a * c)

        if discriminant < 0:
            return None
        else:
            discriminant = math.sqrt(discriminant)
            t0 = (-b - discriminant) / (2 * a)
            t1 = (-b + discriminant) / (2 * a)
            if t0 >= 0 and t0 <= 1:
                return start + t0 * segment_direction
            if t1 >= 0 and t1 <= 1:
                return start + t1 * segment_direction
            return None

    def getCurvature(self, lookahead, state):
        if lookahead == None:
            return None
        if lookahead.x == state.pos.x:
            return None
        slope = (lookahead.y - state.pos.y) / (lookahead.x - state.pos.x)
        a = -slope
        b = 1
        c = slope * state.pos.x - state.pos.y
        x_distance = abs((a * lookahead.x) +
                         (b * lookahead.y) + c)/math.hypot(a, b)
        curvature = (2 * x_distance) / self.lookahead_dist**2
        sign = math.sin(state.angle) * (lookahead.x - state.pos.x) - \
            math.cos(state.angle) * (lookahead.y - state.pos.y)
        return math.copysign(curvature, sign)

    def update(self, state):
        """Update the pure pursuit follower."""
        lookahead = self.getLookaheadPoint(state.pos)
        curvature = self.getCurvature(lookahead, state)
        print("state: {}\nlookahead: {}\ncurvature: {}\n".format(state,lookahead,curvature))
        self.last_state = state

    def getTargetVelocities(self):
        """Get the target velocities of the left and right wheels."""
        # TODO compute target velocities
        return vector2d.Vector2D(1, 1)

    def isDone(self):
        """Check if the path is done being followed."""
        # TODO check if done
        return False
