# Oderlin Sanchez Santana, Matricula: 2023-1339
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Nombre de la base de datos
db_name = "task_manager.db"

# Funciones para gestionar las tareas
def register_task_gui(title, description):
    """Registra una tarea desde la interfaz gráfica."""
    if not title.strip():
        messagebox.showerror("Error", "El título de la tarea no puede estar vacío.")
        return
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
    connection.commit()
    connection.close()
    messagebox.showinfo("Éxito", "¡Tarea registrada con éxito!")
    list_tasks()

def list_tasks():
    """Actualiza la lista de tareas en la interfaz."""
    for row in task_tree.get_children():
        task_tree.delete(row)
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, description, status, created_at FROM tasks WHERE status = 'Pending'")
    tasks = cursor.fetchall()
    connection.close()
    for task in tasks:
        task_tree.insert("", "end", values=task)

def complete_task():
    """Marca una tarea seleccionada como completada."""
    selected_item = task_tree.selection()
    if not selected_item:
        messagebox.showwarning("Advertencia", "Por favor selecciona una tarea para completar.")
        return
    task_id = task_tree.item(selected_item, "values")[0]
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    connection.commit()
    connection.close()
    messagebox.showinfo("Éxito", "¡Tarea marcada como completada!")
    list_tasks()

def filter_tasks(status):
    """Filtra las tareas por su estado."""
    for row in task_tree.get_children():
        task_tree.delete(row)
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    query = "SELECT id, title, description, status, created_at FROM tasks WHERE status = ?"
    cursor.execute(query, (status,))
    tasks = cursor.fetchall()
    connection.close()
    for task in tasks:
        task_tree.insert("", "end", values=task)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Task Manager Lite")
root.geometry("600x400")

# Campo para el título de la tarea
title_label = tk.Label(root, text="Título de la tarea:")
title_label.grid(row=0, column=0, padx=10, pady=10)
title_entry = tk.Entry(root, width=40)
title_entry.grid(row=0, column=1, padx=10, pady=10)

# Campo para la descripción de la tarea
desc_label = tk.Label(root, text="Descripción de la tarea:")
desc_label.grid(row=1, column=0, padx=10, pady=10)
desc_entry = tk.Entry(root, width=40)
desc_entry.grid(row=1, column=1, padx=10, pady=10)

# Botón para agregar tareas
add_task_button = tk.Button(root, text="Agregar Tarea", command=lambda: register_task_gui(title_entry.get(), desc_entry.get()))
add_task_button.grid(row=2, column=1, pady=10)

# Tabla para mostrar las tareas
task_tree = ttk.Treeview(root, columns=("ID", "Title", "Description", "Status", "Created At"), show="headings")
task_tree.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Configuración de las columnas de la tabla
task_tree.heading("ID", text="ID")
task_tree.heading("Title", text="Título")
task_tree.heading("Description", text="Descripción")
task_tree.heading("Status", text="Estado")
task_tree.heading("Created At", text="Creado el")

# Botones adicionales
complete_task_button = tk.Button(root, text="Completar Tarea", command=complete_task)
complete_task_button.grid(row=4, column=0, padx=10, pady=10)

filter_pending_button = tk.Button(root, text="Mostrar Pendientes", command=lambda: filter_tasks("Pending"))
filter_pending_button.grid(row=4, column=1, padx=10, pady=10)

filter_completed_button = tk.Button(root, text="Mostrar Completadas", command=lambda: filter_tasks("Completed"))
filter_completed_button.grid(row=4, column=2, padx=10, pady=10)

# Cargar la lista de tareas al iniciar
list_tasks()

# Iniciar la aplicación
root.mainloop()
