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
                for word in str(line).replace("\n", "").split(" "):
                    if word.replace(" ", "") != "":
                        self.phonems.append(word.replace(" ", ""))
        else:
            raise FileNotFound(message="Reclist not found")
