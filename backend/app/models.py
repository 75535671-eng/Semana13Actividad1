from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool | None = None


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str
    completed: bool


class MessageCreate(BaseModel):
    user: str = Field(..., min_length=1, max_length=100)
    text: str = Field(..., min_length=1, max_length=500)


class MessageResponse(BaseModel):
    id: str
    user: str
    text: str
    timestamp: float | None = None
