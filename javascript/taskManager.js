// Import required modules
const fs = require('fs');
const readline = require('readline');

const fileName = 'tasks.json';
let id = 1;

// Initialize ID based on existing tasks
function initializeId() {
    if (fs.existsSync(fileName)) {
        const data = JSON.parse(fs.readFileSync(fileName, 'utf8'));
        const tasks = data.tasks || [];
        if (tasks.length > 0) {
            id = Math.max(...tasks.map(task => task.ID)) + 1;
            console.log(`Initialized ID to ${id} based on existing tasks.`);
        } else {
            console.log('No tasks found in JSON file. Using default ID = 1.');
        }
    } else {
        console.log('JSON file not found. Starting fresh with ID = 1.');
    }
}

// Add a new task
function addTask(description, mark = 'todo') {
    const newTask = { description, ID: id++, mark };

    let data = { tasks: [] };
    if (fs.existsSync(fileName)) {
        data = JSON.parse(fs.readFileSync(fileName, 'utf8'));
    }
    data.tasks.push(newTask);
    fs.writeFileSync(fileName, JSON.stringify(data, null, 4));
    console.log('New task added:', newTask);
}

// Update a task
function updateTask(taskId, newDescription) {
    if (fs.existsSync(fileName)) {
        const data = JSON.parse(fs.readFileSync(fileName, 'utf8'));
        const task = data.tasks.find(task => task.ID === taskId);

        if (task) {
            task.description = newDescription;
            fs.writeFileSync(fileName, JSON.stringify(data, null, 4));
            console.log(`Task ID ${taskId} updated successfully.`);
        } else {
            console.log(`Task ID ${taskId} not found.`);
        }
    } else {
        console.log('Error: Task file not found. Please add a task first.');
    }
}

// Delete a task
function deleteTask(taskId) {
    if (fs.existsSync(fileName)) {
        const data = JSON.parse(fs.readFileSync(fileName, 'utf8'));
        const originalLength = data.tasks.length;
        data.tasks = data.tasks.filter(task => task.ID !== taskId);

        if (data.tasks.length < originalLength) {
            fs.writeFileSync(fileName, JSON.stringify(data, null, 4));
            console.log(`Task ID ${taskId} deleted successfully.`);
        } else {
            console.log(`Task ID ${taskId} not found.`);
        }
    } else {
        console.log('Error: Task file not found. Please create a task first.');
    }
}

// Mark a task
function markTask(taskId, mark) {
    if (fs.existsSync(fileName)) {
        const data = JSON.parse(fs.readFileSync(fileName, 'utf8'));
        const task = data.tasks.find(task => task.ID === taskId);

        if (task) {
            task.mark = mark;
            fs.writeFileSync(fileName, JSON.stringify(data, null, 4));
            console.log(`Task ID ${taskId} marked as '${mark}' successfully.`);
        } else {
            console.log(`Task ID ${taskId} not found.`);
        }
    } else {
        console.log('Error: Task file not found. Please add a task first.');
    }
}

// Show tasks
function showTasks(filter = 'all') {
    if (fs.existsSync(fileName)) {
        const data = JSON.parse(fs.readFileSync(fileName, 'utf8'));
        const tasks = data.tasks;

        let filteredTasks = tasks;
        if (filter !== 'all') {
            filteredTasks = tasks.filter(task => task.mark === filter);
        }

        filteredTasks.forEach((task, index) => {
            console.log(`${index + 1}.`, task);
        });
    } else {
        console.log('Error: Task file not found. Please add a task first.');
    }
}


function initializeTasksFile() {
    const data = { tasks: [] }; // Define the structure of the tasks file
    fs.writeFileSync(fileName, JSON.stringify(data, null, 4)); // Write the data to the file with indentation
    console.log('Initialized tasks.json with an empty tasks array.');
}

// CLI for user interaction
function taskCLI() {
    initializeId();

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    rl.setPrompt('task-cli> ');
    rl.prompt();

    rl.on('line', input => {
        const args = input.trim().split(/\s+/);
        const command = args[0];

        switch (command) {
            case 'add':
                addTask(args.slice(1).join(' '));
                break;
            case 'update':
                updateTask(parseInt(args[1]), args.slice(2).join(' '));
                break;
            case 'delete':
                deleteTask(parseInt(args[1]));
                break;
            case 'mark-in-progress':
                markTask(parseInt(args[1]), 'in-progress');
                break;
            case 'mark-done':
                markTask(parseInt(args[1]), 'done');
                break;
            case 'list':
                showTasks(args[1] || 'all');
                break;
            case 'exit':
                console.log('Exiting task CLI.');
                rl.close();
                return;
            default:
                console.log('Unknown command. Available commands: add, update, delete, mark-in-progress, mark-done, list, exit.');
        }

        rl.prompt();
    });
}

// Run the CLI if this file is executed directly
if (require.main === module) {
    taskCLI();
}

module.exports = { initializeId, addTask, updateTask, deleteTask, markTask, showTasks, initializeTasksFile};
