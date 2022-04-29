import jsonManager


jsonManager.createNewState("S2", jsonManager.NFA)
jsonManager.addTransition("S2", "S0", "A", jsonManager.NFA)
jsonManager.createJSONFile("NFA.json", jsonManager.NFA)

