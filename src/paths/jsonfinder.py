import os


def getPath(filename):
    return "{}/{}".format(os.path.dirname(os.path.abspath(__file__)), filename)
