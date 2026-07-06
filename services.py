from fastapi import HTTPException, status 
from schemas import Task, TaskUpdate, TaskCreate, TaskPatch
import database

def raise_404_HTTPException():
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Task not found"
        )

def next_task_id():
    current_task_id = database.next_task_id
    database.next_task_id += 1 
    return current_task_id

def get_task_by_id(task_id: int):
    for task in database.tasks:
        if task.id == task_id:
            return task
        
def get_task_index_by_id(task_id):
    for index , task in enumerate(database.tasks):
        if task_id == task.id:
            return index
    
    return None
        

def get_all_tasks():
     return database.tasks




def get_tasks(task_id : int):
    if task_id == None:
            return get_all_tasks() 
    
    if task_id > len(database.tasks):
        raise HTTPException(status_code = 404, detail = "no task")
            
    return get_task_by_id(task_id)

def create_task(task : TaskCreate) -> Task:
    new_task = Task(id = next_task_id(),
                    title = task.title,
                    description = task.description,
                    completed = False
                    )

    database.tasks.append(new_task)

    return new_task

def update_task(task_id : int , updated_task : TaskUpdate):
    index = get_task_index_by_id(task_id)
    if index is not None:
        task = Task(id = task_id,
                    title = updated_task.title,
                    description = updated_task.description,
                    completed = updated_task.completed
                    )
                
        database.tasks[index] = task
                
        return task 

        
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "task id not found")    
              
def delete_task(task_id : int):
    task = get_task_index_by_id(task_id)

    if task is None:
        raise_404_HTTPException()
    
    
    deleted_task = database.tasks.pop(task)
    return {
            "message": "Task deleted successfully",
            "deleted_task": deleted_task 
    }

    
     


def patch_task(id : int, patched_task: TaskPatch):
    
    task_index = get_task_index_by_id(id)

    if task_index is not None:
        task = get_task_by_id(id)

        patched_task = Task(id = task.id,
                            title = patched_task.title if patched_task.title is not None else task.title,
                            description = patched_task.description if patched_task.description is not None else task.description,
                            completed = patched_task.completed if patched_task.completed is not None else task.completed,
                            )

        database.tasks[task_index] = patched_task
        
        return patched_task

    raise_404_HTTPException()



def mark_complete(task_id: int)-> Task:
    task = get_task_by_id(task_id)

    if task is None:
        raise_404_HTTPException()
        
    task.completed = True

    return task