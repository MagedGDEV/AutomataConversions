import jsonManager
from tokenize import String
import sys

specialChar = {
    "star": "*",
    "Or" : "|",
    "plus": "+",
    "conc": ".",
    "openingBrac" : "(",
    "closingBrac" : ")",
    "openingSqBrac" : "[",
    "closingSqBrac" : "]",
    "openingCuBrac" : "{",
    "closingCuBrac" : "}"
}

regex = sys.argv[2]
regexSize: int = len(regex)

# def addConcSymbol(regex): 
#     stack = []
#     res = ""
#     for regChar in regex:
#         if regChar not in specialChar or regChar == "*" or regChar == "+":
#             res+=regChar
#         elif regChar == ")":
#             while len(regChar) > 0 and stack[-1] != "(":
#                 res += stack.pop()
#             stack.pop()
#         elif regChar == "(":
#             stack.append(regChar)
#         elif len(stack) == 0 or stack[-1] == "(":
#             stack.append(regChar)


#jsonManager.createJSONFile("NFA.json", jsonManager.NFA)


def computeNFA (regex, count, regSize):

    
    if (count  != regSize ):
        regChar = regex[0]
        if (regChar not in specialChar):
            computeNFA (regex[1:], count + 1, regexSize)
            jsonManager.addTransition("S" + str(count), "S" + str(count + 1), regChar, jsonManager.NFA)



computeNFA (regex, 0, regexSize)
jsonManager.createJSONFile("NFA.json", jsonManager.NFA)