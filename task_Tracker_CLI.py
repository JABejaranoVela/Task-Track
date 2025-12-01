import argparse
import json
import os
from datetime import datetime


# ===== CAPA CLI: handlers de comandos / Interfaz =====
def print_task_table(task: dict) -> None:
    """
    Imprime una tabla con una sola tarea, con columnas:
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

    # Calcular ancho de cada columna (máximo entre cabecera y valor)
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


def cmd_add(args: argparse.Namespace):
    """Handler para: task-cli add DESCRIPTION"""

    # 0) Validar que la descripción no esté vacía (ni solo espacios)
    description = args.description.strip()
    if not description:
        print("Error: task description cannot be empty.")
        return

    # 1) Cargar estado actual de tareas desde el JSON
    data = load_tasks()

    # 2) Añadir la nueva tarea a esa estructura en memoria
    new_task = add_task(data, args.description)

    # 3) Guardar de nuevo en disco
    save_tasks(data)

    # 4) Mostrar tabla con la tarea creada
    print_task_table(new_task)


def cmd_update(args: argparse.Namespace):
    """Handler para: task-cli update ID DESCRIPTION"""
    print("-----------------------------------------")

    # 0) Validar que la nueva descripción no esté vacía (ni solo espacios)
    new_description = args.description.strip()
    if not new_description:
        print("Error: task description cannot be empty.")
        return

    # 1) Cargar estado actual de tareas desde el JSON
    data = load_tasks()

    # 2) Intentar actualizar la tarea en la capa de dominio
    updated_task = update_task(data, args.id, new_description)

    if updated_task is None:
        # No existe una tarea con ese id
        print(f"Error: task with ID {args.id} not found.")
        return

    # 3) Guardar cambios en disco
    save_tasks(data)

    # 4) Mostrar la tarea actualizada
    print_task_table(updated_task)


def cmd_delete(args: argparse.Namespace):
    """Handler para: task-cli delete ID"""

    # 1) Cargar estado actual de tareas desde el JSON
    data = load_tasks()

    # 2) Intentar eliminar la tarea en la capa de dominio
    deleted_task = delete_task(data, args.id)

    if deleted_task is None:
        # No existe una tarea con ese id
        print(f"Error: task with ID {args.id} not found.")
        return

    # 3) Guardar cambios en disco
    save_tasks(data)

    # 4) Mostrar la tarea eliminada (aunque ya no esté en el archivo)
    print("Task deleted:")
    print_task_table(deleted_task)


def cmd_mark_in_progress(args: argparse.Namespace):
    """Handler para: task-cli mark-in-progress ID"""
    print("-----------------------------------------")
    print(f"We are mark IN PROGRESS the task with id={args.id}")


def cmd_mark_done(args: argparse.Namespace):
    """Handler para: task-cli mark-done ID"""
    print("-----------------------------------------")
    print(f"We are mark DONE the task with id={args.id}")


def cmd_list(args: argparse.Namespace):
    """Handler para: task-cli list [status]"""
    print("-----------------------------------------")
    print("We are list tasks with status:", args.status)


# ===== CAPA DE DOMINIO: lógica de tareas / JSON =====
TASKS_FILE = "tasks.json"


def load_tasks() -> dict:
    """
    Carga las tareas desde el archivo JSON.
    - Si el archivo no existe, devuelve una estructura vacía: {"last_id": 0, "tasks": []}
    - Más adelante implementaremos aquí la lectura de JSON.
    """
    # 1) Comprobar si existe el archivo
    if not os.path.exists(TASKS_FILE):
        # Estructura inicial estándar de nuestro programa
        return {"last_id": 0, "tasks": []}

    # 2) Si existe, intentamos leerlo como JSON
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        # Archivo corrupto o con formato no válido
        # Decisión: en lugar de petar el programa, devolvemos estructura vacía
        return {"last_id": 0, "tasks": []}

    # 3) Normalizar mínimos por si faltan claves
    if "last_id" not in data:
        data["last_id"] = 0
    if "tasks" not in data:
        data["tasks"] = []

    return data


def save_tasks(data: dict) -> None:
    """
    Guarda en disco la estructura 'data' (last_id + tasks) en TASKS_FILE.
    - Sobrescribe el contenido anterior del archivo.
    - Usa json.dump cuando lo implementemos.
    """
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def add_task(data: dict, description: str) -> dict:
    """
    Añade una nueva tarea a 'data' con la descripción dada.
    - Calcula un nuevo id (usando data['last_id'] + 1, por ejemplo).
    - Crea la tarea con campos: id, description, status='todo', createdAt y updatedAt (timestamps).
    - Actualiza data['last_id'] y añade la tarea a data['tasks'].
    - Devuelve la tarea creada (dict).
    """
    # Por si acaso: asegurar estructura mínima
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

    # Guardar de vuelta en el dict original
    data["last_id"] = new_id
    data["tasks"] = tasks

    return task


def update_task(data: dict, task_id: int, new_description: str) -> dict | None:
    """
    Actualiza la descripción de la tarea con id == task_id.
    - Busca la tarea en data['tasks'].
    - Si la encuentra, cambia su description y updatedAt.
    - Devuelve la tarea actualizada (dict) si existe.
    - Devuelve None si no se encontró ninguna tarea con ese id.
    """
    tasks = data.get("tasks", [])

    for task in tasks:
        if task.get("id") == task_id:
            task["description"] = new_description
            task["updatedAt"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            return task

    # No se ha encontrado ninguna tarea con ese id
    return None


def delete_task(data: dict, task_id: int) -> dict | None:
    """
    Elimina la tarea con id == task_id de data['tasks'].
    - Si la encuentra y la elimina, devuelve la tarea eliminada (dict).
    - Si no existe ninguna tarea con ese id, devuelve None.
    """
    tasks = data.get("tasks", [])

    for index, task in enumerate(tasks):
        if task.get("id") == task_id:
            # Guardamos la tarea que vamos a eliminar
            deleted_task = tasks.pop(index)
            # Por claridad, reasignamos la lista a data (aunque es la misma referencia)
            data["tasks"] = tasks
            return deleted_task

    # No se ha encontrado ninguna tarea con ese id
    return None


def set_task_status(data: dict, task_id: int, new_status: str) -> bool:
    """
    Cambia el status de la tarea con id == task_id.
    - new_status será 'todo', 'in-progress' o 'done'.
    - Si la tarea existe, actualiza su status y updatedAt, devuelve True.
    - Si no existe, devuelve False.
    """
    pass


def list_tasks_by_status(data: dict, status: str) -> list[dict]:
    """
    Devuelve una lista de tareas filtradas por status.
    - status puede ser: 'todo', 'in-progress', 'done' o 'all'.
    - Si es 'all', devuelve todas las tareas.
    - Si es otro, devuelve solo las que tienen ese status.
    """
    pass


# ===== CAPA CLI: construcción del parser =====
def build_parser() -> argparse.ArgumentParser:
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
    # aquí asociamos el subcomando 'add' con su handler cmd_add
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
    # status opcional: todo | in-progress | done (o all si no se pasa)
    list_parser = subparsers.add_parser(
        "list",
        help="List all tasks, optionally filtered by status(todo, in-progress, done, all)",
    )
    list_parser.add_argument(
        "status",
        nargs="?",  # opcional
        choices=["todo", "in-progress", "done", "all"],
        default="all",
        help="Filter tasks by status (todo, in-progress, done, all)",
    )
    list_parser.set_defaults(func=cmd_list)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # args.func viene del set_defaults() del subcomando correspondiente
    args.func(args)


if __name__ == "__main__":
    main()
