from wpilib.command import Command

from subsystems import shortarm, longarm
import logging
import oi


class TankArm(Command):
    def __init__(self):
        super().__init__()
        self.longarm = longarm.LongArm()
        self.shortarm = shortarm.ShortArm()

        self.requires(self.shortarm)
        self.requires(self.longarm)

    def initialize(self):
        pass

    def execute(self):
        long_speed = oi.OI().driver.getY() * 0.5
        short_speed = -oi.OI().driver.getThrottle() * 0.5

        self.longarm.m_motor.setPercentOutput(long_speed)
        self.shortarm.m_motor.setPercentOutput(short_speed)

    def isFinished(self):
        return False
