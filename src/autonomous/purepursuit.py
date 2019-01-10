import math
from constants import Constants
from utils import vector2d
from wpilib import SmartDashboard as Dash
from autonomous import pursuitpoint


class PurePursuit():
    """An implementation of the Pure Pursuit path tracking algorithm."""

    def __init__(self, path):
        self.path = path
        self.pursuit_points = [pursuitpoint.PursuitPoint(p, c) for p, c in zip(
            self.path.getPoints(), self.path.getCurvatures())]
        self.last_lookahead_index = 0
        self.cur_curvature = 0
        self.target_velocities = vector2d.Vector2D()
        self.closest_point_index = 0

    def computeVelocities(self):
        """Compute the velocities along the path."""
        # Compute the velocities along the path using the curvature and Constants.CURVE_VELOCITY
        for ppoint in self.pursuit_points:
            if abs(ppoint.curvature) <= Constants.CURVATURE_THRESHOLD:
                velocity = Constants.MAX_VELOCITY
            else:
                velocity = min(Constants.MAX_VELOCITY,
                               Constants.CURVE_VELOCITY/ppoint.curvature)
            ppoint.velocity = velocity
        print(self.pursuit_points[0].velocity)
        # Limit the acceleration of the velocities
        for i in reversed(range(0, len(self.pursuit_points)-1)):
            distance = self.pursuit_points[i].point.getDistance(self.pursuit_points[i+1].point)
            new_velocity = math.sqrt(
                self.pursuit_points[i+1].velocity**2 + (2 * Constants.MAX_ACCELERATION * distance))
            new_velocity = min(self.pursuit_points[i].velocity, new_velocity)
            self.pursuit_points[i].velocity = new_velocity

    def updateLookaheadPointIndex2(self, state):
        """Update the lookahead point given the current robot state.
           Uses the minimum distance point if the state is more than
           Constants.LOOKAHEAD_DIST from all points, otherwise uses the
           closes point to self.loohead_distance"""
        # Compute point distances to state and differences from those distances to Constants.LOOKAHEAD_DIST
        distances = [math.hypot(state.x - ppoint.point.x,
                                state.y - ppoint.point.y) for ppoint in self.pursuit_points]
        differences = [abs(d-Constants.LOOKAHEAD_DIST) for d in distances]
        min_distance = min(distances)
        # Get new lookahead index
        if min_distance <= Constants.LOOKAHEAD_DIST:
            self.last_lookahead_index = differences.index(min(differences))
        else:
            self.last_lookahead_index = distances.index(min_distance)

    def updateLookaheadPointIndex(self, state):
        """Loop over the points in the path to get the lookahead point given the current robot state."""
        for i in range(self.last_lookahead_index, len(self.pursuit_points)-1):
            lookahead = self.computeLookaheadPoint(
                self.pursuit_points[i].point, self.pursuit_points[i+1].point, state)
            if lookahead != None:
                self.last_lookahead_index = i

    def computeLookaheadPoint(self, start, end, state):
        """Compute the lookahead point given the current robot state.
           Returns a point if the current state is Constants.LOOKAHEAD_DIST
           from between start and end, otherwise returns None."""
        # Algorithm for circle line segment intersection found here: https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm/1084899#1084899
        segment_direction = end - start
        center_to_start = start - state

        a = segment_direction * segment_direction
        b = 2 * (center_to_start * segment_direction)
        c = (center_to_start * center_to_start) - Constants.LOOKAHEAD_DIST ** 2
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
        lookahead = self.pursuit_points[self.last_lookahead_index].point
        # Transform the lookahead and state.pos to get an aligned vector
        transform = lookahead - state.pos
        transform = transform.getRotated(-state.angle)
        # Use the transformed vector to calculate the curvature (derived from https://www.ri.cmu.edu/pub_files/pub3/coulter_r_craig_1992_1/coulter_r_craig_1992_1.pdf#page=12)
        self.cur_curvature = (2 * transform.x) / Constants.LOOKAHEAD_DIST**2

    def updateClosestPointIndex(self, state):
        """Update the index of the closest point to the current robot position."""
        index = self.closest_point_index
        smallest_distance = self.pursuit_points[index].point.getDistance(state)
        for i in range(0, len(self.pursuit_points)):
            distance = self.pursuit_points[i].point.getDistance(state)
            if smallest_distance > distance:
                smallest_distance = distance
                index = i
        self.closest_point_index = index

    def updateTargetVelocities(self, state):
        """Update the target velocities of the left and right wheels."""
        robot_velocity = self.pursuit_points[self.closest_point_index].velocity
        # Use kinematics (http://robotsforroboticists.com/drive-kinematics/) and algebra to find wheel target velocties
        l_velocity = robot_velocity * \
            (2 + self.cur_curvature * Constants.TRACK_WIDTH) / \
            2 / Constants.PURE_PURSUIT_KV
        r_velocity = robot_velocity * \
            (2 - self.cur_curvature * Constants.TRACK_WIDTH) / \
            2 / Constants.PURE_PURSUIT_KV
        self.target_velocities = vector2d.Vector2D(l_velocity, r_velocity)

    def update(self, state):
        """Update the pure pursuit follower(runs all update functions)."""
        # TODO which lookahead function to use
        # self.updateLookaheadPointIndex(state.pos)
        self.updateLookaheadPointIndex2(state.pos)
        self.updateCurvature(state)
        self.updateClosestPointIndex(state.pos)
        self.updateTargetVelocities(state.pos)

    def outputToSmartDashboard(self):
        """Output values to the smart dashboard."""
        lookahead = self.pursuit_points[self.last_lookahead_index].point
        closest = self.pursuit_points[self.closest_point_index].point
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
        return (len(self.pursuit_points) - self.closest_point_index) <= 1
