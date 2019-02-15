from wpilib.analogpotentiometer import AnalogPotentiometer
from wpilib.interfaces.pidsource import PIDSource


class PIDPigeon(PIDSource):
    def __init__(self, pigeon):
        self.pigeon = pigeon

    def pidGet(self):
        yaw = self.pigeon.getYawPitchRoll()[0]
        return yaw

    def setPIDSourceType(self, t):
        if t != PIDSource.PIDSourceType.kDisplacement:
            raise Exception("Must use displacement for pigeon")

    def getPIDSourceType(self):
        return PIDSource.PIDSourceType.kDisplacement
