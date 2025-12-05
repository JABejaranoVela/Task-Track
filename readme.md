# Task Tracker CLI

A simple, robust command-line interface (CLI) application to track and manage your tasks.  
This project is a solution to the [Task Tracker](https://roadmap.sh/projects/task-tracker) challenge from roadmap.sh.

The application lets you:

- Add, update, delete tasks  
- Mark tasks as `todo`, `in-progress`, or `done`  
- List all tasks or filter them by status  

All data is stored locally in a JSON file.

---

## 📦 Requirements & Installation

### Requirements

- Python **3.10+** recommended

### Install / setup

Clone the repo:

```bash
git clone https://github.com/your-username/task-tracker-cli.git
cd task-tracker-cli
```

(Optional) create and activate a virtualenv:

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1
```

---

## 💻 Usage

All commands follow this pattern:

```bash
python task_Tracker_CLI.py <command> [arguments...]
```

### Commands

#### 1. Add a task

```bash
python task_Tracker_CLI.py add "TASK DESCRIPTION"
```

- Creates a new task with:
  - Auto‑incremented `id`
  - `status = "todo"`
  - `createdAt` and `updatedAt` set to now  
- Description cannot be empty or only spaces.

#### 2. Update a task

```bash
python task_Tracker_CLI.py update <ID> "NEW DESCRIPTION"
```

- Changes the description of the task with that `ID`.
- Updates `updatedAt`.
- If the ID does not exist, prints an error.

#### 3. Delete a task

```bash
python task_Tracker_CLI.py delete <ID>
```

- Removes the task with that `ID` from `tasks.json`.
- Shows the deleted task as confirmation.
- If the ID does not exist, prints an error.

#### 4. Mark task as in progress

```bash
python task_Tracker_CLI.py mark-in-progress <ID>
```

- Sets `status = "in-progress"` for the given task.
- Updates `updatedAt`.

#### 5. Mark task as done

```bash
python task_Tracker_CLI.py mark-done <ID>
```

- Sets `status = "done"` for the given task.
- Updates `updatedAt`.

#### 6. List tasks

```bash
python task_Tracker_CLI.py list [STATUS]
```

Where `STATUS` can be:

- `all` (default if omitted)
- `todo`
- `in-progress`
- `done`

Examples:

```bash
python task_Tracker_CLI.py list
python task_Tracker_CLI.py list all
python task_Tracker_CLI.py list todo
python task_Tracker_CLI.py list in-progress
python task_Tracker_CLI.py list done
```

The output is a single table with all matching tasks.

---

## 🧪 Manual Tests

There is a separate script for manual tests: `tests.py`.

It uses a different JSON file (`tasks_test.json`) so tests do **not** modify your real `tasks.json`.

### Run the tests

From the project root:

```bash
python manual_tests.py
```

You will see a simple menu where you can:

1. Test `add_task`
2. Test `update_task`
3. Test `delete_task`
4. Test `set_task_status`
5. Test `list_tasks_by_status`
6. Show the current contents of `tasks_test.json`

Each option:

- Resets or modifies `tasks_test.json`
- Calls the domain functions directly
- Prints expectations so you can check the JSON by hand

This matches the project requirement of “testing each feature manually and reviewing the JSON file”.

---

## 📂 Data files

- `tasks.json` — main data file for the CLI app.
- `tasks_test.json` — used only by `manual_tests.py` for manual testing.

Both share this shape:

```json
{
  "last_id": 3,
  "tasks": [
    {
      "id": 1,
      "description": "Example task",
      "status": "todo",
      "createdAt": "28/11/2025 16:19:01",
      "updatedAt": "28/11/2025 16:19:01"
    }
  ]
}
```

---

## 📜 License

This project is licensed under the **MIT License**.

You are free to use, modify and distribute this code, as long as you keep the copyright
and license notice in your copies or substantial portions of the software.