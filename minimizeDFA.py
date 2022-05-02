import copy
import sys
from graphviz import Digraph
import jsonManager


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

    fillDFAStates(DFA)
    fillDFA_Accepting(DFA)

def changeState (DFA, state1, state2):

    for state in DFA:
        if (state == "StartingState"):
            continue
        else:
            for transition in DFA[state]:
                if transition == "IsTerminating":
                    continue     
                else:
                    if state1 == DFA[state][transition]:
                        DFA[state1].update ({transition: state2})
    if (state2 == DFA["StartingState"]):
        DFA["StartingState"] = state1
    DFA[state1] = DFA.pop(state2)
          
def  minimizeDFA(DFA):
    
    global dfaStates
    global dfaAccepting
    global dfaIntial
    removed = []
    minimized = copy.deepcopy(DFA)
    changed = True
    
    while (changed):
        changed = False
        for state1 in DFA:
            for state2 in DFA:
                if state1 != state2 and state1 in minimized and state2 in minimized:
                    if minimized[state1] == minimized[state2]:
                        if state2 not in removed and state1 not in removed:
                            if (state2 in dfaAccepting and state1 in dfaAccepting) or (state2 not in dfaAccepting and state1 not in dfaAccepting):
                                
                                removed.append(state1)
                                removed.append(state2)
                                changed = True
                                
                                if state1 in dfaIntial:
                                    del minimized[state2]
                                    changeState (minimized, state2, state1)
                                    if state2 in dfaAccepting:
                                        dfaAccepting.remove(state2)
                                elif state2 in dfaIntial:
                                    del minimized[state1]
                                    changeState (minimized, state1, state2)
                                    if state1 in dfaAccepting:
                                        dfaAccepting.remove(state1)
                                else:
                                    del minimized[state2]
                                    changeState (minimized, state2, state1)
                                    if state2 in dfaAccepting:
                                        dfaAccepting.remove(state2)
    return minimized

def fillMINTransitions(MIN):
    
    global minTransitions
    for state in MIN:
        if (state == "StartingState"):
            continue
        else:
            for transition in MIN[state]:
                if (transition == "IsTerminating"):
                    continue
                else:
                    for endState in MIN[state][transition]:
                        minTransitions.append([state, transition, endState])

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

def setTransistions(graph):
    global minTransitions
    for transition in minTransitions:
        graph.edge(transition[0], transition[2], label=transition[1])

dfaStates = []
dfaAccepting = []
dfaIntial = ["S1"]
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
jsonManager.minDFA = minimizeDFA(jsonManager.DFA)
print (jsonManager.minDFA)
jsonManager.createJSONFile(fileName, jsonManager.minDFA)
fillMINTransitions(jsonManager.minDFA)
print (minTransitions)
finiteGraph = Digraph(graph_attr={'rankdir': 'LR'})
setTerminatingNode(finiteGraph)
setTransistions(finiteGraph)
jsonManager.createJSONFile(fileName, jsonManager.minDFA)
finiteGraph.render(picFile, view =True, format= 'png', overwrite_source= True)