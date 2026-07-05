from pydantic import BaseModel, Field, field_validator 

class TaskCreate(BaseModel):
    title: str = Field(..., min_length = 1, max_length = 100) #how long or short input field is
    description: str | None = Field(default = None, max_length = 500)

    # completed : bool = Field(default = False)
    #remove so each service create the task with completed = false

    @field_validator("title", mode = "after")#run before or after type validation 
    @classmethod
    def title_not_blank(cls, value:str) -> str:
        if value.strip() == "":
            raise ValueError("Title cannot be blank")
        
        return value.strip()

class TaskUpdate(BaseModel):
    title : str = Field(min_length = 1 , max_length = 50)
    description : str | None = Field(default = None, max_length = 500)
    completed : bool 

    @field_validator('title', mode = "after")
    @classmethod
    def check_if_empty(cls, data : str):
        if data.strip() == "":
            raise ValueError("data cannot be empty")
        
        return data.strip()

     

class TaskPatch(BaseModel):
    title : str | None  = Field(default = None, min_length = 1 , max_length = 50)
    description : str | None = Field(default = None , min_length = 1 , max_length = 500)
    completed : bool | None = Field(default = None)

    @field_validator("title", "description", mode = "after")
    @classmethod
    def fields_empty(cls, data):
        if data.strip() == "":
            raise ValueError("fields cannot be empty")
        
        return data.strip()



class Task(BaseModel):
    id : int 
    title : str 
    description : str 
    completed : bool 

class TaskDeleteResponse(BaseModel):
    message: str
    deleted_task: Task

    