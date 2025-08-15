from config import settings
from langchain_core.messages import HumanMessage
from typing import Literal
from pydantic import BaseModel, Field


class ScriptEvaluation(BaseModel):
    evaluation: Literal["approved", "needs_improvements"] = Field(description="Final Evaluation result")
    feedback: str = Field(..., description="Feedback for the tweet.")


class ScriptGenerator:
    
    def __init__(self, llm):
        self.llm = llm
        self.structured_llm = self.llm.with_structured_output(ScriptEvaluation)
        self.script_system_prompt = settings.SCRIPT_SYS_PROMPT
        self.script_evaluate_prompt = settings.SCRIPT_EVALUATE_PROMPT
        self.script_optmize_promot = settings.SCRIPT_OPTIMIZE_PROMPT
        
    def generate(self, state):
        topic = state["user_topic"]
        prompt = f"{self.script_system_prompt}\n\nTopic: {topic}"
        response = self.llm.invoke(prompt)
        state["feedback_history"].append(HumanMessage(content=topic))
        return {"script": response.content, "feedback_history": [response]}
    
    def evaluate(self, state):
        script = state["script"]
        prompt = f"{self.script_evaluate_prompt}\n\nSCRIPT:\n{script}"
        structured_response = self.structured_llm.invoke(prompt)
        return {"evaluation": structured_response.evaluation, "feedback": structured_response.feedback}
    
    def optimize(self, state):
        topic = state["user_topic"]
        script = state["script"]
        feedback = state["feedback"]
        prompt  = f"{self.script_optmize_promot}\n\nTOPIC: {topic}\n\nSCRIPT: {script}\n\nFEEDBACK: {feedback}"
        response = self.llm.invoke(prompt)
        iteration = state["iteration"] + 1
        return {"script": response.content, "iteration" : iteration, "feed_history": [response]}
    
    def route_evaluation(self, state):
        if state["evaluation"] == "approved" or state["iteration"] >= state["max_iteration"]:
            return "approved"
        else:
            "needs_improvements"