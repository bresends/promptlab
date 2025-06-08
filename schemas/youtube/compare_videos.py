from pydantic import BaseModel, Field
from typing import List, Literal

class VideoComparisonResponse(BaseModel):
    detailed_analysis: str = Field(
        description="A comprehensive analysis of the similarities and differences between the two video summaries.",
    )
    reasoning: str = Field(
        description="A detailed explanation of the reasoning that led to the similarity score.",
    )
    first_video_unique_points: List[str] = Field(
        description="A list of key points or features that are unique to the first video if any.",
    )
    second_video_unique_points: List[str] = Field(
        description="A list of key points or features that are unique to the second video if any.",
    )
    similarity_score: float = Field(
        ge=0,
        le=1,
        description="A score from 0 to 1 indicating how similar the two videos are.",
    )
    recommendation: str = Field(
        description="A recommendation on whether the user should watch both videos or just one, with justification.",
    )
    selected_video: Literal["first_video", "second_video", "both"] = Field(
        description="Indicates which video(s) the user should watch."
    )