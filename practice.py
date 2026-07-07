from typing import TypedDict

from langgraph.graph import StateGraph


class AgentState(TypedDict):
    name: str
    message: str 


def apperitiate(state: AgentState) -> AgentState:
    state["name"]
    state["message"] = state["name"] + ", you are doing such a great job"

    return state


graph = StateGraph(AgentState)
graph.add_node("appeciate", apperitiate)
graph.set_entry_point("appeciate")
graph.set_finish_point("appeciate")

app = graph.compile()

result = app.invoke({"name": "Ankit", "message": ""})

print(result["message"])
