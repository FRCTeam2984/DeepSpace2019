from networktables import NetworkTables

import logging

logging.basicConfig(level=logging.DEBUG)


class Vision():
    def __init__(self):
        NetworkTables.initialize()
        self.table = NetworkTables.getTable("vision")

    def _connectionListener(self, connected, info):
        print(info, "; Connected=%s" % connected)
