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
     ".",
     "-",
     "epsilon"
]

regex = sys.argv[2]
regSize = len(regex)


def addConcatinationSymbol(regex, regSize):
    
    concRegex = ""
    for i in range (regSize - 1): 
        
        concRegex += regex[i]
        if regex[i] not in specialChar:
            if regex[i+1] not in specialChar or regex [i+1] == "(" or regex [i+1] == "[":
                concRegex += "."
        elif regex [i] == ")" and regex [i+1] == "(":
            concRegex+="."
        elif regex[i] == "]" and regex [i+1] == "[":
            concRegex+="."
        elif (regex [i] == "*" or regex [i] == "+") and  (regex [i+1] == "(" or regex [i+1] == "["):
            concRegex += "."
        elif (regex [i] == "*" or regex [i] == "+") and  regex [i+1]  not in specialChar:
            concRegex += "." 
        elif (regex[i] == ")" or regex[i] == "]") and regex[i+1] not in specialChar:
            concRegex += "."

def compPrecedence (first, second):
    precedence = ["|", ".", "+", "*"]
    return precedence.index(first) > precedence.index (second)

addConcatinationSymbol (regex, regSize)