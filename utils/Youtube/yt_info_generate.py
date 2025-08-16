from config import settings
from langchain_core.messages import HumanMessage
from typing import Optional
from pydantic import BaseModel, Field

class YtInfo(BaseModel):
    yt_title: str = Field(..., description="YouTube title")
    yt_description: str = Field(..., description="YouTube description")
    yt_tags: Optional[list[str]] = Field(description="YouTube video tags")
    
class YTInformation:
    def __init__(self, llm):
        self.llm = llm
        self.structured_llm_yt = self.llm.with_structured_output(YtInfo)
        self.generate_yt_info = settings.YT_INFO_PROMPT
        
    def generate_yt_information(self, state):
        topic = state["user_topic"]
        script = state["script"]
        prompt = f"{self.generate_yt_info}\n\nTOPIC: {topic}\n\nSCRIPT: {script}"
        structured_response = self.structured_llm_yt.invoke(prompt)
        return {"yt_title": structured_response.yt_title, "yt_description": structured_response.yt_description, "yt_tags": structured_response.yt_tags}