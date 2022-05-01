import jsonManager

def fillNFAStates (states):
    global nfaStates
    for state in states:
        if (state == "StartingState"):
            continue
        else: 
            nfaStates.append(state)
    

def getPowerSet (nfaStates):
    powerSet = [[]]
    for state in nfaStates:
        for sub in powerSet:
            powerSet = powerSet + [list(sub)+ [state]]
    return powerSet



jsonManager.NFA = jsonManager.readJSONFile("NFA.json")
nfaStates = []
fillNFAStates(jsonManager.NFA)
dfaPStates = getPowerSet(nfaStates)


