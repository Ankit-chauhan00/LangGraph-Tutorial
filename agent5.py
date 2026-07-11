from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
import random
from pathlib import Path



class AgestState(TypedDict):
    name: str
    numbers: List[int]
    counter: int


def greeting_node(state: AgestState)-> AgestState:
    """Greeting Node which says hi to a person"""
    state["name"] = f"Hi There, {state['name']}"
    state["counter"] = 0

    return state

def random_node(state: AgestState)->AgestState:
    """Generating a number form 0 to 10"""
    state["numbers"].append(random.randint(0,10))
    state["counter"]+= 1

    return state

def loop_decider(state: AgestState):
    """Decides weather loop will Run"""
    if state["counter"] == 5:
        return "end"
    else :
        return "loop"

graph = StateGraph(AgestState)

graph.add_node("greeting_node", greeting_node)
graph.add_node("random_node", random_node)

graph.add_edge(START, "greeting_node")
graph.add_edge("greeting_node","random_node")

graph.add_conditional_edges(
    "random_node",
    loop_decider,
    {
        "end": END,
        "loop": "random_node"
    }
)
app = graph.compile()

##=== creating image of that graph formed ==##
output_path = Path("images/loop_graph.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_bytes(app.get_graph().draw_mermaid_png())

result = app.invoke({"counter": 0, "name": "Ankit", "numbers":[]})

print(result["numbers"])



