import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="task-cli",
        description="A CLI application to efficiently manage your tasks",
    )

    # GRUPO DE SUBCOMANDOS (add, update, delete, etc.)
    subparsers = parser.add_subparsers(
        dest="command",  # aquí se guardará el nombre del subcomando usado
        required=True,  # obliga a poner un comando (add, update, ...)
    )

    # ---------- task-cli add "Buy groceries" ----------
    # subcomando: add, subparser = qué comando se ha elegido
    add_parser = subparsers.add_parser(
        "add",  # task-cli add ...
        help="Add a new task",
    )

    # argumento posicional de 'add': la descripción, add_argument = qué datos recibe ese comando
    add_parser.add_argument(
        "description",  # args.description
        type=str,  # será un string
        help="Task description",  # ayuda de este argumento
    )

    # ---------- task-cli update 1 "New description" ----------
    update_parser = subparsers.add_parser(
        "update",
        help="Add a new task",
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

    # ---------- task-cli list [status] ----------
    # status opcional: todo | in-progress | done (o all si no se pasa)
    list_parser = subparsers.add_parser(
        "list",
        help="List tasks (optionally filtered by status)",
    )
    list_parser.add_argument(
        "status",
        nargs="?",  # opcional
        choices=["todo", "in-progress", "done", "all"],
        default="all",
        help="Filter tasks by status (todo, in-progress, done, all)",
    )

    # parseamos los argumentos escritos en la terminal
    args: argparse.Namespace = parser.parse_args()

    if args.command == "add":
        add_Function(args.description)
    # elif args.command == "update":
    #     update_Function(...)
    # elif args.command == "delete":
    #     delete_Function(...)


def add_Function(description: str):
    print("-----------------------------------------")
    print("We are add the task:", description)


def update_Function(id: int, description: str):
    print("-----------------------------------------")
    print("We are add the task: ")


def delete_Function():
    print("-----------------------------------------")
    task = input("Selection the task: ")
    print("We are add the task: ", task)


if __name__ == "__main__":
    main()
