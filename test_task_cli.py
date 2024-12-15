import os
import json
import pytest
from task_cli import add, update, delete_task, mark_in, show_list, initialize_id, file_name, init

# Fixture for setup and teardown
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """
    Setup: Create a fresh JSON file before each test.
    Teardown: Delete the JSON file after each test.
    """
    if os.path.exists(file_name):
        os.remove(file_name)
    yield
    if os.path.exists(file_name):
        os.remove(file_name)

def load_tasks():
    """Helper function to load tasks from the JSON file."""
    with open(file_name, "r") as file:
        return json.load(file)["tasks"]

# Test cases
def test_initialize_id():
    assert initialize_id() == 1

def test_add_task():
    data = {"tasks": []}
    with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    initialize_id()
    add("First Task", "todo")
    tasks = load_tasks()
    assert len(tasks) == 1, "A single task should be added"
    assert tasks[0]["description"] == "First Task", "Task description should match"
    assert tasks[0]["mark"] == "todo", "Task mark should be 'todo'"

def test_update_task():
    data = {"tasks": []}
    with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    initialize_id()
    add("Task to Update", "todo")
    update(2, "Updated Task")
    tasks = load_tasks()
    assert tasks[0]["description"] == "Updated Task", "Task description should be updated"

def test_delete_task():
    data = {"tasks": []}
    with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    initialize_id()
    add("Task to Delete", "todo")
    delete_task(3)
    tasks = load_tasks()
    assert len(tasks) == 0, "Task should be deleted successfully"

def test_mark_in_progress():
    data = {"tasks": []}
    with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    initialize_id()
    add("Task to Mark", "todo")
    mark_in(4, "in-progress")
    tasks = load_tasks()
    assert tasks[0]["mark"] == "in-progress", "Task mark should be updated to 'in-progress'"

def test_mark_done():
    data = {"tasks": []}
    with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    initialize_id()
    add("Task to Complete", "todo")
    mark_in(5, "done")
    tasks = load_tasks()
    assert tasks[0]["mark"] == "done", "Task mark should be updated to 'done'"

def test_show_list_all(capfd):
    data = {"tasks": []}
    with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    initialize_id()
    add("Task 1", "todo")
    add("Task 2", "in-progress")
    show_list("all")
    captured = capfd.readouterr()
    assert "Task 1" in captured.out, "Task 1 should be displayed"
    assert "Task 2" in captured.out, "Task 2 should be displayed"

def test_show_list_filtered(capfd):
    data = {"tasks": []}
    with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    initialize_id()
    add("Task 1", "todo")
    add("Task 2", "in-progress")
    show_list("todo")
    captured = capfd.readouterr()
    assert "Task 1" in captured.out, "Filtered list should include Task 1"
    assert "Task 2" not in captured.out, "Filtered list should exclude Task 2"

def test_nonexistent_task_update():
    data = {"tasks": []}
    with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    initialize_id()
    update(99, "Nonexistent Update")
    tasks = load_tasks()
    assert len(tasks) == 0, "No tasks should be modified for a nonexistent task"

def test_nonexistent_task_delete():
    data = {"tasks": []}
    with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    initialize_id()
    delete_task(99)
    tasks = load_tasks()
    assert len(tasks) == 0, "No tasks should be deleted for a nonexistent task"

def test_nonexistent_task_mark():
    data = {"tasks": []}
    with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    initialize_id()
    mark_in(99, "done")
    tasks = load_tasks()
    assert len(tasks) == 0, "No tasks should be marked for a nonexistent task"

def test_add_multiple_tasks():
    data = {"tasks": []}
    with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    initialize_id()
    add("Task 1", "todo")
    add("Task 2", "todo")
    tasks = load_tasks()
    assert len(tasks) == 2, "Two tasks should be added"
    assert tasks[0]["description"] == "Task 1", "First task description should match"
    assert tasks[1]["description"] == "Task 2", "Second task description should match"

def test_update_marked_task():
    initialize_id()
    add("Task to Mark and Update", "todo")
    mark_in(12, "in-progress")
    update(12, "Updated and Marked Task")
    tasks = load_tasks()
    print(tasks)
    assert tasks[0]["description"] == "Updated and Marked Task", "Description should be updated"
    assert tasks[0]["mark"] == "in-progress", "Mark should remain 'in-progress'"
# No tasks found in JSON file. Using default ID = 1.
# New task added: {'ID': 12}
# Task ID 1 not found.
# Task ID 1 not found.
# [{'description': 'Task to Mark and Update', 'ID': 12, 'mark': 'todo'}]

# Main execution
if __name__ == "__main__":
    pytest.main(["-v", "--tb=short"])
