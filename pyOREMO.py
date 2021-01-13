import os

from utils.record import Recorder
from utils.reclist import Reclist
from utils.play import BGM

currentDir = os.path.dirname(os.path.abspath(__file__))

class UserAction_Skip():
    def __init__(self) -> None:
        pass

class UserAction_Done():
    def __init__(self) -> None:
        pass

class UserAction_Rerecord():
    def __init__(self) -> None:
        pass

if __name__ == "__main__":
    print("Welcome to pyOREMO")

    #bgmPath = input("Path to your BGM: ")
    bgmPath = currentDir + "/data/F4-100bpm.wav"
    bgm = BGM(bgmPath)

    #reclistPath = input("Path to Reclist: ")
    reclistPath = currentDir + "/data/reclist.txt"
    reclist = Reclist(reclistPath)

    skip = False
    done = False
    
    for index, phonem in enumerate(reclist.phonems):
        if skip:
            skip = False
            if index + 2 != len(reclist.phonems):
                print("Next phonem: " + reclist.phonems[index + 1])
                print("Enter [s] to skip the next phonem")
            userInput = input("Press [enter] with nothing when you want to record the next phonem... ").replace(" ", "").lower()
            if userInput == "s":
                skip = True
            continue
        if done:
            break

        def session():
            recording = Recorder(currentDir + "/result/" + phonem.replace("/", "_") + ".aac")
            recording.record()
            os.system('cls' if os.name == 'nt' else 'clear')
            print("<< Recording... >>")
            print("Current Phonem: " + phonem)
            bgm.play()
            bgm.wait()
            recording.stop()
            print("")
            print("")
            print("")
            print("")
            print("")
            if index + 2 != len(reclist.phonems):
                print("Next phonem: " + reclist.phonems[index + 1])
            print("Enter [r] to record again the current phonem")
            if index + 2 != len(reclist.phonems):
                print("Enter [s] to skip the next phonem")
            print("Enter [d] to quit")
            userInput = input("Press [enter] with nothing when you want to record the next phonem... ").replace(" ", "").lower()
            if userInput == "r":
                return UserAction_Rerecord()
            elif userInput == "s":
                return UserAction_Skip()
            elif userInput == "d":
                return UserAction_Done()

        while True:
            action = session()
            if isinstance(action, UserAction_Skip):
                skip = True
                break
            elif isinstance(action, UserAction_Rerecord):
                continue
            elif isinstance(action, UserAction_Done):
                done = True
                break
            else:
                break

    print("お疲れ様でした!")
