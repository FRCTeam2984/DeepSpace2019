import ctre
import wpilib
import wpilib.drive
import robotstate
import constants
import drive
import oi

class Robot(wpilib.IterativeRobot):

    # called when robot turns on
    def robotInit(self):
        self.rightMotorMaster = ctre.WPI_TalonSRX(
            constants.RIGHT_MOTOR_MASTER_ID)
        self.rightMotorSlave = ctre.WPI_TalonSRX(
            constants.RIGHT_MOTOR_SLAVE_ID)
        self.leftMotorMaster = ctre.WPI_TalonSRX(
            constants.LEFT_MOTOR_MASTER_ID)
        self.leftMotorSlave = ctre.WPI_TalonSRX(constants.LEFT_MOTOR_SLAVE_ID)
        self.drive = drive.Drive(
            self, self.leftMotorSlave, self.leftMotorMaster, self.rightMotorSlave, self.rightMotorMaster)
        self.oi = oi.OI(self)
        self.robotState = robotstate.RobotState(self)
        self.timer = wpilib.Timer()

    # periodic is called whenever packet received, ~50 hertz
    # init is called when robot switches to mode
    def autonomousInit(self):
        pass

    def autonomousPeriodic(self):
        pass

    def disabledInit(self):
        pass

    def disabledPeriodic(self):
        pass

    def teleopInit(self):
        print('test')
        self.robotState.updateState(self.timer.getFPGATimestamp())

    def teleopPeriodic(self):
        self.robotState.updateState(self.timer.getFPGATimestamp())
        print(self.robotState.getState())


# defining main function
if __name__ == '__main__':
    wpilib.run(Robot)
