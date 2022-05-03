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

def computeSimplifiedDFA(DFA):
    global dfaTransitions
    stateDict = dict()
    count = 1
    newDFA = {
        "StartingState": "S1",
    }
    for state in DFA:
        if (state == "StartingState"):
            continue
        else:
            stateDict [state] = count
            count += 1
    
    for state in DFA:
        if (state == "StartingState"):
            continue
        else:
            jsonManager.createNewState("S" + str(stateDict[state]), newDFA)
            for transition in DFA[state]:
                if transition == "IsTerminating":
                    if DFA[state]["IsTerminating"] == True:
                        newDFA["S" + str(stateDict[state])]["IsTerminating"] = True
                else:
                    for goState in DFA[state][transition]:
                        jsonManager.addTransition("S" + str(stateDict[state]), "S" + str(stateDict[goState]), transition, newDFA)
                        dfaTransitions.append(["S" + str(stateDict[state]),transition ,"S" + str(stateDict[goState])])
    
    newDFA["StartingState"]   = "S" + str(stateDict[DFA["StartingState"]])
    return newDFA

def setTerminatingNode(graph):

    for state in jsonManager.DFA:
        if (state != "StartingState"):
            if jsonManager.DFA[state]["IsTerminating"] == False:
                graph.attr('node', shape = 'circle')
                graph.node(state)
                if state == jsonManager.DFA["StartingState"]:
                    graph.attr('node', shape='none')
                    graph.node('')
                    graph.edge("", state)
            else:
                graph.attr('node', shape = 'doublecircle')
                graph.node(state)
                if state == jsonManager.DFA["StartingState"]:
                    graph.attr('node', shape='none')
                    graph.node('')
                    graph.edge("", state)

def setTransistions(graph):
    global dfaTransitions
    for transition in dfaTransitions:
        graph.edge(transition[0], transition[2], label=transition[1])
    

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
dfaTransitions = []
fillRequiredData(jsonManager.NFA)
nfaStatesDic = computeStateDict()

epsilonClosure = computeAllEpsilonClosure()
closureStack = [epsilonClosure["S1"]]


if (computeTerminatingDFA(closureStack[0])):
    
    jsonManager.createNewState(computeStateName(closureStack[0]), jsonManager.DFA)
    jsonManager.DFA[computeStateName(closureStack[0])]["IsTerminating"] = True
jsonManager.DFA["StartingState"] = computeStateName(closureStack[0])

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
                        jsonManager.createNewState(computeStateName(list(to)), jsonManager.DFA)
                        jsonManager.DFA[computeStateName(list(to))]["IsTerminating"] = True
                    
                jsonManager.addTransition(computeStateName(current), computeStateName(list(to)),nfaSymbols[symbol] ,jsonManager.DFA)

finiteGraph = Digraph(graph_attr={'rankdir': 'LR'})

jsonManager.DFA = computeSimplifiedDFA(jsonManager.DFA)
setTerminatingNode(finiteGraph)
setTransistions(finiteGraph)
jsonManager.createJSONFile(fileName, jsonManager.DFA)
finiteGraph.render(picFile, view =True, format= 'png', overwrite_source= True)

