from utils.exceptions import RecordingError

## macOS
from AVFoundation import AVAudioRecorder, AVAudioSession
from Foundation import NSURL, NSDictionary, NSString
from CoreAudio import kAudioFormatMPEG4AAC
import objc

class Recorder():
    """
    An object to record from the microphone on macOS
    """
    def __init__(self, filepath) -> None:
        url = NSURL.fileURLWithPath_(NSString.stringByExpandingTildeInPath(filepath))
        audioDict = NSDictionary.dictionaryWithDictionary_({'AVFormatIDKey': kAudioFormatMPEG4AAC, 'AVSampleRateKey': AVAudioSession.sharedInstance().sampleRate(), 'AVNumberOfChannelsKey': AVAudioSession.sharedInstance().inputNumberOfChannels() })
        currentPermission = AVAudioSession.alloc().recordPermission()
        if currentPermission in [1684369017, 1970168948]:
            AVAudioSession.alloc().requestRecordPermission_(None)
            if AVAudioSession.alloc().recordPermission() == 1684369017:
                raise RecordingError("pyOREMO needs your authorization to record things")
        self._avaudiorecorder, error = AVAudioRecorder.alloc().initWithURL_settings_error_(url, audioDict, objc.nil)
        if self._avaudiorecorder is None:
            raise RecordingError("An error occured while creating the AVAudioRecorder object: " + str(error))

    def record(self):
        """
        Starts recording
        """
        if self._avaudiorecorder.prepareToRecord():
            self._avaudiorecorder.record()
        else:
            raise RecordingError(message="An error occured while preparing to record")
    
    def pause(self):
        """
        Pauses recording
        """
        self._avaudiorecorder.pause()
    
    def stop(self):
        """
        Stops recording
        """
        self._avaudiorecorder.stop()

    @property
    def is_recording(self):
        """
        If it is recording or not
        """
        return self._avaudiorecorder.isRecording()


"""other systems
import wave
from os import getcwd
from sys import argv
import pyaudio

def record(filepath, duration, playback=False, channels=1, chunk=1024, sample_rate=44100, format=pyaudio.paInt16):
    pyAudioObj = pyaudio.PyAudio()
    if "-d" in argv:
        print(pyAudioObj.get_default_host_api_info())
    pyAudioObj.is_format_supported(input_format=pyaudio.paInt16, input_channels=channels, rate=sample_rate, input_device=0)
    stream = pyAudioObj.open(format=format, channels=channels, rate=sample_rate, input=True, output=True, frames_per_buffer=chunk)
    frames = []
    print("Recording...")
    for _ in range(int(44100 / chunk * duration)):
        data = stream.read(chunk)
        if playback:
            stream.write(data) # If you want to hear your voice while recording
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    pyAudioObj.terminate()
    outputFile = wave.open(filepath, "wb")
    outputFile.setnchannels(channels)
    outputFile.setsampwidth(pyAudioObj.get_sample_size(format))
    outputFile.setframerate(sample_rate)
    outputFile.writeframes(b"".join(frames))
    outputFile.close()

"""