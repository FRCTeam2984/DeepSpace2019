'''
stop()
reset()
outputToSmartDashboard()
writeToLog()
zeroSensors()
registerEnabledLoops(Looper enabledLooper):
'''


class SubsytemManager:
    def __init__(self, *arg):
        self.subsystems = arg

    def stop(self):
        for subsystem in self.subsystems:
            if callable(getattr(subsystem, "stop", None)):
                subsystem.stop()

    def reset(self):
        for subsystem in self.subsystems:
            if callable(getattr(subsystem, "reset", None)):
                subsystem.reset()

    def outputToSmartDashboard(self):
        for subsystem in self.subsystems:
            if callable(getattr(subsystem,"outputToSmartDashboard",None)):
                subsystem.outputToSmartDashboard()

    def writeToLog(self):
        for subsystem in self.subsystems:
            if callable(getattr(subsystem,"writeToLog",None)):
                subsystem.writeToLog()

    def zeroSensors(self):
        for subsystem in self.subsystems:
            if callable(getattr(subsystem,"zeroSensors",None)):
                subsystem.zeroSensors()

    def update(self):
        for subsystem in self.subsystems:
            if callable(getattr(subsystem,"update",None)):
                subsystem.update()

