if state == jsonManager.minDFA["StartingState"]:
                    graph.attr('node', shape='none')
                    graph.node('')
                    graph.edge("", state)