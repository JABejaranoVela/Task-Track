import sys

# print("Direccion: ", sys.argv)
# text = input("Escribe tu tarea: ")
# print("You entered:", text)


def pantalla_inicio():
    print("--------------------------")
    print(" Welcome to a Task Tracker ")
    print("--------------------------")
    print("Write in the terminal only the number of the action you want to do:")
    print("1. Add")
    print("2. Update")
    print("3. Delete")
    print("4. List all tasks")
    print("5. List all tasks that are done")
    print("6. List all tasks that are not done")
    print("7. List all tasks that are in progress")
    print("-----------------------------------------")
    selection = input("Write the number of the action: ")
    if selection == "1":
        add_Function()
    elif selection == "2":
        print


def add_Function():
    print("-----------------------------------------")
    task = input("Write the task: ")
    print("We are add the task: ", task)


def update_Function():
    print("-----------------------------------------")
    task = input("Selection the task: ")
    print("We are add the task: ", task)


def delete_Function():
    print("-----------------------------------------")
    task = input("Selection the task: ")
    print("We are add the task: ", task)


pantalla_inicio()
