"""
Parsing Reclists
"""
# Standard imports
from os.path import isfile

# Pypi imports
from safeIO import TextFile

# Project imports
from utils.exceptions import FileNotFound

class Reclist():
    def __init__(self, filepath) -> None:
        if isfile(filepath):
            self.file = TextFile(filepath)
            self.phonems = []
            for line in self.file:
                line = str(line).replace("\n", "").replace(" ", "")
                if line != "":
                    self.phonems.append(line)
        else:
            raise FileNotFound(message="Reclist not found")
