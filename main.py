from typing import Annotated

from fastapi import FastAPI, Query, status, Path, Depends

import models
import services
from database import Base, engine, get_db
from schemas import TaskCreate, Task, TaskUpdate, TaskPatch, TaskDeleteResponse
from sqlalchemy.orm import Session


#Create tables using the models connected to base (TaskModel)
#Create tables from the blueprint if they do no already exist
Base.metadata.create_all(bind=engine)



app = FastAPI(
    title= "Task Tracker API",
    description= "Simple FastAPI CRUD project for learning backend fundamentals",
    version="1.0.0"
)


TaskID = Annotated[
    int, # the type
    Path(
        gt=0, #must be > 0
        description="The Unique positive ID of the task."
    )
]

DbSession = Annotated[Session, Depends(get_db)]#no need to manually get session

@app.get("/",
        tags = ["tags: Home"],
        summary = "Summary: Home Route",
        description="Description: Returns a simple message indicating API running",
        include_in_schema = True)
def home_page():
    return {
        "message": "welcome to the home page"
    }

@app.get("/tasks",
        response_model = list[Task],
        status_code = status.HTTP_200_OK,
        tags=["Tasks"],
        summary="Get all Tasks", 
        description="Return all tasks. You can optionally filter by completion status or search by title/description."
)
def get_tasks(
    db: DbSession, #first argument
    completed : Annotated[
        bool | None,
        Query(
            description = "Filter task by completion status. Use true for completed tasks or false for incomplete tasks."
        )
    ] = None,

    search : Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=100,
            description="Search tasks by title or description."
    )] = None
    ):
    results = services.get_all_tasks(db)

    if completed is not None:
       results = [task for task in results if task.completed == completed ]

    if search is not None:
       results = [task for task in results if task.title.lower() in search.lower() or task.title.upper() in search.upper()]

    return results



#create
@app.post("/tasks",
        response_model = Task,
        status_code= status.HTTP_201_CREATED,
        tags=["Tasks"],
        summary="Create a Task",
        description="Create a new task. The server automatically assigns the task ID and sets completed to false.") #does this run first or after? status code before or after succession? Why does post have status code? what do each route have guranteed or good practice exp get, post, update ,delete? 
def create_task(task : TaskCreate, db : DbSession):
    return services.create_task(db, task) #why is it reversed? 

#read
@app.get("/tasks/{task_id}",
        response_model = Task,
        tags = ["Tasks"],
        summary="Get one task",
        description="Return one task by its unique ID."
)
def get_tasks(task_id : TaskID
) -> Task:
    task = services.get_task_by_id(task_id)
    if task is None:
        return services.raise_404_HTTPException()
    
    return task 


#update tasks
@app.put("/tasks/{task_id}",
        response_model = Task,
        status_code = status.HTTP_200_OK,
        tags=["Tasks"],
        summary="Fully update a task",
        description="Replace all editable fields of an existing task: title, description, and completed."
        )
def update_task(
                task_id: int ,
                updated_task : TaskUpdate,
                db: Session = Depends(get_db)):
    
    return services.update_task( db,task_id, updated_task)



#delete 
@app.delete("/tasks/{task_id}",
            status_code = status.HTTP_200_OK,
            response_model= TaskDeleteResponse,
            tags=["Tasks"],
            summary="Delete a task",
            description="Delete one task by ID. Returns no response body when successful."
            )
def delete_task(task_id : TaskID):
    return services.delete_task(task_id)
    # return {"message": "Task deleted successfully"}


@app.patch("/tasks/{task_id}",
            response_model = Task,
            status_code = status.HTTP_200_OK,
            tags=["Tasks"],
            summary="Partially update a task",
            description="Update only the fields provided in the request body."
)
def patch_task(task_id : int, patched_task : TaskPatch):
    return services.patch_task(task_id, patched_task)


#complete_task
@app.patch("/tasks/{task_id}/completed",
            response_model = Task,
            status_code = status.HTTP_200_OK,
            tags=["Tasks"],
            summary="Mark a task complete",
            description="Set a task's completed field to true."
           )
def mark_complete(task_id : TaskID) -> Task:
    return services.mark_complete(task_id)









