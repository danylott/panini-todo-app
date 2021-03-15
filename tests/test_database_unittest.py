import os
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


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from database.main import app
        app.logger_files_path = get_testing_logs_directory_path()
        cls.test_client = TestClient(app.start).start()

    def test_create_task(self):
        response = self.test_client.request("create-task", {"title": "test"})
        self.assertEqual(response["data"]["title"], "test")
        self.assertIn("id", response["data"])

    def test_toggle_task(self):
        response = self.test_client.request("create-task", {"title": "test"})
        self.assertEqual(response["data"]["is_completed"], False)
        response = self.test_client.request("toggle-task", {"id": response["data"]["id"]})
        self.assertEqual(response["data"]["is_completed"], True)

    def test_get_tasks(self):
        self.test_client.request("create-task", {"title": "test1"})
        self.test_client.request("create-task", {"title": "test2"})
        response = self.test_client.request("get-tasks", {})
        titles = [task["title"] for task in response["data"]]
        self.assertIn("test1", titles)
        self.assertIn("test2", titles)
