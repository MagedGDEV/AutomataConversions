import json
from tokenize import String
from typing import Dict

# This file is code that deals with json file
# create, insert, modify

NFA = {
    "StartingState": "S1",
    "S1": {
        "IsTerminating": False,
    }
}

def addTransition(currentState: String, goingState: String, transition: String, stateData: Dict):

    # add the new state if it's not available 
    createNewState(currentState, stateData)

    state = stateData[currentState]
    # check if the transition is not available
    if state.get(transition) != None:
        # if transition is not available
        state[transition].append(goingState)

    else:
        # if transition not available
        state.update({transition: [goingState]})


def createNewState(state: String, stateData: Dict):
    # check if the state is not available
    if stateData.get(state) != None:
        # if available return
        return
    else:
        # not available create the new state
        stateData.update({state: {"IsTerminating": False}})
        #NFA[state].update({"IsTerminating": False})
        pass


def createJSONFile(fileName: String, stateData: Dict): 
    with open(fileName, "w") as outfile:
        json.dump(stateData, outfile, indent= 4)

