from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List
import random
from pathlib import Path

class AgentState(TypedDict):
    player_name: str
    student_gusses:List[int]
    attempts: int
    lower_bound: int
    upper_bound: int
    correct_number: int


def set_bounds(state: AgentState)->AgentState:
    """
    SetUp the numbers lower bound, upper bound,
    and the correct number
    """
    state["lower_bound"] = 1
    state["upper_bound"] = 20
    state["correct_number"] = 7
    state["attempts"] = 0

    return state


def predict_number(state:AgentState) -> AgentState:
    """Predict the number from 1 to 20"""
    number = random.randint(1,20)
    state["student_gusses"].append(number)
    state["attempts"] = state["attempts"]+1

    return state


def check_number(state: AgentState) -> bool:
    guess = state["student_gusses"][-1]


    if guess == state["correct_number"]:
        return True

    if state["attempts"] >= 7:
        return True

    return False


graph = StateGraph(AgentState)
graph.add_node("set_up_node",set_bounds)
graph.add_node("prediction_node",predict_number)

graph.add_edge(START,"set_up_node")
graph.add_edge("set_up_node","prediction_node")

graph.add_conditional_edges(
     "prediction_node",
     check_number,
     {
          False: "prediction_node",
          True: END
     }
)
app = graph.compile()

##=== creating image of that graph formed ==##
output_path = Path("images/predict_number.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_bytes(app.get_graph().draw_mermaid_png())


result = app.invoke({
    "player_name": "Ankit Chauhan",
    "student_gusses": [],
    "attempts": 0,
    "lower_bound": 1,
    "upper_bound": 20,
    "correct_number": 0,
})

print(result)






