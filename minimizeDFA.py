import sys
from graphviz import Digraph
import jsonManager

def fillNFASymbols (DFA):
    global dfaSymbols
    for state in DFA:
        if (state == "StartingState"):
            continue
        else: 
            for transition in DFA[state]:
                if (transition == "IsTerminating"):
                    continue
                else:
                    
                    if (transition not in dfaSymbols):
                        dfaSymbols.append(transition)

def fillDFAStates (DFA):
    global dfaStates
    for state in DFA:
        if (state == "StartingState"):
            continue
        else: 
            dfaStates.append(state)
    
def fillDFA_Accepting (DFA):
    global dfaAccepting 
    for state in DFA:
        if (state == "StartingState"):
            continue
        else:
            if DFA[state]["IsTerminating"] == True:
                dfaAccepting.append(state)

def fillRequiredData (DFA):
    
    global dfaStates 
    global dfaAccepting 
    global dfaIntial
    global dfaSymbols

    dfaIntial = jsonManager.DFA["StartingState"]
    fillNFASymbols (DFA)
    fillDFAStates(DFA)
    fillDFA_Accepting(DFA)

def getReachableStates (DFA):

    global dfaIntial
    to = set()
    stack = list ()
    stack.append(dfaIntial) 
    while (len(stack) > 0):
        state = stack.pop(0)
        to.add(state)
        for state in DFA:
            if state == "StartingState":
                continue
            else:
                for transition in DFA[state]:
                    if transition == "IsTerminating":
                        continue
                    else: 
                        for endState in DFA[state][transition]:
                            if endState not in to:
                                stack.append(endState)
    return to

def getToStates (DFA, state):
    global dfaSymbols
    to = []
    for transition in DFA[state]:
        if (transition == "IsTerminating"):
            continue
        for end in DFA[state][transition]:
            to.append(end)

    return to

def checkGroup (end1, end2, stateToGroup):
    
    for i in range (len(end1)):
        if (stateToGroup[end1[i]] != stateToGroup[end2[i]]):    
            return False
    return True

def getTransitionValue (DFA, start, end):
    
    for transition in DFA[start]:
        if (transition == "IsTerminating"):
            continue
        for goState in DFA[start][transition]:


            if (goState == end):
                return transition

def createMinimizedDFA (DFA, MINDFA, groups, stateToGroup):
    global dfaAccepting
    global minTransitions
    global dfaIntial
    
    for group in groups:
        if (len(group) == 0):
            continue
        state = list(group.keys())[0]
        next = group[state]
        if state in dfaAccepting:
            jsonManager.createNewState("S" + str(stateToGroup[state]), MINDFA)
            MINDFA["S" + str(stateToGroup[state])]["IsTerminating"] = True
        if state == dfaIntial:
            MINDFA["StartingState"] = "S" + str(stateToGroup[state])
        for end in next:
            transition = getTransitionValue (DFA,state,end)
            jsonManager.addTransition("S" + str(stateToGroup[state]), "S" + str(stateToGroup[end]), transition, MINDFA)
            minTransitions.append(["S" + str(stateToGroup[state]), transition, "S" + str(stateToGroup[end])])
            if end in dfaAccepting:
                MINDFA["S" + str(stateToGroup[end])]["IsTerminating"] = True
            if end == dfaIntial:
                MINDFA["StartingState"] = "S" + str(stateToGroup[end])
            
def minimize (DFA, MINDFA):
    
    global dfaAccepting
    reachables = getReachableStates(DFA)
    groups = [{}, {}]
    stateToGroup = {}

    for state in reachables:
        if state in dfaAccepting:
            groups [1][state] = getToStates(DFA,state)
            stateToGroup[state] = 1
        else: 
            groups [0][state] = getToStates (DFA,state)
            stateToGroup[state] = 0
    while True: 
        minimized = False 
        newStateGroup = {}
        groupCount = 0
        for group in groups:
            done = set ()
            for state1, end1 in group.items():
                if state1 not in done:
                    newStateGroup[state1] = groupCount
                    for state2, end2 in group.items():
                        if state2 not in done:
                            if checkGroup(end1,end2,stateToGroup):
                                newStateGroup[state2] = groupCount
                                done.add(state2)
                            else:
                                minimized = True
                    done.add(state1)
                    groupCount += 1
        if not minimized:
            break
        else:
            stateToGroup = newStateGroup.copy()
            groups = []
        for i in range(groupCount):
            group = {}
            for state in reachables:
                if stateToGroup[state] == i:
                    group[state] = getToStates(DFA, state)
            groups.append(group)
    createMinimizedDFA (DFA, MINDFA, groups, stateToGroup)
        
def setTerminatingNode(graph):
    
    for state in jsonManager.minDFA:
        if (state != "StartingState"):
            if jsonManager.minDFA[state]["IsTerminating"] == False:
                graph.attr('node', shape = 'circle')
                graph.node(state)
                if state == jsonManager.minDFA["StartingState"]:
                    graph.attr('node', shape='none')
                    graph.node('')
                    graph.edge("", state)
            else:
                graph.attr('node', shape = 'doublecircle')
                graph.node(state)
                if state == jsonManager.minDFA["StartingState"]:
                    graph.attr('node', shape='none')
                    graph.node('')
                    graph.edge("", state)

def setTransistions(graph):
    global minTransitions
    for transition in minTransitions:
        graph.edge(transition[0], transition[2], label=transition[1])

dfaStates = []
dfaAccepting = []
dfaSymbols = []
dfaIntial = ""
minTransitions = []

file = "DFA.json"
fileName = "minDFA.json"
picFile = "minDFA"
if (len(sys.argv) == 6):
    file = sys.argv[2]
    fileName = sys.argv[4]
    picFile = sys.argv[5]

jsonManager.DFA = jsonManager.readJSONFile(file)
fillRequiredData(jsonManager.DFA)

minimize(jsonManager.DFA, jsonManager.minDFA)
finiteGraph = Digraph(graph_attr={'rankdir': 'LR'})
setTerminatingNode(finiteGraph)
setTransistions(finiteGraph)
jsonManager.createJSONFile(fileName, jsonManager.minDFA)
finiteGraph.render(picFile, view =True, format= 'png', overwrite_source= True)