from wpilib.command import Subsystem
from constants import Constants
from wpilib import AnalogInput
from utils import singleton
from unittest.mock import Mock
import hal

class DistanceSensor(Subsystem, metaclass=singleton.Singleton):
    def __init__(self):
        super().__init__()
    def init(self):
        if hal.isSimulation():
            self.sensor = Mock()
            self.sensor.getAverageVoltage = lambda: 0
            self.sensor.getAccumulatorCount = lambda: 0
            self.sensor.resetAccumulator = lambda: 0
        else:
            self.sensor = AnalogInput(Constants.DISTANCE_SENSOR_PORT)
            self.sensor.setAverageBits(4)

    def getVoltage(self):
        """gets raw voltage from the port"""
        return self.sensor.getAverageVoltage()

    def getAccumulatorCount(self):
        """Read the count of the accumulated values since the last call to resetAccumulator()"""
        return self.sensor.getAccumulatorCount()

    def reset(self):
        """Resets Accumulated Value"""
        self.sensor.resetAccumulator()
        
    def distanceInches(self):
        """returns values in inches"""
        return ((9.462/(self.getVoltage() - 0.01692)) / Constants.CM_TO_IN_MULTIPLYER) * 6.8
