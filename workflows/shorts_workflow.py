from langgraph.graph import StateGraph, START, END
from langgraph.graph import add_messages
from typing import TypedDict, Annotated, Literal
from utils.Youtube.yt_info_generate import YTInformation
from utils.llm import build_llm
from utils.script_generator import ScriptGenerator

class ChatState(TypedDict):
    user_topic: str
    script: str
    yt_title:str
    yt_description: str
    yt_tags: list[str]
    evaluation: Literal["approved", "needs_improvements"]
    feedback: str
    iteration: int
    max_iteration: int
    feedback_history: Annotated[list[str], add_messages]

def workflow():
    graph = StateGraph(ChatState)
    llm = build_llm()
    script_gen = ScriptGenerator(llm)
    yt_info_gen = YTInformation(llm)
    graph.add_node("script_gen", script_gen.generate)
    graph.add_node("script_eval", script_gen.evaluate)
    graph.add_node("script_optimize", script_gen.optimize)
    graph.add_node("yt_info", yt_info_gen.generate_yt_information)
    graph.add_edge(START, "script_gen")
    graph.add_edge("script_gen", "script_eval")
    graph.add_conditional_edges("script_eval", script_gen.route_evaluation, {"approved": "yt_info", "needs_improvements": "script_optimize"})
    graph.add_edge("script_optimize", "script_eval")
    graph.add_edge("yt_info", END)
    return graph.compile()