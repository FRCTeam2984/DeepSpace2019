class SubsystemManager:
    """Loops over all subsystems and, provided that the method exists,
        calls the methods of the class"""

    def __init__(self, *arg):
        self.subsystems = arg

    def stop(self):
        """Stops all of the activity in the subsystems."""
        for subsystem in self.subsystems:
            if callable(getattr(subsystem, "stop", None)):
                subsystem.stop()

    def reset(self):
        """Returns the subsystems to their original state.
            i.e. resets sensors and clears accumulators."""
        for subsystem in self.subsystems:
            if callable(getattr(subsystem, "reset", None)):
                subsystem.reset()

    def outputToSmartDashboard(self):
        """Outputs useful information to the Smart Dashboard"""
        for subsystem in self.subsystems:
            if callable(getattr(subsystem, "outputToSmartDashboard", None)):
                subsystem.outputToSmartDashboard()

    def writeToLog(self):
        """Writes useful information to a log file."""
        for subsystem in self.subsystems:
            if callable(getattr(subsystem, "writeToLog", None)):
                subsystem.writeToLog()

    def zeroSensors(self):
        """Zeros all the sensors with regards to these subsystems."""
        for subsystem in self.subsystems:
            if callable(getattr(subsystem, "zeroSensors", None)):
                subsystem.zeroSensors()

    def update(self):
        """Runs any code that should be updated periodically on each subsystem"""
        for subsystem in self.subsystems:
            if callable(getattr(subsystem, "update", None)):
                subsystem.update()
