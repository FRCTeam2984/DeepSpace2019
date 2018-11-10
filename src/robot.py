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
        """Run when the robot turns on"""
        self.subystem_manager.zeroSensors()

    def disabledInit(self):
        """Run when the robot enters disabled mode"""
        self.subystem_manager.zeroSensors()

    def disabledPeriodic(self):
        """Run periodically during disabled mode."""
        self.robot_state.updateState(self.timer.getFPGATimestamp())
        self.subystem_manager.outputToSmartDashboard()
        self.robot_state.outputToSmartDashboard()
        pass

    def autonomousInit(self):
        """Run when the robot enters auto mode"""
        self.subystem_manager.zeroSensors()
        pass

    def autonomousPeriodic(self):
        """Run periodically during auto mode."""
        self.subystem_manager.update()
        self.robot_state.updateState(self.timer.getFPGATimestamp())
        self.subystem_manager.outputToSmartDashboard()
        self.robot_state.outputToSmartDashboard()
        pass

    def teleopInit(self):
        """Run when the robot enters teleop mode"""
        self.subystem_manager.zeroSensors()
        self.robot_state.updateState(self.timer.getFPGATimestamp())

    def teleopPeriodic(self):
        """Run periodically during teleop mode."""
        self.robot_state.updateState(self.timer.getFPGATimestamp())
        self.subystem_manager.update()
        self.subystem_manager.outputToSmartDashboard()
        self.robot_state.outputToSmartDashboard()


# defining main function
if __name__ == '__main__':
    wpilib.run(Robot)
