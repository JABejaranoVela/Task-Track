Taskly: CLI TODO App

He usado una arquitectura sencilla en capas: una capa de interfaz de línea de comandos (CLI) basada en argparse con un handler por comando (cmd_add, cmd_update, etc.), y una capa de dominio formada por funciones puras que gestionan las tareas (add_task, update_task, list_tasks, etc.). La capa CLI se encarga solo de interpretar los argumentos y mostrar mensajes al usuario, mientras que la lógica de negocio y el acceso al archivo JSON están encapsulados en las funciones de dominio. Esto mantiene el código más limpio, testeable y fácil de extender, sin añadir complejidad innecesaria para una aplicación pequeña.

📖 Description
Taskly is a lightweight command-line interface (CLI) application for efficient task management.
Built as the final project for CS50P, it allows you to add, update, delete, list, and track tasks directly from your terminal.

✨ Features
Add a Task → Create tasks with descriptions. Each task gets a unique ID and a default todo status.
Update a Task → Modify the description or status of a task.
Mark as In-Progress → Quickly change a task’s status to in-progress.
Mark as Done → Quickly change a task’s status to done.
Delete a Task → Remove tasks by their ID.
List Tasks → Display all tasks or filter them by:
status: todo, in-progress, done, or all
date: filter by creation date with operators <, >, =
🗂 Project Structure
taskly.py → Core CLI implementation

main() → Entry point, parses CLI arguments and runs commands.
load_database(path) → Loads tasks from a JSON file.
save_database(database, path) → Saves tasks to JSON.
add_task(database, description) → Adds a new task.
update_task(database, id, description?, status?) → Updates description or status.
mark_in_progress_task(database, id) → Marks a task as in-progress.
mark_done_task(database, id) → Marks a task as done.
delete_task(database, id) → Deletes a task.
list_task(database, status?, date?) → Lists tasks with optional filters.
test_taskly.py → Unit tests for all features using pytest.

pyproject.toml → Project metadata, dependencies, and packaging config.

⚡ Installation
You can install Taskly directly from GitHub:

pip install git+https://github.com/brkahmed/taskly.git
🚀 Usage
$ taskly add [-h] description

$ taskly update [-h] [-d description] [-s {done,in-progress,todo}] id

$ taskly mark-done [-h] id

$ taskly mark-in-progress [-h] id

$ taskly delete [-h] id

$ taskly list [-h] [-s {done,in-progress,todo,all}] [-d DATE]