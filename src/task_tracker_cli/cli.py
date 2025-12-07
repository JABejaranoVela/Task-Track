import argparse
import json
import os
from datetime import datetime


# ===== CLI LAYER: command handlers / Interface =====
def print_task_table(task: dict) -> None:
    """
    Print a table with a single task with columns:
    Id | Description | Status | Created At | Updated At
    """
    headers = ["Id", "Description", "Status", "Created At", "Updated At"]
    row = [
        str(task["id"]),
        task["description"],
        task["status"],
        task["createdAt"],
        task["updatedAt"],
    ]

    # Compute column widths (max between header and value)
    widths = [max(len(headers[i]), len(row[i])) for i in range(len(headers))]

    def make_border() -> str:
        parts = ["+" + "-" * (w + 2) for w in widths]
        return "".join(parts) + "+"

    def make_row(values) -> str:
        cells = []
        for i, value in enumerate(values):
            cells.append("| " + value.ljust(widths[i]) + " ")
        return "".join(cells) + "|"

    border = make_border()
    header_line = make_row(headers)
    row_line = make_row(row)

    print(border)
    print(header_line)
    print(border)
    print(row_line)
    print(border)


def print_tasks_table(tasks: list[dict]) -> None:
    """
    Print a table with multiple tasks (one row per task).
    """
    headers = ["Id", "Description", "Status", "Created At", "Updated At"]

    # 1) Convert all tasks into rows of strings
    rows: list[list[str]] = []
    for task in tasks:
        row = [
            str(task.get("id", "")),
            str(task.get("description", "")),
            str(task.get("status", "")),
            str(task.get("createdAt", "")),
            str(task.get("updatedAt", "")),
        ]
        rows.append(row)

    # 2) Compute widths per column considering all rows
    widths = []
    for col_index in range(len(headers)):
        max_header = len(headers[col_index])
        max_cells = max(len(row[col_index]) for row in rows) if rows else 0
        widths.append(max(max_header, max_cells))

    def make_border() -> str:
        parts = ["+" + "-" * (w + 2) for w in widths]
        return "".join(parts) + "+"

    def make_row(values: list[str]) -> str:
        cells = []
        for i, value in enumerate(values):
            text = str(value)
            cells.append("| " + text.ljust(widths[i]) + " ")
        return "".join(cells) + "|"

    border = make_border()
    print(border)
    print(make_row(headers))
    print(border)

    # 3) Print all rows
    for row in rows:
        print(make_row(row))

    print(border)


def cmd_add(args: argparse.Namespace):
    """Handler for: task-cli add DESCRIPTION"""

    # 0) Validate that the description is not empty (or only spaces)
    description = args.description.strip()
    if not description:
        print("Error: task description cannot be empty.")
        return

    # 1) Load current tasks state from JSON
    data = load_tasks()

    # 2) Add the new task to that in-memory structure
    new_task = add_task(data, description)

    # 3) Save the updated data to disk
    save_tasks(data)

    # 4) Print a table with the created task
    print_task_table(new_task)


def cmd_update(args: argparse.Namespace):
    """Handler for: task-cli update ID DESCRIPTION"""

    # 0) Validate that the new description is not empty (or only spaces)
    new_description = args.description.strip()
    if not new_description:
        print("Error: task description cannot be empty.")
        return

    # 1) Load current tasks state from JSON
    data = load_tasks()

    # 2) Try to update the task in the domain layer
    updated_task = update_task(data, args.id, new_description)

    if updated_task is None:
        # No task found with that id
        print(f"Error: task with ID {args.id} not found.")
        return

    # 3) Save changes to disk
    save_tasks(data)

    # 4) Print the updated task
    print_task_table(updated_task)


def cmd_delete(args: argparse.Namespace):
    """Handler for: task-cli delete ID"""

    # 1) Load current tasks state from JSON
    data = load_tasks()

    # 2) Try to delete the task in the domain layer
    deleted_task = delete_task(data, args.id)

    if deleted_task is None:
        # No task found with that id
        print(f"Error: task with ID {args.id} not found.")
        return

    # 3) Save changes to disk
    save_tasks(data)

    # 4) Show the deleted task (even though it is no longer in the file)
    print("Task deleted:")
    print_task_table(deleted_task)


def cmd_mark_in_progress(args: argparse.Namespace):
    """Handler for: task-cli mark-in-progress ID"""

    # 1) Load current tasks state from JSON
    data = load_tasks()

    # 2) Try to change status in the domain layer
    updated_task = set_task_status(data, args.id, "in-progress")

    if updated_task is None:
        # No task found with that id
        print(f"Error: task with ID {args.id} not found.")
        return

    # 3) Save changes to disk
    save_tasks(data)

    # 4) Print the updated task
    print_task_table(updated_task)


def cmd_mark_done(args: argparse.Namespace):
    """Handler for: task-cli mark-done ID"""

    # 1) Load current tasks state from JSON
    data = load_tasks()

    # 2) Try to change status in the domain layer
    updated_task = set_task_status(data, args.id, "done")

    if updated_task is None:
        # No task found with that id
        print(f"Error: task with ID {args.id} not found.")
        return

    # 3) Save changes to disk
    save_tasks(data)

    # 4) Print the updated task
    print_task_table(updated_task)


def cmd_list(args: argparse.Namespace):
    """Handler for: task-cli list [status]"""

    # 1) Load current tasks state from JSON
    data = load_tasks()

    # 2) Ask the domain layer for the filtered list
    tasks = list_tasks_by_status(data, args.status)

    # 3) If there are no tasks, inform the user and exit
    if not tasks:
        if args.status == "all":
            print("There are no tasks yet.")
        else:
            print(f"There are no tasks with status '{args.status}'.")
        return

    # 4) Print all tasks in a single table
    print_tasks_table(tasks)


# ===== DOMAIN LAYER: task logic / JSON =====
TASKS_FILE = "tasks.json"


def load_tasks() -> dict:
    """
    Load tasks from the JSON file.
    - If the file does not exist, return an empty structure: {"last_id": 0, "tasks": []}
    """
    # 1) Check if the file exists
    if not os.path.exists(TASKS_FILE):
        # Initial standard structure of our program
        return {"last_id": 0, "tasks": []}

    # 2) If it exists, try to read it as JSON
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        # File is corrupted or not valid JSON
        # Decision: instead of crashing, return an empty structure
        return {"last_id": 0, "tasks": []}

    # 3) Normalize minimum keys in case something is missing
    if "last_id" not in data:
        data["last_id"] = 0
    if "tasks" not in data:
        data["tasks"] = []

    return data


def save_tasks(data: dict) -> None:
    """
    Save the 'data' structure (last_id + tasks) to TASKS_FILE.
    - Overwrites the previous contents of the file.
    """
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_task(data: dict, description: str) -> dict:
    """
    Add a new task to 'data' with the given description.
    - Compute a new id (using data['last_id'] + 1, for example).
    - Create the task with fields: id, description, status='todo', createdAt, updatedAt.
    - Update data['last_id'] and append the task to data['tasks'].
    - Return the created task (dict).
    """
    # Just in case: ensure minimal structure
    last_id = data.get("last_id", 0)
    tasks = data.get("tasks", [])

    new_id = last_id + 1
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": date,
        "updatedAt": date,
    }

    tasks.append(task)

    # Save back into the original dict
    data["last_id"] = new_id
    data["tasks"] = tasks

    return task


def update_task(data: dict, task_id: int, new_description: str) -> dict | None:
    """
    Update the description of the task with id == task_id.
    - Search the task in data['tasks'].
    - If found, change its description and updatedAt.
    - Return the updated task (dict) if it exists.
    - Return None if no task with that id is found.
    """
    tasks = data.get("tasks", [])

    for task in tasks:
        if task.get("id") == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            return task

    # No task found with that id
    return None


def delete_task(data: dict, task_id: int) -> dict | None:
    """
    Delete the task with id == task_id from data['tasks'].
    - If found and deleted, return the deleted task (dict).
    - If no task with that id exists, return None.
    """
    tasks = data.get("tasks", [])

    for index, task in enumerate(tasks):
        if task.get("id") == task_id:
            # Store the task that we are going to delete
            deleted_task = tasks.pop(index)
            # For clarity, reassign the list to data (same reference, but explicit)
            data["tasks"] = tasks
            return deleted_task

    # No task found with that id
    return None


def set_task_status(data: dict, task_id: int, new_status: str) -> dict | None:
    """
    Change the status of the task with id == task_id.
    - new_status will be 'todo', 'in-progress' or 'done'.
    - If the task exists, update its status and updatedAt and return the task (dict).
    - If no task with that id exists, return None.
    """
    tasks = data.get("tasks", [])

    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = new_status
            task["updatedAt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            return task

    # No task found with that id
    return None


def list_tasks_by_status(data: dict, status: str) -> list[dict]:
    """
    Return a list of tasks filtered by status.
    - status can be: 'todo', 'in-progress', 'done' or 'all'.
    - If 'all', return all tasks.
    - Otherwise, return only tasks with that status.
    """
    tasks = data.get("tasks", [])

    if status == "all":
        # Return a copy so callers don’t accidentally modify the internal list
        return list(tasks)

    # Filter by status value
    filtered = [task for task in tasks if task.get("status") == status]
    return filtered


# ===== CLI LAYER: parser construction =====
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task-cli",
        description="A CLI application to efficiently manage your tasks",
    )

    # GROUP OF SUBCOMMANDS (add, update, delete, etc.)
    subparsers = parser.add_subparsers(
        dest="command",  # name of the chosen subcommand will be stored here
        required=True,  # force user to provide a subcommand (add, update, ...)
    )

    # ---------- task-cli add "Buy groceries" ----------
    # subcommand: add
    add_parser = subparsers.add_parser(
        "add",  # task-cli add ...
        help="Add a new task",
    )

    # positional argument of 'add': the description
    add_parser.add_argument(
        "description",  # args.description
        type=str,
        help="Task description",
    )
    # associate this subcommand with its handler cmd_add
    add_parser.set_defaults(func=cmd_add)

    # ---------- task-cli update 1 "New description" ----------
    update_parser = subparsers.add_parser(
        "update",
        help="Update an existing task",
    )

    update_parser.add_argument(
        "id",
        type=int,
        help="Task ID to update",
    )

    update_parser.add_argument(
        "description",
        type=str,
        help="New description for the task",
    )
    update_parser.set_defaults(func=cmd_update)

    # ---------- task-cli delete 1 ----------
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a task",
    )
    delete_parser.add_argument(
        "id",
        type=int,
        help="Task ID to delete",
    )
    delete_parser.set_defaults(func=cmd_delete)

    # ---------- task-cli mark-in-progress 1 ----------
    mip_parser = subparsers.add_parser(
        "mark-in-progress",
        help="Mark a task as in progress",
    )
    mip_parser.add_argument(
        "id",
        type=int,
        help="Task ID to mark as in progress",
    )
    mip_parser.set_defaults(func=cmd_mark_in_progress)

    # ---------- task-cli mark-done 1 ----------
    md_parser = subparsers.add_parser(
        "mark-done",
        help="Mark a task as done",
    )
    md_parser.add_argument(
        "id",
        type=int,
        help="Task ID to mark as done",
    )
    md_parser.set_defaults(func=cmd_mark_done)

    # ---------- task-cli list [status] ----------
    # optional status: todo | in-progress | done | all (default)
    list_parser = subparsers.add_parser(
        "list",
        help="List all tasks, optionally filtered by status (todo, in-progress, done, all)",
    )
    list_parser.add_argument(
        "status",
        nargs="?",  # optional
        choices=["todo", "in-progress", "done", "all"],
        default="all",
        help="Filter tasks by status (todo, in-progress, done, all)",
    )
    list_parser.set_defaults(func=cmd_list)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # args.func comes from the set_defaults() of the selected subcommand
    args.func(args)


if __name__ == "__main__":
    main()
