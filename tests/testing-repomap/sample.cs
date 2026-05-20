using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace App.Services {

    public interface ILogger {
        void Log(string message);
        void LogError(Exception ex);
    }

    public struct LogEntry {
        public DateTime Timestamp;
        public string Message;
    }

    public class ConsoleLogger : ILogger {
        public void Log(string message) {
            Console.WriteLine($"[{DateTime.Now}] {message}");
        }

        public void LogError(Exception ex) {
            Console.Error.WriteLine(ex.Message);
        }
    }

    public class TaskQueue {
        private readonly Queue<Func<Task>> _queue = new();
        private readonly ILogger _logger;

        public TaskQueue(ILogger logger) {
            _logger = logger;
        }

        public void Enqueue(Func<Task> task) {
            _queue.Enqueue(task);
        }

        public async Task RunNext() {
            if (_queue.TryDequeue(out var task)) {
                await task();
            }
        }

        public int Count() => _queue.Count;
    }
}
