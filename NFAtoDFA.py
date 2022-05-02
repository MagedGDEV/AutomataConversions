import sys
import jsonManager
from graphviz import Digraph

def fillNFAStates (NFA):
    global nfaStates
    for state in NFA:
        if (state == "StartingState"):
            continue
        else: 
            nfaStates.append(state)
    
def fillNFATransitions(NFA):

    global nfaTransitions
    for state in NFA:
        if (state == "StartingState"):
            continue
        else:
            for transition in NFA[state]:
                if (transition == "IsTerminating"):
                    continue
                else:
                    for endState in NFA[state][transition]:
                        nfaTransitions.append([state, transition, endState])

def fillNFASymbols (NFA):
    global nfaSymbols
    for state in NFA:
        if (state == "StartingState"):
            continue
        else: 
            for transition in NFA[state]:
                if (transition == "IsTerminating"):
                    continue
                else:
                    
                    if (transition not in nfaSymbols):
                        nfaSymbols.append(transition)

def fillNFA_Accepting (NFA):
    global nfaAccepting 
    for state in NFA:
        if (state == "StartingState"):
            continue
        else:
            if NFA[state]["IsTerminating"] == True:
                nfaAccepting.append(state)

def fillRequiredData (NFA):
    
    global nfaStates
    global nfaTransitions
    global nfaSymbols 
    global nfaAccepting 

    fillNFATransitions(NFA)
    fillNFAStates(NFA)
    fillNFASymbols(NFA)
    fillNFA_Accepting(NFA)

def computeStateDict ():
    global nfaStates
    nfaStateDic = dict()
    for i in range(len(nfaStates)):
        nfaStateDic [nfaStates[i]] = i
    return nfaStateDic

def computeStateEpsilonClosure (state): 
    global nfaTransitions
    global nfaStatesDic
    visited = dict()  
    visited[nfaStatesDic[state]] = 0
    next = [nfaStatesDic[state]]

    while (len(next) > 0):

        current = next.pop(0)
        
        for transition in nfaTransitions:
            
            if current == nfaStatesDic[transition[0]] and transition[1] == "epsilon":
                
                if nfaStatesDic[transition[2]] not in visited.keys():
                    visited[nfaStatesDic[transition[2]]] = 0
                    next.append(nfaStatesDic[transition[2]])
        visited[current] = 1
    return visited.keys()

def computeAllEpsilonClosure():
    global nfaStates
    global nfaStatesDic
    epsilonClosure = dict()
    for state in nfaStates:
        epsilonClosure [state] = list(computeStateEpsilonClosure(state))
    return epsilonClosure

def computeTerminatingDFA(closure):
    global nfaAccepting
    global nfaStates
    for state in closure:
        if nfaStates[state] in nfaAccepting:
            return True
    return False

def getAllStateWithTransition(state, Stransition):
    global nfaTransitions
    global nfaStatesDic
    states = []
    for transition in nfaTransitions:
        if state == transition[0] and Stransition == transition[1]:
            states.append(nfaStatesDic[transition[2]])

    return states

def computeStateName (state):
    global nfaStates
    stateName = ""
    for s in state:
        stateName += nfaStates[s]
    return stateName

file = "NFA.json"
fileName = "DFA.json"
picFile = "DFA"
if (len(sys.argv) == 6):
    file = sys.argv[2]
    fileName = sys.argv[4]
    picFile = sys.argv[5]

jsonManager.NFA = jsonManager.readJSONFile(file)
nfaStates = []
nfaTransitions = []
nfaSymbols = []
nfaAccepting = []
fillRequiredData(jsonManager.NFA)
nfaStatesDic = computeStateDict()

epsilonClosure = computeAllEpsilonClosure()
closureStack = [epsilonClosure["S1"]]
finiteGraph = Digraph(graph_attr={'rankdir': 'LR'})

if (computeTerminatingDFA(closureStack[0])):
    finiteGraph.attr('node', shape = 'doublecircle')
else:
    finiteGraph.attr('node', shape = 'circle')
finiteGraph.node(computeStateName(closureStack[0]))
jsonManager.createNewState(computeStateName(closureStack[0]), jsonManager.DFA)

finiteGraph.attr ('node', shape = 'none')
finiteGraph.node('')
finiteGraph.edge('',computeStateName(closureStack[0]))

dfaStates = list ()
dfaStates.append(epsilonClosure["S1"])

while (len(closureStack)> 0):
    
    current = closureStack.pop(0)
    
    for symbol in range(len(nfaSymbols)):
        if (nfaSymbols[symbol] == "epsilon"):
            continue
        else:
            fromClosure = set()
            for state in current:
                fromClosure.update(set(getAllStateWithTransition(nfaStates[state], nfaSymbols[symbol])))
             
            if (len(fromClosure) > 0):
                to = set ()
                for state in list(fromClosure):
                    to.update (set(epsilonClosure[nfaStates[state]]))
                
                if list(to) not in dfaStates:
                    dfaStates.append(list(to))
                    closureStack.append(list(to))

                    if (computeTerminatingDFA(list(to))):
                        finiteGraph.attr('node', shape = 'doublecircle')
                    else:
                        finiteGraph.attr('node', shape = 'circle')
                    finiteGraph.node(computeStateName(list(to)))
                finiteGraph.edge (computeStateName(current), computeStateName(list(to)), label= nfaSymbols[symbol])
                jsonManager.addTransition(computeStateName(current), computeStateName(list(to)),nfaSymbols[symbol] ,jsonManager.DFA)

jsonManager.createJSONFile(fileName, jsonManager.DFA)
finiteGraph.render(picFile, view =True, format= 'png', overwrite_source= True)

