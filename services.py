from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status 

from schemas import Task, TaskUpdate, TaskCreate, TaskPatch
from models import TaskModel

def raise_404_HTTPException():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Task not found"
        )

# def next_task_id():
#     current_task_id = database.next_task_id
#     database.next_task_id += 1 
#     return current_task_id

def get_all_tasks(db: Session): 
    statement = select(TaskModel)
    return db.execute(statement).scalars().all
   


def find_task_by_id(db: Session, task_id: int):
    statement = select(TaskModel).where(TaskModel.id == task_id)
    return db.execute(statement).scalar_one_or_none()

def create_task(db: Session, task: TaskCreate) -> Task:
    db_task = TaskModel(
        title = task.title,
        description = task.description,
        completed = False
    )
    db.add(db_task) #stage to be commit 
    db.commit() #permanent write to the databse 
    db.refresh(db_task) #force db to qeury that new addition giving it fully to be returned

    return db_task

    

def update_task(db: Session, task_id: int, updated_task: TaskUpdate):
    # find the id 
    task = find_task_by_id(task_id)

    if task is not None:
        new_task = Task(
            id = task.id, #not good you can change id
            title = updated_task.title,
            description= updated_task.description,
            completed = updated_task.completed,       
        )
        # stage task to be sent to db 
        db.add(new_task)
        db.commit()
        db.refresh(new_task)


    raise_404_HTTPException()
   

def patch_task(id : int, patched_task: TaskPatch):
    pass


def complete_task():
    pass


def delete_task(task_id : int):
    pass


def get_task_index_by_id(task_id):
    for index , task in enumerate(database.tasks):
        if task_id == task.id:
            return index
    
    return None
        






def get_tasks(task_id : int):
    if task_id == None:
            return get_all_tasks() 
    
    if task_id > len(database.tasks):
        raise HTTPException(status_code = 404, detail = "no task")
            
    return get_task_by_id(task_id)



def mark_complete(task_id: int)-> Task:
    task = get_task_by_id(task_id)

    if task is None:
        raise_404_HTTPException()
        
    task.completed = True

    return task