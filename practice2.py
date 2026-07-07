from typing import TypedDict, List
from langgraph.graph import StateGraph
from math import prod

class AgentClass(TypedDict):
    numbers : List[int]
    name: str
    operation: str
    result: str


def Condition_node(state: AgentClass)-> AgentClass:
    if state["operation"] == "+":
        state["result"] = f"{state['name']} , the addition of the numbers is {sum(state['numbers'])}"
    elif state["operation"] == '*':
        state["result"] = f"{state['name']} , the multiplication of the number is {prod(state['numbers'])}"
    else: 
        state["result"] = f"Invalid operation {state['operation']} on addition and multiplication supported "  

    return state
    
    
graph = StateGraph(AgentClass)
graph.add_node("conditional-node",Condition_node )
graph.set_entry_point("conditional-node")
graph.set_finish_point("conditional-node")
app =  graph.compile()

result = app.invoke({"name":"Ankit", "numbers": [1,3,3,4], "operation": "*", "result": ""})

print(result["result"])
