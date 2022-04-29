import jsonManager
from tokenize import String
import sys

# jsonManager.createNewState("S2", jsonManager.NFA)
# jsonManager.addTransition("S2", "S0", "A", jsonManager.NFA)
# jsonManager.createJSONFile("NFA.json", jsonManager.NFA)

specialChars = ["*", "+", "?", "/", "[", "]", ]
regex = sys.argv[2]
print (regex)