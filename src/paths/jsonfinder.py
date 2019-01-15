import os


def getPath(filename):
    """Hacky workaround to get the absolute path to a json path file."""
    return "{}/{}".format(os.path.dirname(os.path.abspath(__file__)), filename)
