if state1 == "S1":
                                    del minimized[state2]
                                    changeState (minimized, state2, state1)
                                    if state2 in dfaAccepting:
                                        dfaAccepting.remove(state2)