using System;
using System.IO;
using Xunit;

namespace TaskCLITests
{
    public class TaskManagerTests
    {
        private const string FileName = "tasks.json";

        public TaskManagerTests()
        {
            if (File.Exists(FileName)) File.Delete(FileName);
        }

        private void PrintJsonContents(string step)
        {
            Console.WriteLine($"--- JSON Contents after {step} ---");
            if (File.Exists(FileName))
            {
                Console.WriteLine(File.ReadAllText(FileName));
            }
            else
            {
                Console.WriteLine("No JSON file exists.");
            }
            Console.WriteLine("-----------------------------------");
        }

        [Fact]
        public void TestAddTask()
        {
            var manager = new TaskCLI.TaskManager();
            manager.AddTask("Test Task", "todo");
            PrintJsonContents("AddTask");
            Assert.True(File.Exists(FileName), "JSON file should be created.");
        }

        [Fact]
        public void TestUpdateTask()
        {
            var manager = new TaskCLI.TaskManager();
            manager.AddTask("Task to Update", "todo");
            PrintJsonContents("AddTask");
            manager.UpdateTask(2, "Updated Task");
            PrintJsonContents("UpdateTask");
            Assert.True(File.ReadAllText(FileName).Contains("Updated Task"));
        }

        [Fact]
        public void TestDeleteTask()
        {
            var manager = new TaskCLI.TaskManager();
            manager.AddTask("Task to Delete", "todo");
            PrintJsonContents("AddTask");
            manager.DeleteTask(4);
            PrintJsonContents("DeleteTask");
            Assert.False(File.ReadAllText(FileName).Contains("Task to Delete"));
        }

        [Fact]
        public void TestMarkTask()
        {
            var manager = new TaskCLI.TaskManager();
            manager.AddTask("Task to Mark", "todo");
            PrintJsonContents("AddTask");
            manager.MarkTask(1, "done");
            PrintJsonContents("MarkTask");
            Assert.True(File.ReadAllText(FileName).Contains("\"Mark\": \"done\""));
        }
    }
}
