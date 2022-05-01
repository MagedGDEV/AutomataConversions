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


def addConcatenationSymbol(regex, regSize):

    concRegex = ""
    for i in range(regSize - 1):

        concRegex += regex[i]
        if regex[i] not in specialChar:
            if regex[i+1] not in specialChar or regex[i+1] == "(" or regex[i+1] == "[":
                concRegex += "."
        elif regex[i] == ")" and regex[i+1] == "(":
            concRegex += "."
        elif regex[i] == "]" and regex[i+1] == "[":
            concRegex += "."
        elif (regex[i] == "*" or regex[i] == "+") and (regex[i+1] == "(" or regex[i+1] == "["):
            concRegex += "."
        elif (regex[i] == "*" or regex[i] == "+") and regex[i+1] not in specialChar:
            concRegex += "."
        elif (regex[i] == ")" or regex[i] == "]") and regex[i+1] not in specialChar:
            concRegex += "."

    concRegex += regex[-1]
    return concRegex


def compPrecedence(first, second):
    precedence = ["|", ".", "+", "*"]
    return precedence.index(first) > precedence.index(second)


def getPostFix(concatenatedRegex, concSize):

    stack = []
    postFix = ""
    i = 0
    while i < concSize:
        concReChar = concatenatedRegex[i]
        if concReChar not in specialChar or concReChar == "*" or concReChar == "+" or concReChar == "[":
            if (concReChar == "["):
                for j in range(5):
                    postFix += concatenatedRegex[i+j]
                i += 4
            else:
                postFix += concReChar

        elif concReChar == ")":
            while len(stack) > 0 and stack[-1] != "(":
                postFix += stack.pop()
            stack.pop()

        elif concReChar == "(":
            stack.append(concReChar)
        elif len(stack) == 0 or stack[-1] == "(" or compPrecedence(concReChar, stack[-1]):
            stack.append(concReChar)
        else:
            while len(stack) > 0 and stack[-1] != "(" and not compPrecedence(concReChar, stack[-1]):
                postFix += stack.pop()
            stack.append(concReChar)
        i += 1

    while len(stack) > 0:
        postFix += stack.pop()

    return postFix


class RegexType:
    Character = 1
    Concatenate = 2
    OR = 3
    STAR = 4
    PLUS = 5


class State:
    def __init__(self):
        self.next_state = {}


class ExpressionTree:
    def __init__(self, charType, value=None):
        self.charType = charType
        self.value = value
        self.left = None
        self.right = None


def computeExpressionTree(postFix, postSize):

    stack = []
    i = 0
    while i < postSize:
        postChar = postFix[i]
        if postChar == "|":
            tree = ExpressionTree(RegexType.OR)
            tree.right = stack.pop()
            tree.left = stack.pop()
            stack.append(tree)
        elif postChar == ".":
            tree = ExpressionTree(RegexType.Concatenate)
            tree.right = stack.pop()
            tree.left = stack.pop()
            stack.append(tree)
        elif postChar == "*":
            tree = ExpressionTree(RegexType.STAR)
            tree.left = stack.pop()
            stack.append(tree)
        elif postChar == "+":
            tree = ExpressionTree(RegexType.STAR)
            tree.left = stack.pop()
            stack.append(tree)
        else:
            value = ""
            if (postChar == "["):
                if (postChar == "["):
                    for j in range(5):
                        value += postFix[i+j]
                i += 4
                print (value)
                stack.append(ExpressionTree(RegexType.Character, value))
            else:
                stack.append(ExpressionTree(RegexType.Character, postChar))
        i += 1
    return stack[0]


regex = sys.argv[2]

concatenatedRegex = addConcatenationSymbol(regex, len(regex))
postFix = getPostFix(concatenatedRegex, len(concatenatedRegex))
expTree = computeExpressionTree(postFix, len(postFix))
