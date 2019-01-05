import math
from constants import Constants
from utils import vector2d
from wpilib import SmartDashboard as Dash


class PurePursuit():
    """An implementation of the Pure Pursuit path tracking algorithm."""

    def __init__(self, path):
        self.path = path
        self.points = self.path.getPoints()
        self.curvatures = self.path.getCurvatures()
        self.lookahead_dist = Constants.LOOKAHEAD_DIST
        self.velocities = []
        self.last_lookahead_index = 0
        self.cur_curvature = 0
        self.target_velocities = vector2d.Vector2D()
        self.closest_point_index = 0

    def computeVelocities(self):
        """Compute the velocities along the path."""
        # Compute the velocities along the path using the curvature and Constants.CURVE_VELOCITY
        for curvature in self.curvatures:
            if abs(curvature) <= Constants.CURVATURE_THRESHOLD:
                velocity = Constants.MAX_VELOCITY
            else:
                velocity = min(Constants.MAX_VELOCITY,
                               Constants.CURVE_VELOCITY/curvature)
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

    def updateLookaheadPointIndex(self, state):
        """Loop over the points in the path to get the lookahead point given the current robot state."""
        for i in range(self.last_lookahead_index, len(self.points)-1):
            lookahead = self.computeLookaheadPoint(
                self.points[i], self.points[i+1], state)
            if lookahead != None:
                self.last_lookahead_index = i
                return

    def computeLookaheadPoint(self, start, end, state):
        """Compute the lookahead point given the current robot state.
           Returns a point if the current state is self.lookahead_distance
           from between start and end, otherwise returns None."""
        # Algorithm for circle line segment intersection found here: https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm/1084899#1084899
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

    def updateCurvature(self, state):
        """Update the curvature from the current lookahead point to the current robot position."""
        lookahead = self.points[self.last_lookahead_index]
        # Transform the lookahead and state.pos to get an aligned vector
        transform = lookahead - state.pos
        transform = transform.getRotated(-state.angle)
        # Use the transformed vector to calculate the curvature (derived from https://www.ri.cmu.edu/pub_files/pub3/coulter_r_craig_1992_1/coulter_r_craig_1992_1.pdf#page=12)
        self.cur_curvature = (2 * transform.x) / self.lookahead_dist**2

    def updateClosestPointIndex(self, state):
        """Update the index of the closest point to the current robot position."""
        index = self.closest_point_index
        smallest_distance = self.points[index].getDistance(state)
        for i in range(0, len(self.points)):
            distance = self.points[i].getDistance(state)
            if smallest_distance > distance:
                smallest_distance = distance
                index = i
        self.closest_point_index = index

    def updateTargetVelocities(self, state):
        """Update the target velocities of the left and right wheels."""
        robot_velocity = self.velocities[self.closest_point_index]
        # Use kinematics (http://robotsforroboticists.com/drive-kinematics/) and algebra to find wheel target velocties
        l_velocity = robot_velocity * \
            (2 + self.cur_curvature * Constants.TRACK_WIDTH) / \
            2 / Constants.PURE_PURSUIT_KV
        r_velocity = robot_velocity * \
            (2 - self.cur_curvature * Constants.TRACK_WIDTH) / \
            2 / Constants.PURE_PURSUIT_KV
        self.target_velocities = vector2d.Vector2D(l_velocity, r_velocity)

    def update(self, state):
        """Update the pure pursuit follower (runs all update functions)."""
        self.updateLookaheadPointIndex(state.pos)
        self.updateCurvature(state)
        self.updateClosestPointIndex(state.pos)
        self.updateTargetVelocities(state.pos)

    def outputToSmartDashboard(self):
        """Output values to the smart dashboard."""
        lookahead = self.points[self.last_lookahead_index]
        closest = self.points[self.closest_point_index]
        Dash.putNumberArray("Lookahead Point", [lookahead.x, lookahead.y])
        Dash.putNumber("Curvature", self.cur_curvature)
        Dash.putNumberArray("Closes Point", [closest.x, closest.y])
        Dash.putNumberArray("Target Velocities", [
            self.target_velocities.x, self.target_velocities.y])
        print("Lookahead Point - {}".format(lookahead))
        print("Curvature - {}".format(self.cur_curvature))
        print("Closes Point - {}".format(closest))
        print("Target Velocities - {}".format(self.target_velocities))
        print("------------------------------")

    def isDone(self):
        """Check if the path is done being followed."""
        return (len(self.points) - self.closest_point_index) <= 1
