# Task Tracker CLI

> Pequeña aplicación de línea de comandos para gestionar tareas, basada en el proyecto de roadmap.sh: [Task Tracker](https://roadmap.sh/projects/task-tracker).

Task Tracker CLI es una aplicación ligera en Python que te permite gestionar tus tareas directamente desde la terminal.  
Actualmente permite `add` y `update` tareas guardándolas en un archivo `tasks.json` en el directorio actual.  
El resto de comandos (`delete`, `mark-in-progress`, `mark-done`, `list`) están definidos a nivel de CLI, pero su lógica interna todavía está en desarrollo.

---

## ✨ Características (estado actual)

Implementado:

- ✅ **Añadir tarea**  
  - `task-cli add DESCRIPTION`  
  - Crea una nueva tarea con:
    - `id` incremental
    - `description`
    - `status = "todo"`
    - `createdAt` y `updatedAt` con fecha/hora actual
  - Muestra la tarea creada en una tabla formateada en la terminal.

- ✅ **Actualizar tarea**  
  - `task-cli update ID DESCRIPTION`  
  - Cambia la descripción de una tarea existente e actualiza `updatedAt`.
  - Si el `ID` no existe, muestra un mensaje de error.

Definido pero **aún no implementado en la capa de dominio**:

- ⏳ **Eliminar tarea**  
  - `task-cli delete ID`

- ⏳ **Marcar tarea como in-progress**  
  - `task-cli mark-in-progress ID`

- ⏳ **Marcar tarea como done**  
  - `task-cli mark-done ID`

- ⏳ **Listar tareas**  
  - `task-cli list [status]`  
  - `status` será una de: `todo`, `in-progress`, `done`, `all`

> ⚠️ Nota: De momento, los comandos que no son `add` o `update` solo muestran mensajes de prueba y **no modifican** el archivo `tasks.json`.

---

## 🧠 Modelo de datos

Las tareas se guardan en un archivo `tasks.json` en el directorio actual, con una estructura similar a:

```json
{
  "last_id": 3,
  "tasks": [
    {
      "id": 1,
      "description": "Buy groceries",
      "status": "todo",
      "createdAt": "28/11/2025 16:19:01",
      "updatedAt": "28/11/2025 16:19:01"
    },
    {
      "id": 2,
      "description": "Clean the house",
      "status": "todo",
      "createdAt": "28/11/2025 16:25:10",
      "updatedAt": "28/11/2025 16:25:10"
    }
  ]
}

## 📜 License
This project is licensed under the MIT License. You are free to use, modify, and distribute it.