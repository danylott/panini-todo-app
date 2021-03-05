import uuid

from panini import app as panini_app
from panini.validator import Validator, Field

TASKS = {}

app = panini_app.App(
    service_name="database",
    host="127.0.0.1",
    port=4222,
)


class Task:
    def __init__(self, title: str):
        self.id = str(uuid.uuid4())
        self.title = title
        self.is_completed = False


class CreateTaskValidator(Validator):
    title = Field(type=str)


class ToggleTaskValidator(Validator):
    id = Field(type=str)


@app.listen("create-task", validator=CreateTaskValidator)
async def create_task(subject: str, message: dict):
    assert subject == "create-task"
    task = Task(message['title'])
    TASKS[task.id] = task
    return {"message": "Task was successfully created", "data": task.__dict__}


@app.listen("toggle-task", validator=ToggleTaskValidator)
async def toggle_task(subject: str, message: dict):
    assert subject == "toggle-task"
    task = TASKS[message['id']]
    task.is_completed = not task.is_completed
    return {"message": "Task was successfully toggled", "data": task.__dict__}


@app.listen("get-tasks")
async def get_tasks(subject: str, message: dict):
    assert subject == "get-tasks"
    return {"message": "Tasks retrieved successfully", "data": [task.__dict__ for task in TASKS.values()]}


if __name__ == '__main__':
    app.start()
