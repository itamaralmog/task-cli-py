const fs = require('fs');
const { initializeId, addTask, updateTask, deleteTask, markTask, listTasks ,initializeTasksFile } = require('./taskManager');

const fileName = 'tasks.json';

beforeEach(() => {
    if (fs.existsSync(fileName)) {
        fs.unlinkSync(fileName);
    }
});

afterEach(() => {
    if (fs.existsSync(fileName)) {
        fs.unlinkSync(fileName);
    }
});

test('Initialize ID starts from 1 for a fresh file', () => {
    initializeTasksFile();
    initializeId();
    const data = JSON.parse(fs.readFileSync(fileName, 'utf-8'));
    expect(data.tasks.length).toBe(0);
});

test('Add task correctly', () => {
    initializeId();
    addTask('First task');
    const data = JSON.parse(fs.readFileSync(fileName, 'utf-8'));
    expect(data.tasks.length).toBe(1);
    expect(data.tasks[0].description).toBe('First task');
});

test('Update task correctly', () => {
    initializeId();
    addTask('Task to update');
    updateTask(2, 'Updated task');
    const data = JSON.parse(fs.readFileSync(fileName, 'utf-8'));
    expect(data.tasks[0].description).toBe('Updated task');
});

test('Delete task correctly', () => {
    initializeId();
    addTask('Task to delete');
    deleteTask(3);
    const data = JSON.parse(fs.readFileSync(fileName, 'utf-8'));
    expect(data.tasks.length).toBe(0);
});

test('Mark task correctly', () => {
    initializeId();
    addTask('Task to mark');
    markTask(4, 'done');
    const data = JSON.parse(fs.readFileSync(fileName, 'utf-8'));
    expect(data.tasks[0].mark).toBe('done');
});
// jest taskManager.test.js