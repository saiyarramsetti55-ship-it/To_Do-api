from fastapi import FastAPI, HTTPException
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

# GET — get all tasks
@app.get("/tasks")
def get_all_tasks():
    return {
        "count": len(tasks),
        "tasks": tasks
    }



# GET — get one task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    return {
        "id": task_id,
        "task": tasks[task_id]
    }

    
# PUT — update a task completely
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):

    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    tasks[task_id] = task.model_dump()

    return {
        "id": task_id,
        "message": "Task updated successfully",
        "task": tasks[task_id]
    }

# PATCH — mark a task as completed
@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int):

    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    tasks[task_id]["completed"] = True

    return {
        "id": task_id,
        "message": "Task marked as completed",
        "task": tasks[task_id]
    }

# DELETE — delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    deleted_task = tasks.pop(task_id)

    return {
        "id": task_id,
        "message": "Task deleted successfully",
        "task": deleted_task
    }



# GET — get tasks by priority
@app.get("/tasks/priority/{level}")
def get_tasks_by_priority(level: str):

    if level not in ["low", "medium", "high"]:
        raise HTTPException(
            status_code=400,
            detail="Priority must be low, medium, or high"
        )

    filtered_tasks = {
        task_id: task
        for task_id, task in tasks.items()
        if task["priority"] == level
    }

    return {
        "priority": level,
        "count": len(filtered_tasks),
        "tasks": filtered_tasks
    }    