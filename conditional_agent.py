from typing import TypedDict, Dict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from pathlib import Path

class Agentstate(TypedDict):
    num1: int
    operation: str
    num2: int
    finalNumber: int

def adder(state: Agentstate)-> Agentstate:
    state['finalNumber'] = state['num1'] + state['num2']
    return state

def product(state: Agentstate)->Agentstate:
    state["finalNumber"] = state['num1'] * state['num2']
    return state

def subtract(state: Agentstate)->Agentstate:
    state['finalNumber'] = state['num1'] - state['num2']
    return state

def decide_node(state: Agentstate):
    """This node will select the next node of the graph"""
    if state['operation'] =="+":
        return "addition_operation"
    elif state['operation'] == "-":
        return "subtraction_operation"
    else :
        return "default_operation"


def operation_decider(state: Agentstate):
    return state

graph = StateGraph(Agentstate)

graph.add_node("add_node", adder)
graph.add_node("sub_node",subtract)
graph.add_node("default_node", product)
graph.add_node("operation_decider", operation_decider)

graph.add_edge(START,"operation_decider")

graph.add_conditional_edges(
    "operation_decider", # First argument --> Node 
    decide_node, # Actual function that decides and return a value 
    {
        # Edge: Node
        "addition_operation": "add_node",
        "subtraction_operation": "sub_node",
        "default_operation": "default_node"
    }
)

graph.add_edge("add_node",END)
graph.add_edge("sub_node", END)
graph.add_edge("default_node", END)

app = graph.compile()


##=== creating image of that graph formed ==##
output_path = Path("images/conditional_graph.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_bytes(app.get_graph().draw_mermaid_png())

result = app.invoke({"num1": 1, "operation": "+", "num2": 10, "finalNumber":0})

print(result["finalNumber"])

