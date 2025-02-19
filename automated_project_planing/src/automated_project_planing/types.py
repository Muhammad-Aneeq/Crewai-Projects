from typing import List
from pydantic import BaseModel

class TaskEstimate(BaseModel):
    task_name: str | None = None
    estimated_time_hours: float | None = None
    required_resources: List[str] = []

class Milestone(BaseModel):
    milestone_name: str | None = None
    tasks: List[str] = []

class ProjectPlan(BaseModel):
    tasks: List[TaskEstimate] = []
    milestones: List[Milestone] = []
