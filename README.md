
# Task Tracker CLI

Small command‑line app to track your tasks.  
Solution for the [Task Tracker](https://roadmap.sh/projects/task-tracker) project.

It lets you:

- Add, update and delete tasks
- Mark tasks as `todo`, `in-progress` or `done`
- List all tasks or filter by status

All data is stored in a local JSON file.

---

## 🔧 Installation

Requirements:

- Python **3.10+**

Clone the repo and install in editable mode:

```bash
git clone https://github.com/JABejaranoVela/Task-Track
cd Task-Track

python -m venv .venv
source .venv/bin/activate      # Linux / macOS
# .venv\Scripts\activate     # Windows

pip install -e .
```

This will install a CLI command called `task-cli`.

---

## 🚀 Usage

Basic syntax:

```bash
task-cli <command> [arguments...]
```

### Main commands

```bash
# Add a task
task-cli add "Buy groceries"

# Update a task
task-cli update 1 "Buy groceries and cook dinner"

# Delete a task
task-cli delete 1

# Change status
task-cli mark-in-progress 2
task-cli mark-done 2

# List tasks
task-cli list            # same as: task-cli list all
task-cli list todo
task-cli list in-progress
task-cli list done
```

- New tasks start as `status = "todo"`.
- `createdAt` and `updatedAt` are stored as timestamps.
- If an ID does not exist, the CLI prints an error message.

---

## 🧪 Manual tests

This project includes **manual domain tests** that use a separate JSON file  
(`tasks_test.json`) so you don’t break your real data.

From the project root:

```bash
python tests/manual_tests.py
```

The script shows a small menu to test:

1. `add_task`
2. `update_task`
3. `delete_task`
4. `set_task_status`
5. `list_tasks_by_status`
6. Show the current test JSON

Each option:

- Resets or modifies `tasks_test.json`
- Calls the domain functions directly
- Prints expectations so you can visually verify the results

---

## 📜 License

This project is licensed under the **MIT License**.
You are free to use, modify and distribute it under the terms of that license.