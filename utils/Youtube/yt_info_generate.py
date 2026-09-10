import base64
import re
from pathlib import Path

from config import settings
from pydantic import BaseModel, Field
from typing import Optional

from utils.llm import build_image_llm


class YtInfo(BaseModel):
    yt_title: str = Field(..., description="YouTube title")
    yt_description: str = Field(..., description="YouTube description")
    yt_tags: Optional[list[str]] = Field(
        default=None,
        description="YouTube video tags"
    )


class YtThumbnail(BaseModel):
    yt_thumbnail: str = Field(
        ...,
        description="A detailed image-generation prompt for the YouTube thumbnail"
    )


class YTInformation:
    def __init__(self, llm):
        self.llm = llm

        self.structured_llm_yt = self.llm.with_structured_output(YtInfo)
        self.structured_llm_thumbnail = self.llm.with_structured_output(YtThumbnail)
        self.image_llm = build_image_llm()

        self.generate_yt_info = settings.YT_INFO_PROMPT
        self.generate_thumbnail = settings.THUMBNAIL_PROMPT

    def generate_yt_information(self, state):
        topic = state["user_topic"]
        script = state["script"]

        prompt = (
            f"{self.generate_yt_info}\n\n"
            f"TOPIC: {topic}\n\n"
            f"SCRIPT: {script}"
        )

        structured_response = self.structured_llm_yt.invoke(prompt)

        return {
            "yt_title": structured_response.yt_title,
            "yt_description": structured_response.yt_description,
            "yt_tags": structured_response.yt_tags,
        }

    def generate_yt_thumbnail(self, state):
        topic = state["user_topic"]
        script = state["script"]

        prompt = (
            f"{self.generate_thumbnail}\n\n"
            f"TOPIC: {topic}\n\n"
            f"SCRIPT: {script}"
        )

        structured_response = self.structured_llm_thumbnail.invoke(prompt)

        return {
            "yt_thumbnail": structured_response.yt_thumbnail
        }

    def generate_thumbnail_image(self, state, output_dir="Data/thumbnails"):
        image_prompt = self.generate_yt_thumbnail(state)["yt_thumbnail"]

        response = self.image_llm.invoke(image_prompt)

        image_url = None
        for block in response.content:
            if isinstance(block, dict) and block.get("type") == "image_url":
                image_url = block["image_url"]["url"]
                break

        if image_url is None:
            raise ValueError("The model did not return an image for the thumbnail prompt")

        match = re.match(r"data:image/(\w+);base64,(.*)", image_url, re.DOTALL)
        image_format, b64_data = match.group(1), match.group(2)

        topic_slug = re.sub(r"[^a-zA-Z0-9]+", "_", state["user_topic"]).strip("_")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        thumbnail_path = Path(output_dir) / f"{topic_slug}.{image_format}"
        thumbnail_path.write_bytes(base64.b64decode(b64_data))

        return {
            "yt_thumbnail": image_prompt,
            "thumbnail_path": str(thumbnail_path)
        }