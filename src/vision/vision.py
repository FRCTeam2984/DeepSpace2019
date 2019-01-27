from networktables import NetworkTables

import logging

logging.basicConfig(level=logging.DEBUG)


class Vision():
    """A network table interface bewteen the robot 
       and the raspberry pi for vision tracking."""

    def __init__(self):
        NetworkTables.initialize()
        self.table = NetworkTables.getTable("vision")

    def _connectionListener(self, connected, info):
        """Outputs connection data."""
        print(info, "; Connected=%s" % connected)
