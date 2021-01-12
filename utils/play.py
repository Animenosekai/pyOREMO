"""
BGM Handlers
"""

# Standard imports
import wave
import contextlib
from os import getcwd
from time import sleep
from os.path import isfile
from platform import system
from threading import Thread

# Pypi imports
if system() != "Darwin":
    import simpleaudio
else:
    from AppKit import NSSound
    from Foundation import NSURL

# Project imports
from utils.exceptions import FileNotFound

class PlayObj():
    """
    Mimicking simpleaudio's play object
    """
    def __init__(self, audioObj) -> None:
        self._nssound = audioObj._nssound
    
    def wait_done(self):
        """
        Waits for the sound to end (blocking)
        """
        sleep(self._nssound.duration() - self._nssound.currentTime())

    def is_playing(self):
        """
        Returns if the sound is playing or not
        """
        if self._nssound.isPlaying():
            return True
        else:
            return False

    def stop(self):
        """
        Stops the current sound
        """
        self._nssound.stop()

class AudioObj():
    """
    Mimicking the WaveObject from simpleaudio
    """
    def __init__(self, filepath) -> None:
        if '://' not in filepath:
            if not filepath.startswith('/'):
                filepath = getcwd() + '/' + filepath
            filepath = 'file://' + filepath
        url = NSURL.URLWithString_(filepath)
        self._nssound = NSSound.alloc().initWithContentsOfURL_byReference_(url, True)

    def _stopWhenDone(self, PlayObj):
        PlayObj.wait_done()
        PlayObj.stop()
        
    def play(self):
        """
        Plays the sound (non blocking)
        """
        self._nssound.stop()
        self._nssound.play()
        _playObj = PlayObj(self)
        Thread(target=self._stopWhenDone, args=[_playObj], daemon=True).start()
        return _playObj
    
class BGM():
    """
    A BGM Object
    """
    def __init__(self, filepath) -> None:
        self.filepath = str(filepath)
        if isfile(self.filepath):
            if system()!= "Darwin":
                self._audioObj = simpleaudio.WaveObject.from_wave_file(self.filepath)
            else:
                self._audioObj = AudioObj(self.filepath)
            self._playObj = None
            self._stop_loop = False
        else:
            raise FileNotFound(message="BGM not found")

    def play(self):
        self._playObj = self._audioObj.play()
        
    @property
    def is_playing(self):
        if self._playObj is None or not self._playObj.is_playing():
            return False
        else:
            return True

    def stop(self):
        if self._playObj is not None and self._playObj.is_playing():
            self._playObj.stop()
        return

    def wait(self):
        if self._playObj is not None and self._playObj.is_playing():
            self._playObj.wait_done()
        return

    def _loop(self):
        while not self._stop_loop:
            self.wait()
            if not self._stop_loop:
                self.play()

    def loop(self):
        self._stop_loop = False
        Thread(target=self._loop, daemon=True).start()

    def stop_loop(self):
        self._stop_loop = True
        self.stop()


    @property
    def duration(self):
        with contextlib.closing(wave.open(self.filepath,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            if rate != 0:
                return frames / float(rate)
            else: # mathematically incorrect
                return 0