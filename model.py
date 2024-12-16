from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,Field
class ProjectInput(BaseModel):
    project_description : str
    user_stories : list[str]


class LLMResponse(BaseModel):
    duration: float = Field(..., description="Estimated duration in years")
    cost: int = Field(..., description="Estimated cost in dollars")
    explanation: str
