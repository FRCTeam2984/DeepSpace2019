from wpilib.command import Subsystem
from constants import Constants
from wpilib import AnalogInput
from utils import singleton, units
from unittest.mock import Mock
import hal


class DistanceSensor(Subsystem, metaclass=singleton.Singleton):
    """IR Distance sensor used on the front of the robot."""

    def __init__(self):
        super().__init__()
        if hal.isSimulation():
            self.sensor = Mock()
            self.sensor.getAverageVoltage = lambda: 0
        else:
            self.sensor = AnalogInput(Constants.DISTANCE_SENSOR_PORT)
            self.sensor.setAverageBits(4)

    def getVoltage(self):
        """Gets the voltage from the port."""
        return self.sensor.getAverageVoltage()

    def distanceInches(self):
        """Get the distance in inches."""
        return units.metersToInches((9.462 / (self.getVoltage() - 0.01692)) / 100)
