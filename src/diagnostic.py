from wpilib import PowerDistributionPanel as PDP
from networktables import NetworkTables
from wpilib import RobotController as RC
from constants import Constants
import csv


class Diagnostic:
    def __init__(self):
        self.pdp = PDP(Constants.PDP_ID)
        self.diagnostic_table = NetworkTables.getTable(
            "SmartDashboard").getSubTable("Diagnostic")
        self.pdp_table = self.diagnostic_table.getSubTable("PDP")
        self.roborio_table = self.diagnostic_table.getSubTable("roboRIO")
        self.data = {}
        self.pdp_logfile = None
        self.roborio_logfile = None

    def log(self):
        timestamp = RC.getFPGATime()
        self.logPDP(timestamp)
        self.logroboRIO(timestamp)

    def logPDP(self, timestamp):
        self.pdp_logfile.writerow(
            [timestamp] + list(self.data["PDP"].values()))

    def logroboRIO(self, timestamp):
        self.roborio_logfile.writerow(
            [timestamp] + list(self.data["roboRIO"].values()))

    def outputToSmartDashboard(self):
        self.outputPDP()
        self.outputroboRIO()

    def outputPDP(self):
        for key, value in self.data["PDP"].items():
            self._putData(self.pdp_table, key, value)

    def outputroboRIO(self):
        for key, value in self.data["roboRIO"].items():
            self._putData(self.roborio_table, key, value)

    def _putData(self, table, key, value):
        if isinstance(value, (int, float)):
            self.roborio_table.putNumber(key, value)
        elif isinstance(value, str):
            self.roborio_table.putString(key, value)
        elif isinstance(value, bool):
            self.roborio_table.putBoolean(key, value)

    def update(self):
        self.updatePDP()
        self.updateroboRIO()
        if self.pdp_logfile == None:
            self.pdp_logfile = csv.writer(open("/home/lvuser/pdp.csv", 'w'))
            self.pdp_logfile.writerow(
                ["FPGATime"] + list(self.data["PDP"].keys()))
        if self.roborio_logfile == None:
            self.roborio_logfile = csv.writer(
                open("/home/lvuser/roborio.csv", 'w'))
            self.roborio_logfile.writerow(
                ["FPGATime"] + list(self.data["roboRIO"].keys()))

    def updatePDP(self):
        self.data["PDP"] = {}
        self.data["PDP"]["Total Current"] = self.pdp.getTotalCurrent()
        for i in range(16):
            self.data["PDP"][f"Channel {i} Current"] = self.pdp.getCurrent(i)
        self.data["PDP"]["Input Voltage"] = self.pdp.getVoltage()

    def updateroboRIO(self):
        self.data["roboRIO"] = {}
        self.data["roboRIO"]["Battery Voltage"] = RC.getBatteryVoltage()
        self.data["roboRIO"]["Current 3.3V Rail"] = RC.getCurrent3V3()
        self.data["roboRIO"]["Current 5V Rail"] = RC.getCurrent5V()
        self.data["roboRIO"]["Current 6V Rail"] = RC.getCurrent6V()
        self.data["roboRIO"]["Enabled 3.3V Rail"] = RC.getEnabled3V3()
        self.data["roboRIO"]["Enabled 5V Rail"] = RC.getEnabled5V()
        self.data["roboRIO"]["Enabled 6V Rail"] = RC.getEnabled6V()
        self.data["roboRIO"]["Fault Count 3.3V Rail"] = RC.getFaultCount3V3()
        self.data["roboRIO"]["Fault Count 5V Rail"] = RC.getFaultCount5V()
        self.data["roboRIO"]["Fault Count 6V Rail"] = RC.getFaultCount6V()
        self.data["roboRIO"]["Input Current"] = RC.getInputCurrent()
        self.data["roboRIO"]["Input Voltage"] = RC.getInputVoltage()
        self.data["roboRIO"]["Voltage 3.3V Rail"] = RC.getVoltage3V3()
        self.data["roboRIO"]["Voltage 5V Rail"] = RC.getVoltage5V()
        self.data["roboRIO"]["Voltage 6V Rail"] = RC.getVoltage6V()
        self.data["roboRIO"]["Is Browned Out"] = RC.isBrownedOut()
        self.data["roboRIO"]["Is System Active"] = RC.isSysActive()
