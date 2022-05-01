import jsonManager

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

def getPowerSet (nfaStates):
    powerSet = [[]]
    for state in nfaStates:
        for sub in powerSet:
            powerSet = powerSet + [list(sub)+ [state]]
    return powerSet

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

jsonManager.NFA = jsonManager.readJSONFile("NFA.json")
nfaStates = []
nfaTransitions = []
nfaSymbols = []
nfaAccepting = []

fillRequiredData(jsonManager.NFA)




