import ctre
import wpilib
import wpilib.drive
import wpilib.adxrs450_gyro
from utils import subsytemmanager
import oi
import robotstate
import constants
from subsystems import drive


class Robot(wpilib.IterativeRobot):
    def __init__(self):
        super().__init__()
        self.drive = drive.Drive()
        self.robot_state = robotstate.RobotState()
        self.subystem_manager = subsytemmanager.SubsytemManager(
            self.drive)

        self.timer = wpilib.Timer()
        self.oi = oi.OI()

    def robotInit(self):
        self.subystem_manager.zeroSensors()
        
    def disabledInit(self):
        self.subystem_manager.zeroSensors()
        pass

    def disabledPeriodic(self):
        self.robot_state.updateState(self.timer.getFPGATimestamp())
        self.subystem_manager.outputToSmartDashboard()
        pass

    def autonomousInit(self):
        self.subystem_manager.zeroSensors()
        pass

    def autonomousPeriodic(self):
        self.subystem_manager.update()
        self.robot_state.updateState(self.timer.getFPGATimestamp())
        self.subystem_manager.outputToSmartDashboard()
        pass


    def teleopInit(self):
        self.subystem_manager.zeroSensors()
        self.robot_state.updateState(self.timer.getFPGATimestamp())

    def teleopPeriodic(self):
        self.robot_state.updateState(self.timer.getFPGATimestamp())
        self.subystem_manager.update()
        self.subystem_manager.outputToSmartDashboard()

# defining main function
if __name__ == '__main__':
    wpilib.run(Robot)
