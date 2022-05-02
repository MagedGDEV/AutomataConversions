import sys
import jsonManager

file = "DFA.json"
fileName = "minDFA.json"
picFile = "minDFA"
if (len(sys.argv) == 6):
    file = sys.argv[2]
    fileName = sys.argv[4]
    picFile = sys.argv[5]

jsonManager.DFA = jsonManager.readJSONFile(file)