from colorama import Style
import jsonManager
import sys
from graphviz import Digraph

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
            tree = ExpressionTree(RegexType.PLUS)
            tree.left = stack.pop()
            stack.append(tree)
        else:
            value = ""
            if (postChar == "["):
                for j in range(5):
                    value += postFix[i+j]
                i += 4
                
                stack.append(ExpressionTree(RegexType.Character, value))
            else:
                stack.append(ExpressionTree(RegexType.Character, postChar))
        i += 1
    return stack[0]

def doConcatenation(expTree):
    
    leftNFA = computeRegex(expTree.left)
    rightNFA = computeRegex(expTree.right)

    leftNFA[1].next_state["epsilon"] = [rightNFA[0]]
    return leftNFA[0], rightNFA[1]

def doOR(expTree):
    
    start = State()
    end = State()

    firstNFA = computeRegex(expTree.left)
    secondNFA = computeRegex(expTree.right)

    start.next_state["epsilon"] = [firstNFA[0], secondNFA[0]]
    firstNFA[1].next_state["epsilon"] = [end]
    secondNFA[1].next_state["epsilon"] = [end]
    return start, end

def doSTAR (expTree):

    start = State()
    end = State()

    starred_nfa = computeRegex(expTree.left)

    start.next_state["epsilon"] = [starred_nfa[0], end]
    starred_nfa[1].next_state["epsilon"] = [starred_nfa[0], end]

    return start, end
    
def doPLUS (expTree):
    start = State()
    end = State()

    starred_nfa = computeRegex(expTree.left)

    start.next_state["epsilon"] = [starred_nfa[0]]
    starred_nfa[1].next_state["epsilon"] = [starred_nfa[0], end]

    return start, end

def doChar (expTree):
    start = State ()
    end = State()
    start.next_state[expTree.value] = [end]
    return start, end

def computeRegex (expTree):

    if expTree.charType == RegexType.Concatenate:
        return doConcatenation(expTree)
    elif expTree.charType == RegexType.OR:
        return doOR(expTree)
    elif expTree.charType == RegexType.STAR:
        return doSTAR(expTree)
    elif expTree.charType == RegexType.PLUS:
        return doPLUS(expTree)
    else: 
        return doChar(expTree)

def arrangeNFA(computedRegex):
    
    global transitions
    transitions = []

    arrangeTransitions(computedRegex[0], [], {computedRegex[0] : 1})
    isTerminating() 

def isTerminating ():
    global transitions
    
    for state in jsonManager.NFA:
        if (len (jsonManager.NFA[state]) == 1):
            jsonManager.NFA[state]["IsTerminating"] = True
           
def arrangeTransitions (state, statesDone, symbolTable):

    global transitions
    if state in statesDone : 
        return
    statesDone.append (state)

    for symbol in list (state.next_state):
        for nextSymbol in state.next_state[symbol]:
            if nextSymbol not in symbolTable:
                symbolTable[nextSymbol] = sorted(symbolTable.values())[-1] + 1
                jsonManager.createNewState ("S" + str (symbolTable[nextSymbol]), jsonManager.NFA)
            transitions.append (["S" + str (symbolTable[state]), symbol, "S" + str (symbolTable[nextSymbol])])
            jsonManager.addTransition ("S" + str (symbolTable[state]), "S" + str (symbolTable[nextSymbol]), symbol, jsonManager.NFA)
            arrangeTransitions (nextSymbol, statesDone, symbolTable)

def setTerminatingNode(graph):
    for state in jsonManager.NFA:
        if (state != "StartingState"):
            if jsonManager.NFA[state]["IsTerminating"] == False:
                graph.attr('node', shape = 'circle')
                graph.node(state)
                if state == 'S1':
                    graph.attr('node', shape='none')
                    graph.node('')
                    graph.edge("", state)
            else:
                graph.attr('node', shape = 'doublecircle')
                graph.node(state)

def setTransistions(graph):
    global transitions
    for transition in transitions:
        graph.edge(transition[0], transition[2], label=('ε', transition[1])[transition[1] != 'epsilon'])
        


regex = sys.argv[2]

concatenatedRegex = addConcatenationSymbol(regex, len(regex))
postFix = getPostFix(concatenatedRegex, len(concatenatedRegex))
expTree = computeExpressionTree(postFix, len(postFix))
computedRegex = computeRegex(expTree)
arrangeNFA(computedRegex)
jsonManager.createJSONFile ("NFA.json", jsonManager.NFA)

finiteGraph = Digraph(graph_attr={'rankdir': 'LR'})

setTerminatingNode (finiteGraph)
setTransistions(finiteGraph)
finiteGraph.render("NFA", view =True, format= 'png', overwrite_source= True)