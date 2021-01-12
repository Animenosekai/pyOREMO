from time import sleep
from utils.record import Recorder
from utils.reclist import Reclist
from utils.play import BGM

if __name__ == "__main__":
    print("Welcome to pyOREMO")


    #bgmPath = input("Path to your BGM: ")
    bgmPath = "/Users/animenosekai/Desktop/sample.wav"
    bgm = BGM(bgmPath)

    #reclistPath = input("Path to Reclist: ")
    reclistPath = "/Users/animenosekai/Downloads/reclist.txt"
    reclist = Reclist(reclistPath)

    recording = Recorder("/Users/animenosekai/Documents/Coding/Projects/pyOREMO/a.aac")
    recording.record()
    sleep(5)
    recording.stop()

    
    for phonem in reclist.phonems:
        recording = Recorder("result/" + phonem + ".wav")
        print("Current Phonem: " + phonem)
        recording.record()
        bgm.play()
        bgm.wait()
        recording.stop()
