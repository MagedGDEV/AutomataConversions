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


def addConcatenationSymbol(regex, regSize):
    
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

    concRegex += regex[-1]
    return concRegex

def compPrecedence (first, second):
    precedence = ["|", ".", "+", "*"]
    return precedence.index(first) > precedence.index (second)

def getPostFix (concatenatedRegex, concSize):

    stack = []
    postFix = ""
    i = 0
    while i  < concSize:
        concReChar = concatenatedRegex[i]
        if concReChar not in specialChar or concReChar == "*" or concReChar == "+" or concReChar == "[":
            if (concReChar == "["):
                for j in range (5):
                    postFix+=concatenatedRegex[i+j]
                i += 4
            else:
                postFix += concReChar
            
        elif concReChar == ")":
            while len(stack) > 0 and stack [-1] != "(":
                postFix += stack.pop()
            stack.pop()
       
        elif concReChar == "(":
            stack.append(concReChar)
        elif len(stack) == 0 or stack [-1] == "(" or compPrecedence(concReChar, stack[-1]):
            stack.append(concReChar)
        else:
            while len(stack) > 0 and stack [-1] != "(" and not compPrecedence (concReChar, stack[-1]):
                postFix+=stack.pop()
            stack.append(concReChar)
        i += 1

    while len(stack) > 0:
        postFix += stack.pop()

    return postFix



concatenatedRegex = addConcatenationSymbol (regex, regSize)
postFix = getPostFix (concatenatedRegex, len(concatenatedRegex))
print (concatenatedRegex)
print (postFix)