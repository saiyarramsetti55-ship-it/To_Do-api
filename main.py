from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Todo Task Manager API")

tasks = {}
task_counter = 0


class Task(BaseModel):
    title: str
    priority: str = "medium"
    completed: bool = False


@app.post("/tasks")
def create_task(task: Task):
    global task_counter

    task_counter += 1

    tasks[task_counter] = task.model_dump()

    return {
        "id": task_counter,
        "message": "Task created",
        "task": tasks[task_counter]
    }


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):

    if task_id not in tasks:
        return {"error": "Task not found"}

    tasks[task_id] = task.model_dump()

    return {
        "id": task_id,
        "message": "Task updated",
        "task": tasks[task_id]
    }