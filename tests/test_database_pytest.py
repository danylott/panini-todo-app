import os
import pytest
import pathlib
import shutil
import unittest

from panini.test_client import TestClient

testing_directory_path = pathlib.Path(__file__).parent.absolute()


def get_testing_logs_directory_path(
    folder: str = "logs", remove_if_exist: bool = False
):
    testing_logs_directory_path = os.path.join(testing_directory_path, folder)
    if remove_if_exist:
        if os.path.exists(testing_logs_directory_path):
            shutil.rmtree(testing_logs_directory_path)

    return testing_logs_directory_path


@pytest.fixture(scope="session")
def test_client():
    from database.main import app
    app.logger_files_path = get_testing_logs_directory_path()
    return TestClient(app.start).start()


def test_create_task(test_client):
    response = test_client.request("create-task", {"title": "test"})
    assert response["data"]["title"] == "test"
    assert "id" in response["data"]


def test_toggle_task(test_client):
    response = test_client.request("create-task", {"title": "test"})
    assert response["data"]["is_completed"] is False
    response = test_client.request("toggle-task", {"id": response["data"]["id"]})
    assert response["data"]["is_completed"] is True


def test_get_tasks(test_client):
    test_client.request("create-task", {"title": "test1"})
    test_client.request("create-task", {"title": "test2"})
    response = test_client.request("get-tasks", {})
    titles = [task["title"] for task in response["data"]]
    assert "test1" in titles
    assert "test2" in titles
