from wpilib.command import InstantCommand

import odemetry


class CalibrateSensors(InstantCommand):
    def __init__(self):
        super().__init__()
        self.odemetry = odemetry.Odemetry()

    def initialize(self):
        self.odemetry.calibrate()
