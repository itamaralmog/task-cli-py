using System;

namespace TaskCLI
{
    internal class Program
    {
        private static void Main(string[] args)
        {
            var taskManager = new TaskManager();
            while (true)
            {
                Console.Write("task-cli> ");
                var input = Console.ReadLine()?.Split(" ");
                if (input == null || input.Length == 0) continue;

                var command = input[0];
                switch (command)
                {
                    case "add":
                        taskManager.AddTask(string.Join(" ", input[1..]), "todo");
                        break;
                    case "update":
                        taskManager.UpdateTask(int.Parse(input[1]), string.Join(" ", input[2..]));
                        break;
                    case "delete":
                        taskManager.DeleteTask(int.Parse(input[1]));
                        break;
                    case "mark-in-progress":
                        taskManager.MarkTask(int.Parse(input[1]), "in-progress");
                        break;
                    case "mark-done":
                        taskManager.MarkTask(int.Parse(input[1]), "done");
                        break;
                    case "list":
                        taskManager.ShowTasks(input.Length > 1 ? input[1] : "all");
                        break;
                    case "exit":
                        Console.WriteLine("Exiting CLI.");
                        return;
                    default:
                        Console.WriteLine("Unknown command.");
                        break;
                }
            }
        }
    }
}
