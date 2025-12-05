"""
Manual tests for the Task Tracker project.

- No external libraries (no unittest, no pytest).
- Tests call the domain layer directly (add_task, update_task, etc.)
- They use a separate JSON file: tasks_test.json so they do NOT modify your real tasks.json
"""

import json
import os

import task_tracker_cli.cli as app


# Usaremos un archivo de tareas SOLO PARA TEST
TEST_TASKS_FILE = "tasks_test.json"


def use_test_file() -> None:
    """
    Hace que todas las funciones de dominio usen tasks_test.json
    en lugar de tasks.json, cambiando la constante TASKS_FILE del módulo.
    """
    app.TASKS_FILE = TEST_TASKS_FILE


def reset_test_data() -> None:
    """
    Sobrescribe el archivo de test con una estructura vacía estándar.
    """
    data = {"last_id": 0, "tasks": []}
    app.save_tasks(data)
    print(f"[INFO] Reset {TEST_TASKS_FILE} to an empty state.")


def show_test_json() -> None:
    """
    Muestra por pantalla el contenido crudo de tasks_test.json.
    """
    if not os.path.exists(TEST_TASKS_FILE):
        print(f"[WARN] {TEST_TASKS_FILE} does not exist yet.")
        return

    print(f"\n[DEBUG] Current contents of {TEST_TASKS_FILE}:\n")
    with open(TEST_TASKS_FILE, "r", encoding="utf-8") as f:
        print(f.read())
    print()  # línea en blanco


# =========================
# TESTS MANUALES INDIVIDUALES
# =========================


def test_add() -> None:
    """
    Test: add_task
    - Crea dos tareas.
    - Guarda en JSON.
    - Te pide que revises tasks_test.json.
    """
    print("\n===== TEST: add_task =====")
    reset_test_data()

    data = app.load_tasks()
    t1 = app.add_task(data, "Test task 1")
    t2 = app.add_task(data, "Test task 2")
    app.save_tasks(data)

    print("[INFO] Added tasks:")
    print("  -", t1)
    print("  -", t2)

    print("\n[EXPECTATION]")
    print(" - IDs consecutivos (1 y 2).")
    print(" - status='todo'.")
    print(" - createdAt y updatedAt con timestamps.")
    print(" - last_id = 2 en el JSON.")

    show_test_json()
    input("Check the JSON file, then press ENTER to continue...")


def test_update() -> None:
    """
    Test: update_task
    - Crea una tarea.
    - La actualiza.
    - Revisa que description y updatedAt cambien.
    """
    print("\n===== TEST: update_task =====")
    reset_test_data()

    data = app.load_tasks()
    original = app.add_task(data, "Original description")
    app.save_tasks(data)

    print("[INFO] Created task:")
    print(original)

    # Actualizamos la descripción
    data = app.load_tasks()
    updated = app.update_task(data, original["id"], "Updated description")
    app.save_tasks(data)

    print("\n[INFO] Updated task:")
    print(updated)

    print("\n[EXPECTATION]")
    print(" - Mismo id.")
    print(" - description = 'Updated description'.")
    print(" - updatedAt cambiado (mayor que createdAt).")

    show_test_json()
    input("Check the JSON file, then press ENTER to continue...")


def test_delete() -> None:
    """
    Test: delete_task
    - Crea dos tareas.
    - Borra la primera.
    - Comprueba que solo queda la segunda en el JSON.
    """
    print("\n===== TEST: delete_task =====")
    reset_test_data()

    data = app.load_tasks()
    t1 = app.add_task(data, "Task to delete")
    t2 = app.add_task(data, "Task to keep")
    app.save_tasks(data)

    print("[INFO] Created tasks:")
    print("  -", t1)
    print("  -", t2)

    # Borramos la primera
    data = app.load_tasks()
    deleted = app.delete_task(data, t1["id"])
    app.save_tasks(data)

    print("\n[INFO] Deleted task:")
    print(deleted)

    print("\n[EXPECTATION]")
    print(" - En tasks_test.json solo debería quedar la tarea 'Task to keep'.")
    print(" - last_id conserva el valor 2 (no se renumeran IDs).")

    show_test_json()
    input("Check the JSON file, then press ENTER to continue...")


def test_set_status() -> None:
    """
    Test: set_task_status
    - Crea una tarea.
    - La marca como in-progress.
    - Luego la marca como done.
    """
    print("\n===== TEST: set_task_status (in-progress / done) =====")
    reset_test_data()

    data = app.load_tasks()
    task = app.add_task(data, "Task to change status")
    app.save_tasks(data)

    print("[INFO] Created task:")
    print(task)

    # in-progress
    data = app.load_tasks()
    in_progress = app.set_task_status(data, task["id"], "in-progress")
    app.save_tasks(data)

    print("\n[INFO] After set_task_status(..., 'in-progress'):")
    print(in_progress)

    # done
    data = app.load_tasks()
    done = app.set_task_status(data, task["id"], "done")
    app.save_tasks(data)

    print("\n[INFO] After set_task_status(..., 'done'):")
    print(done)

    print("\n[EXPECTATION]")
    print(" - status cambia 'todo' -> 'in-progress' -> 'done'.")
    print(" - updatedAt se actualiza cada vez.")

    show_test_json()
    input("Check the JSON file, then press ENTER to continue...")


def test_list_filters() -> None:
    """
    Test: list_tasks_by_status
    - Crea varias tareas con distintos estados.
    - Llama a list_tasks_by_status con all, todo, in-progress, done.
    """
    print("\n===== TEST: list_tasks_by_status =====")
    reset_test_data()

    data = app.load_tasks()
    t1 = app.add_task(data, "Task A (todo)")
    t2 = app.add_task(data, "Task B (in-progress)")
    t3 = app.add_task(data, "Task C (done)")

    # Cambiamos estados de B y C
    app.set_task_status(data, t2["id"], "in-progress")
    app.set_task_status(data, t3["id"], "done")
    app.save_tasks(data)

    print("[INFO] Created tasks with different statuses.")
    show_test_json()

    data = app.load_tasks()
    all_tasks = app.list_tasks_by_status(data, "all")
    todos = app.list_tasks_by_status(data, "todo")
    in_progress = app.list_tasks_by_status(data, "in-progress")
    done = app.list_tasks_by_status(data, "done")

    print(
        "\n[RESULT] list_tasks_by_status(..., 'all') -> IDs:",
        [t["id"] for t in all_tasks],
    )
    print(
        "         list_tasks_by_status(..., 'todo') -> IDs:", [t["id"] for t in todos]
    )
    print(
        "         list_tasks_by_status(..., 'in-progress') -> IDs:",
        [t["id"] for t in in_progress],
    )
    print("         list_tasks_by_status(..., 'done') -> IDs:", [t["id"] for t in done])

    print("\n[EXPECTATION]")
    print(f" - 'all' debe contener los 3 IDs: {[t1['id'], t2['id'], t3['id']]}")
    print(f" - 'todo' debería contener solo el ID de '{t1['description']}'.")
    print(f" - 'in-progress' debería contener solo el ID de '{t2['description']}'.")
    print(f" - 'done' debería contener solo el ID de '{t3['description']}'.")

    input("Visually verify the IDs printed above, then press ENTER to continue...")


# =========================
# MENÚ PRINCIPAL DE TESTS
# =========================


def main() -> None:
    use_test_file()

    while True:
        print("\n==============================")
        print(" MANUAL TESTS - TASK TRACKER ")
        print("==============================")
        print("Using JSON file:", TEST_TASKS_FILE)
        print()
        print("1) Test add_task")
        print("2) Test update_task")
        print("3) Test delete_task")
        print("4) Test set_task_status (in-progress / done)")
        print("5) Test list_tasks_by_status (all / todo / in-progress / done)")
        print("6) Show current test JSON")
        print("q) Quit")
        choice = input("\nSelect an option: ").strip().lower()

        if choice == "1":
            test_add()
        elif choice == "2":
            test_update()
        elif choice == "3":
            test_delete()
        elif choice == "4":
            test_set_status()
        elif choice == "5":
            test_list_filters()
        elif choice == "6":
            show_test_json()
            input("Press ENTER to return to menu...")
        elif choice == "q":
            print("Bye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
