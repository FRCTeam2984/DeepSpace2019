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
        self.right_motor_master = ctre.WPI_TalonSRX(
            constants.RIGHT_MOTOR_MASTER_ID)
        self.right_motor_slave = ctre.WPI_TalonSRX(
            constants.RIGHT_MOTOR_SLAVE_ID)
        self.left_motor_master = ctre.WPI_TalonSRX(
            constants.LEFT_MOTOR_MASTER_ID)
        self.left_motor_slave = ctre.WPI_TalonSRX(constants.LEFT_MOTOR_SLAVE_ID)
        self.drive = drive.Drive(
            self, self.left_motor_slave, self.left_motor_master, self.right_motor_slave, self.right_motor_master)
        self.oi = oi.OI(self)
        self.robot_state = robotstate.RobotState(self)
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
        self.robot_state.updateState(self.timer.getFPGATimestamp())

    def teleopPeriodic(self):
        self.robot_state.updateState(self.timer.getFPGATimestamp())
        print(self.robot_state.getState())


# defining main function
if __name__ == '__main__':
    wpilib.run(Robot)
