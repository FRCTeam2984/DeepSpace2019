class PID:
    """A PID skeleton class."""

    def __init__(self, setpoint=0, kp=0, ki=0, kd=0, continuous=False, minIn=-100, maxIn=100):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.last_error = 0
        self.cur_error = 0
        self.last_input = 0

        self.integral = 0
        self.derivative = 0

        self.setpoint = setpoint
        self.output = 0
        self.continuous = continuous

        self.minIn = minIn
        self.maxIn = maxIn

    def update(self, input, dt):
        """Update the PID controller."""
        self.cur_error = self.setpoint - input
        if self.continuous and abs(self.cur_error) > (self.maxIn - self.minIn) / 2:
            if self.cur_error > 0:
                self.cur_error = self.cur_error - self.maxIn + self.minIn
            else:
                self.cur_error = self.cur_error + self.maxIn - self.minIn
        self.proportion = self.cur_error
        self.integral = self.integral + (self.cur_error * dt)
        if dt == 0: 
            self.derivative == 0
        else:
            self.derivative = (self.cur_error - self.last_error) / dt

        self.output = (self.kp * self.proportion) + (self.ki *
                                                     self.integral) + (self.kd * self.derivative)

        self.last_input = input
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
