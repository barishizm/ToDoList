import tkinter as tk
from tkinter import filedialog, messagebox
import unittest

class TaskFactory:
    """Factory Method for creating tasks."""
    @staticmethod
    def create_task(task_name):
        return task_name

class TaskManagerSingleton:
    """Singleton for managing tasks."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TaskManagerSingleton, cls).__new__(cls)
            cls._instance.tasks = []
        return cls._instance

    def add_task(self, task):
        self.tasks.append(task)

    def edit_task(self, index, new_task):
        self.tasks[index] = new_task

    def delete_task(self, index):
        self.tasks.pop(index)

    def get_tasks(self):
        return self.tasks

class ToDoListApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do")
        self.geometry("400x400")
        self.task_manager = TaskManagerSingleton()  # Singleton instance
        self._create_widgets()

    def _create_widgets(self):
        self._task_input = tk.Entry(self, width=30)
        self._task_input.pack(padx=10, pady=10)

        self._add_task_button = tk.Button(self, text="Add Task", command=self._add_task)
        self._add_task_button.pack(pady=5)

        self._tasks_list_box = tk.Listbox(self, selectmode=tk.SINGLE, height=10, width=35)
        self._tasks_list_box.pack(padx=10, pady=10)

        self._button_frame = tk.Frame(self)
        self._button_frame.pack(pady=5)

        self._edit_task_button = tk.Button(self._button_frame, text="Edit Task", command=self._edit_task)
        self._edit_task_button.grid(row=0, column=0, padx=5)

        self._delete_task_button = tk.Button(self._button_frame, text="Delete Task", command=self._delete_task)
        self._delete_task_button.grid(row=0, column=1, padx=5)

        self._save_task_button = tk.Button(self, text="Save Tasks", command=self._save_tasks)
        self._save_task_button.pack(pady=5)

        self._load_task_button = tk.Button(self, text="Load Tasks", command=self._load_tasks)
        self._load_task_button.pack(pady=5)

    def _add_task(self):
        task = self._task_input.get()
        if task:
            new_task = TaskFactory.create_task(task)
            self.task_manager.add_task(new_task)
            self._tasks_list_box.insert(tk.END, new_task)
            self._task_input.delete(0, tk.END)

    def _edit_task(self):
        try:
            index = self._tasks_list_box.curselection()[0]
            new_task = self._task_input.get()
            if new_task:
                if messagebox.askyesno("Edit Task", f"Are you sure you want to edit the task to: {new_task}?"):
                    self.task_manager.edit_task(index, new_task)
                    self._tasks_list_box.delete(index)
                    self._tasks_list_box.insert(index, new_task)
                    self._task_input.delete(0, tk.END)
        except IndexError:
            messagebox.showinfo("Edit Task", "Please select a task to edit.")

    def _delete_task(self):
        try:
            index = self._tasks_list_box.curselection()[0]
            if messagebox.askyesno("Delete Task", "Are you sure you want to delete the selected task?"):
                self.task_manager.delete_task(index)
                self._tasks_list_box.delete(index)
        except IndexError:
            messagebox.showinfo("Delete Task", "Please select a task to delete.")

    def _save_tasks(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as f:
                for task in self.task_manager.get_tasks():
                    f.write(task + "\n")

    def _load_tasks(self):
        self._tasks_list_box.delete(0, tk.END)
        self.task_manager.tasks.clear()
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as f:
                for line in f:
                    task = line.strip()
                    if task:
                        self.task_manager.add_task(task)
                        self._tasks_list_box.insert(tk.END, task)

#inheritence, advancedtodolistapp isimli subclass todolistappden miras aldı.
class AdvancedToDoListApp(ToDoListApp):
    def _add_task(self):
        task = self._task_input.get()
        if task:
            if messagebox.askyesno("Add Task", f"Are you sure you want to add the task: {task}?"):
                new_task = TaskFactory.create_task(task)
                self.task_manager.add_task(new_task)
                self._tasks_list_box.insert(tk.END, new_task)
                self._task_input.delete(0, tk.END)

    def _edit_task(self):
        try:
            index = self._tasks_list_box.curselection()[0]
            new_task = self._task_input.get()
            if new_task:
                if messagebox.askyesno("Edit Task", f"Are you sure you want to edit the task to: {new_task}?"):
                    self.task_manager.edit_task(index, new_task)
                    self._tasks_list_box.delete(index)
                    self._tasks_list_box.insert(index, new_task)
                    self._task_input.delete(0, tk.END)
        except IndexError:
            messagebox.showinfo("Edit Task", "Please select a task to edit.")

# Unit Tests
class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManagerSingleton()

    def tearDown(self):
        TaskManagerSingleton._instance = None  # Reset the singleton instance for each test

    def test_add_task(self):
        self.task_manager.add_task("Task 1")
        self.assertIn("Task 1", self.task_manager.get_tasks())

    def test_edit_task(self):
        self.task_manager.add_task("Task 1")
        self.task_manager.edit_task(0, "Task 1 Edited")
        self.assertIn("Task 1 Edited", self.task_manager.get_tasks())
        self.assertNotIn("Task 1", self.task_manager.get_tasks())

    def test_delete_task(self):
        self.task_manager.add_task("Task 1")
        self.task_manager.delete_task(0)
        self.assertNotIn("Task 1", self.task_manager.get_tasks())

if __name__ == "__main__":
    # Run the application
    app = AdvancedToDoListApp()
    app.mainloop()
    # Run the unit tests
    unittest.main(exit=False)
