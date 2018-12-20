class PIDF:
    """A PIDF skeleton class."""

    def __init__(self, setpoint=0, kp=0, ki=0, kd=0, kf=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.kf = kf

        self.last_error = 0
        self.cur_error = 0
        self.last_input = 0

        self.integral = 0
        self.derivative = 0

        self.setpoint = setpoint
        self.output = 0
        self.has_updated = False

    def update(self, input, dt):
        """Update the PIDF controller."""
        self.cur_error = self.setpoint - input

        self.proportion = self.cur_error
        self.integral = self.integral + (self.cur_error * dt)
        self.derivative = (self.cur_error - self.last_error) / dt

        self.output = (self.kp * self.proportion) + (self.ki * self.integral)
        + (self.kd * self.derivative) + (self.kf * self.setpoint)

        self.last_input = input
        self.has_updated = True
        return self.output

    def reset(self):
        """Reset control values."""

        self.last_error = 0
        self.cur_error = 0
        self.last_input = 0

        self.integral = 0
        self.derivative = 0

        self.setpoint = 0
        self.output = 0
