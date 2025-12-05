# Task Tracker CLI

A simple, robust command-line interface (CLI) application to track and manage your tasks. This project is a solution to the [Task Tracker](https://roadmap.sh/projects/task-tracker) challenge from roadmap.sh.

The application allows you to add, update, delete, and list tasks, as well as track their status (todo, in-progress, done). All data is persisted locally in a JSON file.

---

## 🚀 Features

- **Persistence:** Tasks are saved automatically to `tasks.json`.
- **CRUD Operations:** Create, Read (List), Update, and Delete tasks.
- **Status Tracking:** Mark tasks as `todo`, `in-progress`, or `done`.
- **Filtering:** List all tasks or filter them by specific status.
- **Error Handling:** Robust handling of invalid IDs, empty descriptions, or missing files.

---

## 🛠️ Usage Guide

You can run the application using Python directly from your terminal. Ensure you have Python installed.

### 1. Add a Task
Create a new task. The ID is auto-generated, and the default status is `todo`.

```bash
python task_Tracker_CLI.py add "Buy groceries"