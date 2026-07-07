from typing import TypedDict, List
from langgraph.graph import StateGraph
from pathlib import Path

class AgentNode(TypedDict):
    name: str
    age: int
    skills: List[str]
    result: str

def first_node(state: AgentNode)-> AgentNode:
    print(f"{state['name']}, hello! this is your first node...")
    return state

def second_node(state: AgentNode)-> AgentNode:
    print(f"your age is {state['age']}")
    return state

def third_node(state: AgentNode)-> AgentNode:
    print(f"hey,{state['name']} your age is {state['age']}, your skills are...:")
    print(f" \n{state['skills']}")
    return state

graph = StateGraph(AgentNode)
graph.add_node("first_node",first_node)
graph.add_edge("first_node", "second_node")
graph.add_node("second_node", second_node)
graph.add_edge("second_node", "third_node")
graph.add_node("third_node", third_node)

graph.set_entry_point("first_node")
graph.set_finish_point("third_node")

app = graph.compile()

##=== creating image of that graph formed ==##
output_path = Path("images/multi-node-graph-three-nodes.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_bytes(app.get_graph().draw_mermaid_png())

result = app.invoke({"age":21, "result": "", "name": "Ankit", "skills":["Python", "Next-js","LangGraph", "LangChain", "PgVector"]})

print(result)
