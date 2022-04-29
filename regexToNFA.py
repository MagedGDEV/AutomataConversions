from ctypes.wintypes import CHAR
from tkinter import W
import jsonManager
from tokenize import String
import sys

specialChars = ["*", "+", "?", "\\", "[", "]", "(", ")", "{", "}", "|", "ε"]
regex = sys.argv[2]
regexSize: int = len(regex)
currentState: String = "S"
goingState:String = "S"
count: int = 0


def handleCharacterTransition (reChar: String, count:int):

    if (reChar not in specialChars):
        currentState = "S" + str(count)
        goingState = "S" + str(count + 1)
        jsonManager.addTransition (currentState, goingState, reChar, jsonManager.NFA)
    pass

def handeCharacterTerminationState(reChar:String):
    pass

while (regexSize != count):
    jsonManager.createNewState ("S" + str(count), jsonManager.NFA)
    handleCharacterTransition (regex[count], count)
    count = count + 1


jsonManager.createJSONFile("NFA.json", jsonManager.NFA)


