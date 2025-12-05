# Task Tracker CLI

A simple, robust command-line interface (CLI) application to track and manage your tasks.  
This project is a solution to the [Task Tracker](https://roadmap.sh/projects/task-tracker) challenge from roadmap.sh.

The application lets you:

- Add, update, delete tasks  
- Mark tasks as `todo`, `in-progress`, or `done`  
- List all tasks or filter them by status  

All data is stored locally in a JSON file.

---

## 🚀 Features

- **Persistence**  
  Tasks are stored in `tasks.json` in the current directory. The file is created automatically if it does not exist.

- **Full CRUD**  
  - Create tasks (`add`)
  - Read/list tasks (`list`)
  - Update descriptions (`update`)
  - Delete tasks (`delete`)

- **Status tracking**  
  - `todo` (default)
  - `in-progress`
  - `done`

- **Filtering**  
  - List all tasks
  - List only tasks with a specific status (`todo`, `in-progress`, `done`).

- **Error handling**  
  - Invalid IDs
  - Empty descriptions
  - Missing or corrupted JSON file (auto-recovery to an empty structure)

---

## 🧱 Architecture Overview

The project is implemented in a single Python module (`task_Tracker_CLI.py`), but internally it is split into two logical layers:

### 1. CLI Layer (Presentation / Interface)

Responsible for:

- Parsing command-line arguments using `argparse`
- Validating user input (e.g. non-empty descriptions)
- Calling the domain layer functions
- Printing formatted tables and messages to the terminal

Key functions:

- **Command handlers**
  - `cmd_add(args)`
  - `cmd_update(args)`
  - `cmd_delete(args)`
  - `cmd_mark_in_progress(args)`
  - `cmd_mark_done(args)`
  - `cmd_list(args)`

- **Presentation helpers**
  - `print_task_table(task)` — pretty-prints a single task as a table
  - `print_tasks_table(tasks)` — pretty-prints multiple tasks in one table

- **Parser and entry point**
  - `build_parser()` — defines all subcommands (`add`, `update`, `delete`, `mark-in-progress`, `mark-done`, `list`) and binds each one to its handler via `set_defaults(func=...)`
  - `main()` — builds the parser, parses CLI args, and calls `args.func(args)`

---

### 2. Domain Layer (Business Logic + Persistence)

Responsible for:

- How tasks are represented in memory
- How tasks are loaded and saved to JSON
- Operations on tasks (create, update, delete, change status, filter)

Core elements:

- **Constant**

  ```python
  TASKS_FILE = "tasks.json"
  ```

- **Persistence**

  - `load_tasks()`  
    - Reads `TASKS_FILE` if it exists.  
    - If it does not exist or is corrupted, returns a safe default:

      ```python
      {"last_id": 0, "tasks": []}
      ```

  - `save_tasks(data)`  
    - Writes the full `data` dict back to `TASKS_FILE` using `json.dump`.

- **Business logic**

  - `add_task(data, description)`  
    - Generates a new incremental `id` (`last_id + 1`)
    - Creates a task with:
      - `id`
      - `description`
      - `status = "todo"`
      - `createdAt` and `updatedAt` (current timestamp)
    - Updates `data["last_id"]` and appends the task to `data["tasks"]`
    - Returns the created task (dict)

  - `update_task(data, task_id, new_description)`  
    - Finds a task with the given `id`
    - Updates its `description` and `updatedAt`
    - Returns the updated task, or `None` if the ID does not exist

  - `delete_task(data, task_id)`  
    - Removes the task with the given `id` from `data["tasks"]`
    - Returns the deleted task (dict) if found, else `None`

  - `set_task_status(data, task_id, new_status)`  
    - Changes `status` to one of `"todo"`, `"in-progress"`, `"done"`
    - Updates `updatedAt`
    - Returns the updated task if found, else `None`

  - `list_tasks_by_status(data, status)`  
    - Returns:
      - All tasks if `status == "all"`
      - Only tasks whose `status` matches otherwise

---

## 📦 Requirements & Installation

### Requirements

- Python **3.10+** (recommended)
- No external dependencies: only the Python standard library (`argparse`, `json`, `os`, `datetime`)

### Clone the repository

```bash
git clone https://github.com/your-username/task-tracker-cli.git
cd task-tracker-cli
```

*(Replace the URL with your actual repository when you publish it.)*

### Optional: Virtual environment

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1
```

---

## 💻 How to Use the Program (CLI Commands)

The main entry point is:

```bash
python task_Tracker_CLI.py <command> [arguments...]
```

Below is each command and what it does.

---

### 1. `add` — Create a new task

**Syntax:**

```bash
python task_Tracker_CLI.py add "TASK DESCRIPTION"
```

**Behavior:**

- Creates a new task with:
  - Auto-incremented `id`
  - Given `description`
  - `status = "todo"`
  - `createdAt` and `updatedAt` set to the current date and time
- Refuses empty or whitespace-only descriptions.
- Prints the created task as a formatted table.

**Example:**

```bash
python task_Tracker_CLI.py add "Buy groceries"
```

---

### 2. `update` — Update an existing task description

**Syntax:**

```bash
python task_Tracker_CLI.py update <ID> "NEW DESCRIPTION"
```

**Behavior:**

- Loads tasks from `tasks.json`.
- Finds the task with the given `ID`.
- Updates its `description` and `updatedAt`.
- If the ID does not exist, prints an error and does nothing.
- On success, prints the updated task.

**Example:**

```bash
python task_Tracker_CLI.py update 1 "Buy groceries and cook dinner"
```

---

### 3. `delete` — Delete a task

**Syntax:**

```bash
python task_Tracker_CLI.py delete <ID>
```

**Behavior:**

- Loads tasks from `tasks.json`.
- Removes the task with the given `ID` from the list.
- If the task is found:
  - Saves the updated list back to JSON.
  - Prints the deleted task as confirmation.
- If the ID does not exist:
  - Prints: `Error: task with ID <ID> not found.`

**Example:**

```bash
python task_Tracker_CLI.py delete 3
```

---

### 4. `mark-in-progress` — Mark a task as in progress

**Syntax:**

```bash
python task_Tracker_CLI.py mark-in-progress <ID>
```

**Behavior:**

- Loads tasks from `tasks.json`.
- Calls the domain function to set the task status to `"in-progress"`.
- Updates `updatedAt`.
- If the task exists, prints the updated task.
- If not, prints an error.

**Example:**

```bash
python task_Tracker_CLI.py mark-in-progress 2
```

---

### 5. `mark-done` — Mark a task as done

**Syntax:**

```bash
python task_Tracker_CLI.py mark-done <ID>
```

**Behavior:**

- Loads tasks from `tasks.json`.
- Sets the status of the given task to `"done"`.
- Updates `updatedAt`.
- Prints the updated task if successful.
- Prints an error if the `ID` does not exist.

**Example:**

```bash
python task_Tracker_CLI.py mark-done 2
```

---

### 6. `list` — List tasks (optionally filtered by status)

**Syntax:**

```bash
python task_Tracker_CLI.py list [STATUS]
```

Where `STATUS` can be:

- `all`
- `todo`
- `in-progress`
- `done`

If no status is provided, it defaults to `all`.

**Behavior:**

- Loads tasks from `tasks.json`.
- Uses the domain function `list_tasks_by_status` to filter.
- If there are no tasks:
  - For `all`: prints `There are no tasks yet.`
  - For a specific status: prints `There are no tasks with status '<status>'.`
- If there are tasks:
  - Prints a single table containing all matching tasks.

**Examples:**

```bash
# All tasks
python task_Tracker_CLI.py list all

# Only todo tasks
python task_Tracker_CLI.py list todo

# Only in-progress tasks
python task_Tracker_CLI.py list in-progress

# Only done tasks
python task_Tracker_CLI.py list done
```

---

## 🧪 Manual Tests (manual_tests.py)

This project includes a separate script for **manual testing**: `manual_tests.py`.

- No frameworks (`unittest`, `pytest`, etc.)
- Tests call the **domain layer** (`add_task`, `update_task`, `delete_task`, `set_task_status`, `list_tasks_by_status`) directly.
- They use a **separate JSON file**: `tasks_test.json` so they **do not modify** your real `tasks.json`.

### How to run the test menu

From the project root:

```bash
python manual_tests.py
```

You will see a menu like:

```text
==============================
 MANUAL TESTS - TASK TRACKER 
==============================
Using JSON file: tasks_test.json

1) Test add_task
2) Test update_task
3) Test delete_task
4) Test set_task_status (in-progress / done)
5) Test list_tasks_by_status (all / todo / in-progress / done)
6) Show current test JSON
q) Quit
```

You can enter `1`, `2`, `3`, `4`, `5` or `6`, or `q` to quit.

---

### What each test option does

#### `1) Test add_task`

- Resets `tasks_test.json` to an empty structure.
- Calls `add_task` twice to create two tasks.
- Saves them to `tasks_test.json`.
- Prints:
  - The two created tasks.
  - The expectations (IDs, statuses, timestamps).
- Shows the raw JSON and asks you to visually verify it.

#### `2) Test update_task`

- Resets `tasks_test.json`.
- Creates a single task with `"Original description"`.
- Updates that task with `"Updated description"` using `update_task`.
- Saves and prints:
  - Original task
  - Updated task
  - Expectations: same `id`, new `description`, updated `updatedAt`.
- Shows `tasks_test.json` so you can confirm the changes.

#### `3) Test delete_task`

- Resets `tasks_test.json`.
- Creates two tasks:
  - `"Task to delete"`
  - `"Task to keep"`
- Deletes the first one using `delete_task`.
- Saves changes.
- Prints the deleted task and explains what you should see:
  - Only `"Task to keep"` left in `tasks_test.json`.
  - `last_id` remains `2` (IDs are not renumbered).

#### `4) Test set_task_status`

- Resets `tasks_test.json`.
- Creates one task `"Task to change status"`.
- Calls `set_task_status` twice:
  - First to `"in-progress"`
  - Then to `"done"`
- After each change, saves and prints the result.
- Explains what to verify:
  - Status transitions: `todo → in-progress → done`
  - `updatedAt` changes each time.

#### `5) Test list_tasks_by_status`

- Resets `tasks_test.json`.
- Creates three tasks:
  - Task A → stays `todo`
  - Task B → set to `in-progress`
  - Task C → set to `done`
- Calls:
  - `list_tasks_by_status(..., "all")`
  - `list_tasks_by_status(..., "todo")`
  - `list_tasks_by_status(..., "in-progress")`
  - `list_tasks_by_status(..., "done")`
- Prints the IDs returned by each call.
- Explains what you should check:
  - `"all"` contains the 3 IDs
  - `"todo"` only contains Task A’s ID
  - `"in-progress"` only Task B’s ID
  - `"done"` only Task C’s ID

#### `6) Show current test JSON`

- Simply prints the current contents of `tasks_test.json` to the terminal so you can inspect it at any time.

---

## 📂 Data Files

- `tasks.json`  
  - Main data file used by the CLI application.
  - Created automatically if it does not exist.

- `tasks_test.json`  
  - Data file used **only** by `manual_tests.py`.
  - Keeps test data separate from your real tasks.

Both follow the same structure:

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

You are free to use, modify, and distribute this code, as long as you include the copyright and license notice in your copies or substantial portions of the software.

See the `LICENSE` file for full details (when added to the repository).