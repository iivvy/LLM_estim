from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
class ProjectInput(BaseModel):
    project_description : str
    user_stories : list[str]