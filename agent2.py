from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str


def process_value(state: AgentState)->AgentState:
    """This function handles multiple different inputs"""

    state["result"] = f"Hi there {state['name']}! your sum = {sum(state['values'])}"
    return state


graph = StateGraph(AgentState)
graph.add_node("processor", process_value)
graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile() # compiling the graph
result = app.invoke({"values": [10, 5, 15,], "name": "Ankit", "result":""})

print(result["result"])