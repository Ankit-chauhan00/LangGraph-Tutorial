from pathlib import Path
from typing import TypedDict, Union

from langgraph.graph import END, START, StateGraph


class AgentState(TypedDict):
    num1: int
    operation1: str
    num2: int

    num3: int
    operation2: str
    num4: int

    finalNumber1: Union[float, int]
    finalNumber2: Union[float, int]


def operation(a: int, b: int, operation: str):
    match operation:
        case "+":
            return a + b
        case "-":
            return a - b
        case "*":
            return a * b
        case "/":
            return a / b
        case _:
            raise ValueError(f"Invalid Error: {operation}")


def router1(state: AgentState) -> AgentState:
    return state


def router2(state: AgentState) -> AgentState:
    return state


def add_node(state: AgentState) -> AgentState:
    state["finalNumber1"] = operation(state["num1"], state["num2"], state["operation1"])
    return state


def sub_node(state: AgentState) -> AgentState:
    state["finalNumber1"] = operation(state["num1"], state["num2"], state["operation1"])
    return state


def prod_node(state: AgentState) -> AgentState:
    state["finalNumber1"] = operation(state["num1"], state["num2"], state["operation1"])
    return state


def div_node(state: AgentState) -> AgentState:
    state["finalNumber1"] = operation(state["num1"], state["num2"], state["operation1"])
    return state


def router1_decider(state: AgentState):
    match state["operation1"]:
        case "+":
            return "add"
        case "-":
            return "sub"
        case "*":
            return "mul"
        case "/":
            return "div"


def add_node2(state: AgentState) -> AgentState:
    state["finalNumber2"] = operation(state["num3"], state["num4"], state["operation2"])
    return state


def sub_node2(state: AgentState) -> AgentState:
    state["finalNumber2"] = operation(state["num3"], state["num4"], state["operation2"])
    return state


def prod_node2(state: AgentState) -> AgentState:
    state["finalNumber2"] = operation(state["num3"], state["num4"], state["operation2"])
    return state


def div_node2(state: AgentState) -> AgentState:
    state["finalNumber2"] = operation(state["num3"], state["num4"], state["operation2"])
    return state


def router2_decider(state: AgentState):
    match state["operation2"]:
        case "+":
            return "add"
        case "-":
            return "sub"
        case "*":
            return "mul"
        case "/":
            return "div"


graph = StateGraph(AgentState)

graph.add_node("router1", router1)
graph.add_edge(START, "router1")

graph.add_node("add_node1", add_node)
graph.add_node("sub_node1", sub_node)
graph.add_node("prod_node1", prod_node)
graph.add_node("div_node1", div_node)


graph.add_conditional_edges(
    "router1",
    router1_decider,
    {"add": "add_node1", "sub": "sub_node1", "mul": "prod_node1", "div": "div_node1"},
)

graph.add_edge("add_node1", "router2")
graph.add_edge("sub_node1", "router2")
graph.add_edge("prod_node1", "router2")
graph.add_edge("div_node1", "router2")

graph.add_node("router2", router2)
graph.add_node("add_node2", add_node2)
graph.add_node("sub_node2", sub_node2)
graph.add_node("prod_node2", prod_node2)
graph.add_node("div_node2", div_node2)


graph.add_conditional_edges(
    "router2",
    router2_decider,
    {"add": "add_node2", "sub": "sub_node2", "mul": "prod_node2", "div": "div_node2"},
)


graph.add_edge("add_node2", END)
graph.add_edge("sub_node2", END)
graph.add_edge("prod_node2", END)
graph.add_edge("div_node2", END)

app = graph.compile()

##=== creating image of that graph formed ==##
output_path = Path("images/conditional_graph_complex.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_bytes(app.get_graph().draw_mermaid_png())

result = app.invoke(
    {
        "num1": 10,
        "num2": 20,
        "num3": 2,
        "num4": 30,
        "finalNumber1": 0,
        "finalNumber2": 0,
        "operation1": "+",
        "operation2": "-",
    }
)


print(result)
