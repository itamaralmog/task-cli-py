import os
import json
import shlex

file_name = "tasks.json"
id = 1

def add(task, mark):
    global id
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        
        # Add a new task
        data["tasks"].append({"description": task, "ID": id, "mark": mark})
        id += 1
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        print("New task added:", {"description": task, "ID": id - 1, "mark": mark})
    else:
        data = {
            "tasks": [{"description": task, "ID": id, "mark": mark}]
        }
        id += 1
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        print("New JSON file created with the first task:", {"description": task, "ID": id - 1, "mark": mark})


def update(task_id, new_description):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        
        # Search for the task by ID and update it
        for task in data["tasks"]:
            if task["ID"] == task_id:  # Task ID matches
                task["description"] = new_description
                print(f"Task ID {task_id} updated successfully.")
                break
        else:
            print(f"Task ID {task_id} not found.")

        # Save the updated data back to the file
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        print("Error: Task file not found. Please add a task first.")

def delete_task(task_id):
    if os.path.exists(file_name):
        # Load the JSON file
        with open(file_name, 'r') as file:
            data = json.load(file)
        
        # Filter out the task with the specified ID
        original_length = len(data["tasks"])
        data["tasks"] = [task for task in data["tasks"] if task["ID"] != task_id]
        
        if len(data["tasks"]) < original_length:
            # Save the updated JSON data
            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Task ID {task_id} deleted successfully.")
        else:
            print(f"Task ID {task_id} not found.")
    else:
        print("Error: Task file not found. Please create a task first.")
    
def mark_in(task_id,mark):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        
        # Search for the task by ID and update it
        for task in data["tasks"]:
            if task["ID"] == task_id:  # Task ID matches
                task["mark"] = mark
                print(f"Task ID {task_id} marked in-progress successfully.")
                break
        else:
            print(f"Task ID {task_id} not found.")

        # Save the updated data back to the file
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    else:
        print("Error: Task file not found. Please add a task first.")

def show_list(mark):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        num = 1
        if mark == "all":
            for task in data["tasks"]:
                print(f"{num}. {task}")
                num+=1
        else:
            for task in data["tasks"]:
                if task["mark"] == mark:
                    print(f"{num}. {task}")
                    num+=1
            
    else:
        print("Error: Task file not found. Please add a task first.")
    

def tasks():
    while True:
        user_input = input("task-cli> ")  # Takes input as a string
        parsed_input = shlex.split(user_input)
        print(parsed_input)
        
        if parsed_input[0] == "add":
            mark = "todo"
            name = " ".join(parsed_input[1:])  # Handle multi-word task names
            add(name, mark)
        
        elif parsed_input[0] == "update":
            task_id = int(parsed_input[1])
            update_description = " ".join(parsed_input[2:])  # Handle multi-word descriptions
            update(task_id, update_description)
        
        elif parsed_input[0] =="delete":
            task_id = int(parsed_input[1])
            delete_task(task_id)
        
        elif parsed_input[0] =="mark-in-progress":
            task_id = int(parsed_input[1])
            mark_in(task_id,"in-progress")
            
        elif parsed_input[0] =="mark-done":
            task_id = int(parsed_input[1])
            mark_in(task_id,"done")
        
        elif parsed_input[0] =="list":
            if len(parsed_input) == 1:
                show_list("all")
            else:
                show_list(parsed_input[1])
        
        elif parsed_input[0] == "exit":
            print("Exiting task CLI.")
            break
        
        else:
            print("Unknown command. Available commands: add, update, exit.")

tasks()
