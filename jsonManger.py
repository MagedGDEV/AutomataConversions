import json
from tokenize import String

# This file is code that deals with json file
# create, insert, modify

NFA = {
    "StartingState": "S0",
    "S0": {
        "IsTerminating": False,
    }
}


#NFA["S0"].update ({"a": ["S1", "S2"]})

def addTransition(currentState: String, goingState: String, transition: String):

    state = NFA[currentState]
    # check if the transition is not available
    if state.get(transition) != None:
        # if transition is not available
        state[transition].append(goingState)

    else:
        # if transition not available
        state.update({transition: [goingState]})


def createNewState(state: String):
    # check if the state is not available
    if NFA.get(state) != None:
        # if available return
        return
    else:
        # not available create the new state
        NFA.update({state: {"IsTerminating": False}})
        #NFA[state].update({"IsTerminating": False})
        pass

createNewState("S2")
addTransition('S0', 'S3', 'b')
addTransition ('S0', 'S3', 'c')
addTransition('S0', 'S4', 'b')
addTransition('S2', 'S3', 'b')

with open("NFA.json", "w") as outfile:
    json.dump(NFA, outfile)
