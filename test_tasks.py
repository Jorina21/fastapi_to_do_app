from fastapi.testclient import TestClient

from main import app 

import pytest
import database


client = TestClient(app)

@pytest.fixture(autouse = True)
def reset_database():
    database.tasks = database.get_default_tasks()
    database.next_task_id = 4



def test_home_route():

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "welcome to the home page"}


def test_get_all_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_task():
    response = client.post(
        "/tasks",
        json = {
            "title" : "Test task",
            "description" : "Created during automated testing"
        }
    )

    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "Test task"
    assert data["description"] == "Created during automated testing"
    assert data["completed"] is False
    assert "id" in data


def test_create_then_get_task():
    create_response = client.post(
        url = "/tasks",
        json = {
            "title": "Create then get",
            "description" : "Testing full flow" 
        }

    )

    created_task = create_response.json() #convert json to python dictionary / array 
    task_id = created_task["id"] #acces dict 
    
    get_response = client.get(f"/tasks/{task_id}")
    fetched_task = get_response.json()

    assert get_response.status_code == 200
    assert fetched_task["id"] == task_id
    assert fetched_task["title"] == "Create then get"


def test_get_missing_task_returns_404():
    response = client.get("/tasks/9999")

    assert response.status_code == 404
    assert response.json() == {"detail":"Task not found"}


def test_create_task_with_blank_title_fails():
    response = client.post(
        url = "/tasks",
        json = {
            "title":"  ",
            "description": " this hould fail"
            }
        )
    

    assert response.status_code == 422

def test_filter_completed_task():
    response = client.get("/tasks?completed=true")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 0
    assert all(task["completed"] is True for task in data)


########################pasted##############################################


def test_filter_incomplete_tasks():
    response = client.get("/tasks?completed=false")
    data = response.json()

    
    assert response.status_code == 200
    assert len(data) == 3
    assert all(task["completed"] is False for task in data)


def test_search_tasks():
    response = client.get("/tasks?search=GYM")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["description"] == "Go lift or play basketball"


def test_update_task():
    response = client.put(
        "/tasks/1",
        json={
            "title": "Updated title",
            "description": "Updated description",
            "completed": True
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == 1
    assert data["title"] == "Updated title"
    assert data["description"] == "Updated description"
    assert data["completed"] is True


def test_patch_task_title():
    response = client.patch(
        "/tasks/1",
        json={
            "title": "Patched title"
        }
    )

    data = response.json()

    assert response.status_code == 200
    assert data["id"] == 1
    assert data["title"] == "Patched title"
    assert data["description"] == "part of morning regiment"
    assert data["completed"] is False


def test_complete_task():
    response = client.patch("/tasks/1/completed")
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == 1
    assert data["completed"] is True


def test_delete_task():
    delete_response = client.delete("/tasks/1")
    data = delete_response.json()

    assert delete_response.status_code == 200
    assert data["message"] == "Task deleted successfully"
    assert data["deleted_task"]["id"] ==  1

    get_response = client.get("/tasks/1")

    assert get_response.status_code == 404


def test_search_query_cannot_be_empty():
    response = client.get("/tasks?search=")

    assert response.status_code == 422


def test_search_query_cannot_be_too_long():
    
    long_search = "a" * 101 #string 100 times


    response = client.get(f"/tasks?search={long_search}")

    assert response.status_code == 422 

def test_task_id_must_be_greater_than_zero():
    
    response = client.get("/tasks/0")

    assert response.status_code == 422

def test_task_id_cannot_be_negative():
    response = client.get("/tasks/-1")

    assert response.status_code == 422

def test_delete_task_id_must_be_greater_than_zero():
    response = client.delete("/tasks/0")

    assert response.status_code == 422