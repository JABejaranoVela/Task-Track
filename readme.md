# Task Tracker CLI

A simple, robust command-line interface (CLI) application to track and manage your tasks.  
This project is a solution to the [Task Tracker](https://roadmap.sh/projects/task-tracker) challenge from roadmap.sh. :contentReference[oaicite:0]{index=0}

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
  - List only tasks with a specific status (`todo`, `in-progress`, `in-progress`, `done`).

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


License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this code, as long as you include the copyright and license notice in your copies or substantial portions of the software.

See the LICENSE file for full details (when added to the repository).