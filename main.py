# # Adding a new task
# task-cli add "Buy groceries"
# # Output: Task added successfully (ID: 1)

# # Updating and deleting tasks
# task-cli update 1 "Buy groceries and cook dinner"
# task-cli delete 1

# # Marking a task as in progress or done
# task-cli mark-in-progress 1
# task-cli mark-done 1

# # Listing all tasks
# task-cli list

# # Listing tasks by status
# task-cli list done
# task-cli list todo
# task-cli list in-progress
#json: task , mark, id 

import os
import json
import shlex

file_name = "tasks.json"
id = 1

def add(task,mark):
    global id
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
        
        # Add a new task
        data["tasks"].append({"description": task, "ID": id, "mark": mark})
        id+=1
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        print("New append created:", data)
    else:
        data = {
            "tasks": [{"description": task, "ID": id, "mark":mark}]
        }
        id += 1
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        print("New JSON file created:", data)
    
    
def tasks():
    while True:
        user_input = input("task cli ")  # Takes input as a string
        parsed_input = shlex.split(user_input)
        
        if parsed_input[0] == "add":
            mark = "todo"
            name = parsed_input[1]
            add(name,mark)
        if parsed_input[0] == "update":
            id_task = parsed_input[1]
            update_description = parsed_input[2]
            
        
        




tasks()