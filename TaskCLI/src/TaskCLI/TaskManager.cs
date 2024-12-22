using System;
using System.Collections.Generic;
using System.IO;
using Newtonsoft.Json;

namespace TaskCLI
{
    public class Task
    {
        public int ID { get; set; }
        public string Description { get; set; }
        public string Mark { get; set; }
    }

    public class TaskManager
    {
        private static readonly string FileName = "tasks.json";
        private static int _id = 1;

        public TaskManager()
        {
            InitializeID();
        }

        private void InitializeID()
        {
            if (File.Exists(FileName))
            {
                try
                {
                    var data = JsonConvert.DeserializeObject<Dictionary<string, List<Task>>>(File.ReadAllText(FileName));
                    if (data != null && data.ContainsKey("tasks") && data["tasks"].Count > 0)
                    {
                        _id = data["tasks"].Max(task => task.ID) + 1;
                        Console.WriteLine($"Initialized ID to {_id}.");
                    }
                }
                catch
                {
                    Console.WriteLine("Invalid JSON file. Starting fresh.");
                }
            }
            else
            {
                Console.WriteLine("No tasks file found. Starting fresh.");
            }
        }

        private List<Task> LoadTasks()
        {
            if (!File.Exists(FileName)) return new List<Task>();
            var data = JsonConvert.DeserializeObject<Dictionary<string, List<Task>>>(File.ReadAllText(FileName));
            return data != null && data.ContainsKey("tasks") ? data["tasks"] : new List<Task>();
        }

        private void SaveTasks(List<Task> tasks)
        {
            var data = new Dictionary<string, List<Task>> { { "tasks", tasks } };
            File.WriteAllText(FileName, JsonConvert.SerializeObject(data, Formatting.Indented));
        }

        public void AddTask(string description, string mark)
        {
            var tasks = LoadTasks();
            tasks.Add(new Task { ID = _id++, Description = description, Mark = mark });
            SaveTasks(tasks);
            Console.WriteLine("Task added successfully.");
        }

        public void UpdateTask(int taskId, string newDescription)
        {
            var tasks = LoadTasks();
            var task = tasks.Find(t => t.ID == taskId);
            if (task != null)
            {
                task.Description = newDescription;
                SaveTasks(tasks);
                Console.WriteLine($"Task {taskId} updated successfully.");
            }
            else
            {
                Console.WriteLine($"Task {taskId} not found.");
            }
        }

        public void DeleteTask(int taskId)
        {
            var tasks = LoadTasks();
            var originalCount = tasks.Count;
            tasks.RemoveAll(t => t.ID == taskId);
            SaveTasks(tasks);

            if (tasks.Count < originalCount)
                Console.WriteLine($"Task {taskId} deleted successfully.");
            else
                Console.WriteLine($"Task {taskId} not found.");
        }

        public void MarkTask(int taskId, string mark)
        {
            var tasks = LoadTasks();
            var task = tasks.Find(t => t.ID == taskId);
            if (task != null)
            {
                task.Mark = mark;
                SaveTasks(tasks);
                Console.WriteLine($"Task {taskId} marked as {mark}.");
            }
            else
            {
                Console.WriteLine($"Task {taskId} not found.");
            }
        }

        public void ShowTasks(string filter)
        {
            var tasks = LoadTasks();
            var filteredTasks = filter == "all" ? tasks : tasks.FindAll(t => t.Mark == filter);

            foreach (var task in filteredTasks)
            {
                Console.WriteLine($"ID: {task.ID}, Description: {task.Description}, Mark: {task.Mark}");
            }
        }
    }
}
