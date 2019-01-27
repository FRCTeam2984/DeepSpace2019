import ctre


class TalonSRX(ctre.WPI_TalonSRX):
    """A wraper for the ctre.WPI_TalonSRX to simplfy configuration and getting/setting values."""
    NO_ENCODER_ERR = "WARNING: No encoder connected"

    def __init__(self, id):
        super().__init__(id)

    def initialize(self, inverted=False, encoder=False):
        """Initialize the motors (enable the encoder, set invert status, set voltage limits)."""
        self.encoder = encoder
        if self.encoder:
            self.configSelectedFeedbackSensor(
                ctre.FeedbackDevice.QuadEncoder, 0, timeoutMs=10)
        self.setInverted(inverted)
        self.configNominalOutputForward(0, 5)
        self.configNominalOutputReverse(0, 5)
        self.configPeakOutputForward(1, 5)
        self.configPeakOutputReverse(-1, 5)

    def setPercentOutput(self, signal, max_signal=1):
        """Set the percent output of the motor."""
        signal = min(max(signal, -max_signal), max_signal)
        self.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput, signal)

    def zero(self):
        """Zero the encoder if it exists."""
        if self.encoder:
            self.setSelectedSensorPosition(0, 0, 0)
        else:
            print(self.NO_ENCODER_ERR)

    def getPosition(self):
        """Get the encoder position if it exists."""
        if self.encoder:
            return self.lm_motor.getSelectedSensorPosition(0)
        else:
            print(self.NO_ENCODER_ERR)
            return 0

    def getVelocity(self):
        """Get the encoder velocity if it exists."""
        if self.encoder:
            return self.lm_motor.getSelectedSensorVelocity(0)
        else:
            print(self.NO_ENCODER_ERR)
            return 0
