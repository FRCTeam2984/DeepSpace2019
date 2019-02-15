from wpilib.interfaces.pidsource import PIDSource


class PIDAnalogGyro(PIDSource):
    def __init__(self, gyro):
        self.gyro = gyro

    def pidGet(self):
        angle = self.gyro.getAngle()
        return angle

    def setPIDSourceType(self, t):
        if t != PIDSource.PIDSourceType.kDisplacement:
            raise Exception("Must use displacement for analog gyro")

    def getPIDSourceType(self):
        return PIDSource.PIDSourceType.kDisplacement
