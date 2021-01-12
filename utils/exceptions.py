"""
The different exceptions that you can encounter during your use of pyOREMO
"""

class FileNotFound(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)

class RecordingError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)