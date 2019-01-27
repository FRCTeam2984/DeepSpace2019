from networktables import NetworkTables

import logging


class Vision():
    """A network table interface between the robot 
       and the raspberry pi for vision tracking."""

    def __init__(self):
        NetworkTables.initialize()
        self.table = NetworkTables.getTable("vision")

    def _connectionListener(self, connected, info):
        """Outputs connection data."""
        logging.info("{}; Connected={}".format(info, connected))
