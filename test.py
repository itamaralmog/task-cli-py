import unittest
from unittest.mock import patch, mock_open, call
import json
import os

# Import the functions to test
from task_cli import add, update, delete_task, mark_in, show_list, initialize_id


class TestTaskCLI(unittest.TestCase):
    def setUp(self):
        # Mock file content as JSON string
        self.mock_data = {
            "tasks": [
                {"description": "Buy groceries", "ID": 1, "mark": "todo"},
                {"description": "Buy basketball", "ID": 2, "mark": "todo"},
            ]
        }
        self.mock_file_content = json.dumps(self.mock_data)

    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    @patch("os.path.exists", return_value=False)
    def test_initialize_id_no_file(self, mock_exists, mock_open):
        """Test initialize_id when file does not exist."""
        initialize_id()
        self.assertTrue(mock_open.called)
    
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"tasks": []}))
    @patch("os.path.exists", return_value=True)
    def test_initialize_id_empty_file(self, mock_exists, mock_open):
        """Test initialize_id with an empty file."""
        initialize_id()
        self.assertTrue(mock_open.called)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(self.mock_data))
    @patch("os.path.exists", return_value=True)
    def test_initialize_id_existing_file(self, mock_exists, mock_open):
        """Test initialize_id when file exists."""
        initialize_id()
        self.assertTrue(mock_open.called)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=False)
    def test_add_no_file(self, mock_exists, mock_open):
        """Test add functionality when file does not exist."""
        add("New Task", "todo")
        mock_open().write.assert_called_once_with(json.dumps({
            "tasks": [{"description": "New Task", "ID": 1, "mark": "todo"}]
        }, indent=4))

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(self.mock_data))
    @patch("os.path.exists", return_value=True)
    def test_add_existing_file(self, mock_exists, mock_open):
        """Test add functionality when file exists."""
        add("New Task", "todo")
        calls = mock_open().write.call_args_list
        updated_data = json.loads(calls[-1][0][0])  # Get the last write call data
        self.assertEqual(len(updated_data["tasks"]), 3)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(self.mock_data))
    @patch("os.path.exists", return_value=True)
    def test_update_existing_task(self, mock_exists, mock_open):
        """Test updating an existing task."""
        update(1, "Updated Task")
        calls = mock_open().write.call_args_list
        updated_data = json.loads(calls[-1][0][0])  # Get the last write call data
        self.assertEqual(updated_data["tasks"][0]["description"], "Updated Task")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(self.mock_data))
    @patch("os.path.exists", return_value=True)
    def test_update_nonexistent_task(self, mock_exists, mock_open):
        """Test updating a nonexistent task."""
        update(99, "Updated Task")
        mock_open().write.assert_called_once_with(self.mock_file_content)  # No change

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(self.mock_data))
    @patch("os.path.exists", return_value=True)
    def test_delete_existing_task(self, mock_exists, mock_open):
        """Test deleting an existing task."""
        delete_task(1)
        calls = mock_open().write.call_args_list
        updated_data = json.loads(calls[-1][0][0])  # Get the last write call data
        self.assertEqual(len(updated_data["tasks"]), 1)

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(self.mock_data))
    @patch("os.path.exists", return_value=True)
    def test_delete_nonexistent_task(self, mock_exists, mock_open):
        """Test deleting a nonexistent task."""
        delete_task(99)
        mock_open().write.assert_called_once_with(self.mock_file_content)  # No change

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(self.mock_data))
    @patch("os.path.exists", return_value=True)
    def test_mark_task(self, mock_exists, mock_open):
        """Test marking a task as in-progress or done."""
        mark_in(1, "in-progress")
        calls = mock_open().write.call_args_list
        updated_data = json.loads(calls[-1][0][0])  # Get the last write call data
        self.assertEqual(updated_data["tasks"][0]["mark"], "in-progress")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(self.mock_data))
    @patch("os.path.exists", return_value=True)
    @patch("builtins.print")
    def test_show_list_all(self, mock_print, mock_exists, mock_open):
        """Test showing all tasks."""
        show_list("all")
        mock_print.assert_any_call("1. {'description': 'Buy groceries', 'ID': 1, 'mark': 'todo'}")
        mock_print.assert_any_call("2. {'description': 'Buy basketball', 'ID': 2, 'mark': 'todo'}")

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(self.mock_data))
    @patch("os.path.exists", return_value=True)
    @patch("builtins.print")
    def test_show_list_filtered(self, mock_print, mock_exists, mock_open):
        """Test showing tasks filtered by mark."""
        show_list("todo")
        mock_print.assert_any_call("1. {'description': 'Buy groceries', 'ID': 1, 'mark': 'todo'}")
        mock_print.assert_any_call("2. {'description': 'Buy basketball', 'ID': 2, 'mark': 'todo'}")

class CustomTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super().run(test)
        total = result.testsRun
        errors = len(result.errors)
        failures = len(result.failures)
        passed = total - (errors + failures)

        print("\n======= Test Results =======")
        print(f"Total Tests: {total}")
        print(f"Passed Tests: {passed}")
        print(f"Failed Tests: {failures}")
        print(f"Errors: {errors}")
        
        if failures or errors:
            print("\nDetailed Report:")
            for test, err in result.failures + result.errors:
                print(f"\nFailed Test: {test}")
                print(err)

        return result

if __name__ == "__main__":
    unittest.main(testRunner=CustomTestRunner())
    
