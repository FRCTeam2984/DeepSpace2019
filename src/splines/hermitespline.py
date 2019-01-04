#!/usr/bin/env python
import json
import math
import os.path

from splines import hermitecurve as hc
from utils import pose, vector2d
from paths import jsonfinder


class HermiteSpline:
    """A cubic Hermite spline made up of several HermiteCurves."""

    def __init__(self, poses=None, filename=None):
        self.curves = []
        self.res = 100

        if poses == None and filename != None:
            self.poses = []
            self.load(filename)
        elif poses != None and filename == None:
            self.poses = poses
        elif poses != None and filename != None:
            print("Both poses and filename provided, defaulting to poses")
            self.poses = poses
        else:
            self.poses = []

    def addPose(self, *argv):
        """Add some number of poses to the spline."""
        self.poses += argv

    def updateCurves(self):
        """Create the list of HermiteCurves. This must be run in order to make interpolations."""
        self.curves = []
        for i in range(0, len(self.poses)-1):
            self.curves.append(hc.HermiteCurve(self.poses[i], self.poses[i+1]))

    def computeCoefficients(self):
        """Compute the coefficients of the curves. This is done by default when constructing an HermiteCurves."""
        if len(self.curves) == 0:
            return
        for curve in self.curves:
            curve.computeCoefficients()

    def _getT(self, t):
        """Scale a t value based on the number of curves and return the new t value and the index of the curve to use."""
        t = min(max(t, 0), 1)
        t *= len(self.curves)
        index = math.floor(t) if t != len(self.curves) else len(self.curves)-1
        return (t-index, index)

    def interpolatePoint(self, t):
        """Interpolate a point along the spline where 0 <= t <= 1."""
        if len(self.curves) == 0:
            return None
        ret = self.curves[self._getT(t)[1]].interpolatePoint(
            self._getT(t)[0])
        return ret

    def interpolateDerivative(self, t):
        """Interpolate a derivative along the spline where 0 <= t <= 1."""
        if len(self.curves) == 0:
            return None
        ret = self.curves[self._getT(t)[1]].interpolateDerivative(
            self._getT(t)[0])
        return ret

    def interpolate2ndDerivative(self, t):
        """Interpolate a 2nd derivative along the spline where 0 <= t <= 1."""
        if len(self.curves) == 0:
            return None
        ret = self.curves[self._getT(t)[1]].interpolate2ndDerivative(
            self._getT(t)[0])
        return ret

    def interpolateCurvature(self, t):
        """Interpolate the curvature along the spline where 0 <= t <= 1."""
        if len(self.curves) == 0:
            return None
        ret = self.curves[self._getT(t)[1]].interpolateCurvature(
            self._getT(t)[0])
        return ret

    def getPoints(self):
        """Interpolate a list of points that is self.res long."""
        return [self.interpolatePoint(i/self.res) for i in range(0, self.res+1)]

    def getDerivatives(self):
        """Interpolate a list of derivatives that is self.res long."""
        return [self.interpolateDerivative(i/self.res) for i in range(0, self.res+1)]

    def get2ndDerivatives(self):
        """Interpolate a list of 2nd derivatives that is self.res long."""
        return [self.interpolate2ndDerivative(i/self.res) for i in range(0, self.res+1)]

    def getCurvatures(self):
        """Interpolate a list of curvatures that is self.res long."""
        return [self.interpolateCurvature(i/self.res) for i in range(0, self.res+1)]

    def load(self, filename):
        """Load a json path file into a spline. The paths folder is searched by default."""
        path = jsonfinder.getPath(filename)
        try:
            with open(path) as path_data:
                path_json = json.load(path_data)
                for point_data in path_json:
                    try:
                        pose_data = point_data["pose"]
                        pose0 = pose.Pose(
                            pose_data["x"], pose_data["y"], pose_data["heading"])
                        self.addPose(pose0)
                    except KeyError:
                        print("Json is invalid")
                        return
            self.updateCurves()
        except FileNotFoundError:
            print("{} not found".format(filename))

    def __str__(self):
        return "[{}]".format(", ".join(str(p) for p in self.poses))
