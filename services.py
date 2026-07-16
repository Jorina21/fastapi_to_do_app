from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import HTTPException, status 

from models import TaskModel
from schemas import Task, TaskUpdate, TaskCreate, TaskPatch

def raise_404_HTTPException():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Task not found"
        )







def get_all_tasks(db: Session)-> list[TaskModel]: 
    statement = select(TaskModel)
    return list(db.execute(statement).scalars().all()) #all and list are the same thing
   


def find_task_by_id(db: Session, task_id: int) -> TaskModel | None:
    statement = select(TaskModel).where(TaskModel.id == task_id)
    return db.execute(statement).scalar_one_or_none()




def create_task(db: Session, task: TaskCreate) -> TaskModel:
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
    task = find_task_by_id(db, task_id)

    if task is not None:
        task.title = updated_task.title,
        task.description= updated_task.description,
        task.completed = updated_task.completed,       
        
        db.commit()
        db.refresh(task)


    raise_404_HTTPException()
   
    return task










































def patch_task(db: Session, task_id : int, patched_task: TaskPatch): #why say db of type session? 
    #for editing task can update all or none 

    task = select(TaskModel).Where(TaskModel.id == task_id)
    #task has a task inside it of taskModel (SQL Data --> Python)

    #what type does a select statement return
    #do you need to convert to a python type
    #commit, add, refresh? 


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