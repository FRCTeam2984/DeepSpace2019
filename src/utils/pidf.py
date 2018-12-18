class PIDF:
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

    def update(self, input, dt):
        self.cur_error = self.setpoint - input

        self.proportion = self.cur_error
        self.integral = self.integral + (self.cur_error * dt)
        self.derivative = (self.cur_error - self.last_error) / dt
        
        self.output = (self.kp * self.proportion) + (self.ki * self.integral)
        + (self.kd * self.derivative) + (self.kf * self.setpoint)

        self.last_input = input
        return self.output

    def reset(self):
        self.last_error = 0
        self.cur_error = 0
        self.last_input = 0

        self.integral = 0
        self.derivative = 0

        self.setpoint = 0
        self.output = 0
