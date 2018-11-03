import wpilib
import wpilib.drive
import ctre


class Robot(wpilib.IterativeRobot):

    # called when robot turns on
    def robotInit(self):
        self.stick = wpilib.Joystick(0)

        self.rightMotorUp = ctre.WPI_TalonSRX(22)
        self.rightMotorDown = ctre.WPI_TalonSRX(12)
        self.rightMotors = wpilib.SpeedControllerGroup(self.rightMotorUp, self.rightMotorDown)

        self.leftMotorUp = ctre.WPI_TalonSRX(28)
        self.leftMotorDown = ctre.WPI_TalonSRX(23)
        self.leftMotors = wpilib.SpeedControllerGroup(self.leftMotorUp, self.leftMotorDown)

        self.robotDrive = wpilib.drive.DifferentialDrive(self.leftMotors, self.rightMotors)

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

    def teleopPeriodic(self):
        self.robotDrive.arcadeDrive(self.stick.getX(), -self.stick.getY())

# defining main function
if __name__ == '__main__':
    wpilib.run(Robot)

