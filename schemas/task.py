from pydantic import BaseModel, ConfigDict

class TaskCreate(BaseModel):
    title: str
    priority: str = "medium"
    completed: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)
