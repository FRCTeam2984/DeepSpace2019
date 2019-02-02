import wpilib
import ctre
from wpilib.command import Subsystem
from constants import Constants
from utils import singleton, units, talonsrx

class Intake(Subsystem, metaclass=singleton.Singleton):
    """the intake subsystem controlls the
    intake motors as well as the intake angle"""
    def __init__(self):
        super().__init__()
    
    def init(self):
        self.li_motor = talonsrx.TalonSRX(Constants.IL_MOTOR_ID)
        self.ri_motor = talonsrx.TalonSRX(Constants.IR_MOTOR_ID)
        self.ai_motor = talonsrx.TalonSRX(Constants.IA_MOTOR_ID)
        self.ai_motor.initialize(inverted=False, encoder=True)
        self.kp = Constants.TURN_ARM_TO_ANGLE_KP
        self.ki = Constants.TURN_ARM_TO_ANGLE_KI
        self.kd = Constants.TURN_ARM_TO_ANGLE_KD
        self.kf = Constants.TURN_ARM_TO_ANGLE_KF
        self.ai_motor.setPositionPIDF(self.kp, self.ki, self.kd, self.kf)


    def setPowerSpin(self, power=0):
        neg_power = power * -1
        self.li_motor.setPercentOutput(
            power, max_signal=Constants.MAX_DRIVE_OUTPUT)
        self.ri_motor.setPercentOutput(
            neg_power, max_signal=Constants.MAX_DRIVE_OUTPUT)
    
    def resetSpin(self):
        self.setPowerSpin(0)

    def setAngle(self, angle):
        self.ai_motor.setPositionSetpoint(units.degreesToTicks(angle))
