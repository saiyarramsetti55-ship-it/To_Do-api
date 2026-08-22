from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database.database import engine, get_db, Base
import models
import schemas

# Create the database tables on startup if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo Task Manager API")


# POST — create a new task
@app.post("/tasks")
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(
        title=task.title,
        priority=task.priority,
        completed=task.completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return {
        "id": db_task.id,
        "message": "Task created",
        "task": {
            "title": db_task.title,
            "priority": db_task.priority,
            "completed": db_task.completed
        }
    }


# GET — get all tasks
@app.get("/tasks")
def get_all_tasks(db: Session = Depends(get_db)):
    db_tasks = db.query(models.Task).all()
    
    # Format tasks as a dictionary with task.id as the key to match original response format
    tasks_dict = {
        str(task.id): {
            "title": task.title,
            "priority": task.priority,
            "completed": task.completed
        }
        for task in db_tasks
    }

    return {
        "count": len(db_tasks),
        "tasks": tasks_dict
    }


# GET — task statistics
@app.get("/tasks/stats")
def get_task_stats(db: Session = Depends(get_db)):
    total_tasks = db.query(models.Task).count()
    completed_tasks = db.query(models.Task).filter(models.Task.completed == True).count()
    pending_tasks = db.query(models.Task).filter(models.Task.completed == False).count()

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks
    }


# GET — search tasks by title (placed before /{task_id} to avoid conflicts)
@app.get("/tasks/search")
def search_tasks(keyword: str, db: Session = Depends(get_db)):
    db_tasks = db.query(models.Task).filter(models.Task.title.ilike(f"%{keyword}%")).all()

    tasks_dict = {
        str(task.id): {
            "title": task.title,
            "priority": task.priority,
            "completed": task.completed
        }
        for task in db_tasks
    }

    return {
        "keyword": keyword,
        "count": len(db_tasks),
        "tasks": tasks_dict
    }


# GET — get pending tasks (placed before /{task_id} to avoid conflicts)
@app.get("/tasks/status/pending")
def get_pending_tasks(db: Session = Depends(get_db)):
    db_tasks = db.query(models.Task).filter(models.Task.completed == False).all()

    tasks_dict = {
        str(task.id): {
            "title": task.title,
            "priority": task.priority,
            "completed": task.completed
        }
        for task in db_tasks
    }

    return {
        "status": "pending",
        "count": len(db_tasks),
        "tasks": tasks_dict
    }


# GET — get tasks by priority
@app.get("/tasks/priority/{level}")
def get_tasks_by_priority(level: str, db: Session = Depends(get_db)):
    if level not in ["low", "medium", "high"]:
        raise HTTPException(
            status_code=400,
            detail="Priority must be low, medium, or high"
        )

    db_tasks = db.query(models.Task).filter(models.Task.priority == level).all()

    tasks_dict = {
        str(task.id): {
            "title": task.title,
            "priority": task.priority,
            "completed": task.completed
        }
        for task in db_tasks
    }

    return {
        "priority": level,
        "count": len(db_tasks),
        "tasks": tasks_dict
    }


# GET — get one task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    
    return {
        "id": db_task.id,
        "task": {
            "title": db_task.title,
            "priority": db_task.priority,
            "completed": db_task.completed
        }
    }


# PUT — update a task completely
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db_task.title = task.title
    db_task.priority = task.priority
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)

    return {
        "id": db_task.id,
        "message": "Task updated successfully",
        "task": {
            "title": db_task.title,
            "priority": db_task.priority,
            "completed": db_task.completed
        }
    }


# PATCH — mark a task as completed
@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db_task.completed = True
    db.commit()
    db.refresh(db_task)

    return {
        "id": db_task.id,
        "message": "Task marked as completed",
        "task": {
            "title": db_task.title,
            "priority": db_task.priority,
            "completed": db_task.completed
        }
    }


# DELETE — delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    deleted_task = {
        "title": db_task.title,
        "priority": db_task.priority,
        "completed": db_task.completed
    }

    db.delete(db_task)
    db.commit()

    return {
        "id": task_id,
        "message": "Task deleted successfully",
        "task": deleted_task
    }
