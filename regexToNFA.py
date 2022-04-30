from goto import with_goto
import jsonManager
import sys

specialChar = [
     "*",
    "|",
     "+",
     ".",
    "(",
    ")",
     "[",
     "]",
    "{",
     "}", 
     "epsilon"
]

orStart:int = 0
orEnd:int = 0

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

@with_goto
def computeNFA (regex, count, regSize, orStart, epsilonAdded):

    
    returnValue = [0 , -1, ""]
    if (count  != regSize ):
        regChar = regex[count]
        if (regChar not in specialChar):

            returnValue = computeNFA (regex, count + 1, regexSize, orStart, epsilonAdded)
            jsonManager.addTransition("S" + str(count + epsilonAdded), "S" + str(count + 1+ epsilonAdded), regChar, jsonManager.NFA)
            if count == regSize -1 :
                returnValue = [0, count + epsilonAdded + 1, regChar]

        elif (regChar == specialChar[1]):
            
            return [1, count -1 + epsilonAdded, regex[count -1]]


    if (orStart == count and returnValue[0] == 1):
        jsonManager.addTransition ("S" + str(count), "S" + str (returnValue[1] + 2), specialChar[-1], jsonManager.NFA)
        jsonManager.addTransition ("S"+ str(returnValue[1] + 2), "S" + str(count + 1), regChar, jsonManager.NFA)
        jsonManager.NFA["S" + str(count)][regChar].remove("S" + str(count + 1))
        jsonManager.addTransition ("S" + str(returnValue[1]+1), "S" + str(returnValue[1] + 3), specialChar[-1], jsonManager.NFA)
        jsonManager.addTransition ("S" + str(count), "S" + str(returnValue[1] + 4), specialChar[-1], jsonManager.NFA)
        
        label .begin
        oldReturn = returnValue
        returnValue = computeNFA(regex, returnValue[1]+2, regSize, orStart,2)
        if (returnValue[0] == 0):
            jsonManager.addTransition("S" + str(returnValue[1]), "S" + str(oldReturn[1] + 3), specialChar[-1], jsonManager.NFA)
        elif (returnValue[1] == 1):
            jsonManager.addTransition ("S" + str(returnValue[1] + 1), "S" + str(oldReturn[1] + 3), specialChar[-1], jsonManager.NFA)
            jsonManager.addTransition("S" + str(count),"S" + str(returnValue[1] + 2), specialChar[-1], jsonManager.NFA )
            goto .begin
    return returnValue

    


computeNFA (regex, 0, regexSize, orStart, 0)
jsonManager.createJSONFile("NFA.json", jsonManager.NFA)