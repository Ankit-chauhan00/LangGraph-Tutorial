
from typing import Dict, TypedDict # type dictonary
from langgraph.graph import StateGraph # frame work that helps you to design and manage the flow of task in your application using a graph structure
from IPython.display import Image, display
from pathlib import Path

# we create the state of the agents Agentstate - shared data structure track of your application

class AgentState(TypedDict): # our state schema
    message: str



def greeting_node(state: AgentState)-> AgentState:
    """Simple node that adds a greetings message to the state"""
    state['message'] = "Hey" + state['message'] + ", how is your day going?"

    return state


#==== Graph Node =====##
graph  = StateGraph(AgentState)
graph.add_node("greeter", greeting_node)

graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app= graph.compile()


##=== creating image of that graph formed ==##
output_path = Path("images/graph.png")
output_path.parent.mkdir(parents=True, exist_ok=True)

png = app.get_graph().draw_mermaid_png()

output_path.write_bytes(app.get_graph().draw_mermaid_png())

print(f"Saved to: {output_path.resolve()}")