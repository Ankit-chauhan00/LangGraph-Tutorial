from typing import TypedDict
from langgraph.graph import StateGraph
from IPython.display import Image, display
from pathlib import Path



class AgentState(TypedDict):
    name: str
    age: int
    result: str


def first_node(state: AgentState) -> AgentState:
    """This is the first nod eof our sequence"""
    state["result"] = f"Hi {state['name']}!"
    return state


def second_node(state: AgentState) -> AgentState:
    """This is the second state of our sequence"""
    state["result"] = (
        f"{state['name']}, you are at second node and age is {state['age']}"
    )
    return state


graph = StateGraph(AgentState)
graph.add_node("first-node", first_node)
graph.add_node("second-node", second_node)
graph.set_entry_point("first-node")

graph.add_edge("first-node", "second-node")

graph.set_finish_point("second-node")
app = graph.compile()


##=== creating image of that graph formed ==##
output_path = Path("images/multi-node-graph.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_bytes(app.get_graph().draw_mermaid_png())

result = app.invoke({"age": 21, "result": "", "name": "Ankit"})

print(result)

