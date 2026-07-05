from models import Task

#helper function
def get_default_tasks():
    return [ 
        Task(
            id = 1,
            title = "code for 1 hr",
            description = "part of morning regiment" ,
            completed = False ,

        ),
        Task(
            id = 2,
            title = "wash Dishes",
            description = "Do the dishes from last night ",
            completed = False
            ),

        Task(
            id = 3,
            title = "Gym",
            description = "Go lift or play basketball",
            completed = False  
        )


    ]

tasks = get_default_tasks()

next_task_id = 4