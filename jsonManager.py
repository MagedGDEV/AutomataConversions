import json
from tokenize import String
from typing import Dict




NFA = {
    "StartingState": "S1",
    "S1": {
        "IsTerminating": False,
    }
}

DFA = {
    "StartingState": "S1",
}

minDFA = {
    "StartingState": "S1",
}

def addTransition(currentState: String, goingState: String, transition: String, stateData: Dict):

    # add the new state if it's not available 
    createNewState (goingState,stateData)
    createNewState(currentState, stateData)
    state = stateData[currentState]
    # check if the transition is not available
    if state.get(transition) != None:
        # if transition is not available
        for end in state[transition]:
            if (end == goingState):
                return 
        state[transition].append(goingState)

    else:
        # if transition not available
        state.update({transition: [goingState]})

def createNewState(state: String, stateData: Dict):
   
    if stateData.get(state) != None:
        return
    else:
        stateData.update({state: {"IsTerminating": False}})


def createJSONFile(fileName: String, stateData: Dict): 
    with open(fileName, "w") as outfile:
        json.dump(stateData, outfile, indent= 4)

def readJSONFile (fileName):
    file = open (fileName, "r")
    inData = json.loads(file.read())
    return inData