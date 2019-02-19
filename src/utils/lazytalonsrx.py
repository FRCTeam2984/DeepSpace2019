import ctre
import logging
from networktables import NetworkTables


class LazyTalonSRX(ctre.WPI_TalonSRX):
    """A wraper for the ctre.WPI_TalonSRX to simplfy configuration and getting/setting values."""
    MotorDash = NetworkTables.getTable(
        "SmartDashboard").getSubTable("TalonSRX")
    ControlMode = ctre.WPI_TalonSRX.ControlMode

    def __init__(self, id):
        super().__init__(id)

    def initialize(self, inverted=False, encoder=False, phase=False, name=None):
        """Initialize the motors (enable the encoder, set invert status, set voltage limits)."""
        self.encoder = encoder
        if self.encoder:
            self.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, timeoutMs=10)
            self.setSensorPhase(phase)
        self.setInverted(inverted)
        self.configNominalOutputForward(0, 5)
        self.configNominalOutputReverse(0, 5)
        self.configPeakOutputForward(1, 5)
        self.configPeakOutputReverse(-1, 5)
        if name != None:
            self.setName(name)
        self.no_encoder_warning = f"No encoder connected to {self.name}"
        self.no_closed_loop_warning = f"{self.name} not in closed loop mode"

    def setPIDF(self, slot, kp, ki, kd, kf):
        """Initialize the PIDF controller."""
        self.selectProfileSlot(slot, 0)
        self.config_kP(slot, kp, 0)
        self.config_kI(slot, ki, 0)
        self.config_kD(slot, kd, 0)
        self.config_kF(slot, kf, 0)

    def setMotionMagicConfig(self, vel, accel):
        self.configMotionAcceleration(int(accel), 0)
        self.configMotionCruiseVelocity(int(vel), 0)

    def setPercentOutput(self, signal, max_signal=1):
        """Set the percent output of the motor."""
        signal = min(max(signal, -max_signal), max_signal)
        self.set(self.ControlMode.PercentOutput, signal)

    def setPositionSetpoint(self, pos):
        """Set the position of the motor."""
        self.set(self.ControlMode.Position, pos)

    def setVelocitySetpoint(self, vel):
        """Set the velocity of the motor."""
        self.set(self.ControlMode.Velocity, vel)

    def setMotionMagicSetpoint(self, pos):
        """Set the position of the motor using motion magic."""
        self.set(self.ControlMode.MotionMagic, pos)

    def zero(self):
        """Zero the encoder if it exists."""
        if self.encoder:
            self.setSelectedSensorPosition(0, 0, 0)
        else:
            logging.warning(self.no_encoder_warning)

    def getPosition(self):
        """Get the encoder position if it exists."""
        if self.encoder:
            return self.getSelectedSensorPosition(0)
        else:
            logging.warning(self.no_encoder_warning)
            return 0

    def getVelocity(self):
        """Get the encoder velocity if it exists."""
        if self.encoder:
            return self.getSelectedSensorVelocity(0)
        else:
            logging.warning(self.no_encoder_warning)
            return 0

    def getError(self):
        """Get the closed loop error if in closed loop mode."""
        if self._isClosedLoop():
            return self.getClosedLoopError(0)
        else:
            logging.warning(self.no_closed_loop_warning)
            return 0

    def getTarget(self):
        """Get the closed loop target if in closed loop mode."""
        if self._isClosedLoop():
            return self.getClosedLoopTarget(0)
        else:
            logging.warning(self.no_closed_loop_warning)
            return 0

    def outputToDashboard(self):
        #self.MotorDash.putNumber(f"{self.name} Voltage", self.getBusVoltage())
        self.MotorDash.putNumber(f"{self.name} Percent Output",
                                 self.getMotorOutputPercent())
        if self.encoder:
            self.MotorDash.putNumber(
                f"{self.name} Position", self.getPosition())
            if self._isClosedLoop():
                self.MotorDash.putNumber(f"{self.name} PIDF Target",
                                         self.getClosedLoopTarget(0))
                self.MotorDash.putNumber(f"{self.name} PIDF Error",
                                         self.getClosedLoopError(0))

    def _isClosedLoop(self):
        return self.getControlMode() == ctre.WPI_TalonSRX.ControlMode.Velocity or self.getControlMode() == ctre.WPI_TalonSRX.ControlMode.Position or self.getControlMode() == ctre.WPI_TalonSRX.ControlMode.MotionMagic
