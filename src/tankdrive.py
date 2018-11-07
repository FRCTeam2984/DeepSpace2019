
from wpilib.command import Command
import math
import oi
import drive

class TankDrive(Command):
    '''
        Have the robot drive tank style using the PS3 Joystick until interrupted.
    '''

    def __init__(self,robot):
        super().__init__()
        self.robot = robot
        self.requires(self.robot)

    def initialize(self):
        '''Called just before this Command runs the first time'''

    def execute(self):
        '''Called repeatedly when this Command is scheduled to run'''
        power = math.pow(self.robot.oi.getJoystick().getX(), 3)
        rotation = -self.robot.oi.getJoystick().getY()
        rotation = (rotation, 0)[abs(rotation) < 0.05]
        left = power + rotation
        right = power + rotation
        self.robot.drive.setPercentOutput(left, right)

    def isFinished(self):
        '''Make this return true when this Command no longer needs to run execute()'''
        return False  # Runs until interrupted

    def end(self):
        '''Called once after isFinished returns true'''

    def interrupted(self):
        '''Called when another command which requires one or more of the same
           subsystems is scheduled to run'''
        self.end()
