from ConexionSQLite import conectar_db
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import font

def insertar_proveedor(nombre, contacto, direccion, widgets_proveedores_a_limpiar):
    if not nombre or not contacto or not direccion:
        messagebox.showerror("Error de Validación", "Por favor, completá todos los campos correctamente.")
        return False

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Proveedores (nombre, contacto, direccion) VALUES (?, ?, ?)",
                           (nombre, contacto, direccion))
            conn.commit()

        messagebox.showinfo("Aviso!", f"Proveedor Registrado con Éxito\n")

        for widget_proveedores in widgets_proveedores_a_limpiar:
            if isinstance(widget_proveedores, (tk.Entry, tk.Text)):
                widget_proveedores.delete(0, tk.END)

        if widgets_proveedores_a_limpiar and isinstance(widgets_proveedores_a_limpiar[0], tk.Entry):
            widgets_proveedores_a_limpiar[0].focus_set()

        return True

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el Proveedor: {e}")
        return False

def listar_proveedores():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Proveedores")
    proveedores = cursor.fetchall()
    conn.close()
    return proveedores

def formulario_edicion_proveedor(tree, ventana_lista):
    # Fuente Calibri
    calibri_font = font.Font(family="Calibri", size=14)

    item_seleccionado = tree.focus()
    if not item_seleccionado:
        return

    datos = tree.item(item_seleccionado, "values")
    ventana_lista.withdraw()

    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Proveedor")
    ventana_edicion.geometry("600x400")
    ventana_edicion.configure(bg="#e6f7ff")

    labels = ["id_proveedor", "Nombre", "Contacto", "Direccion"]
    entradas = []

    frame_form = tk.LabelFrame(ventana_edicion, text="Formulario Edición de Proveedores", bg="#f0f8ff",
                               font=calibri_font, padx=10,
                               pady=10)
    frame_form.pack(padx=20, pady=20, fill="x")

    for i, valor in enumerate(datos, start=1):
        label = tk.Label(frame_form, text=labels[i-1], bg="#f0f8ff",
                         font=("Calibri", 12), anchor="e", width=18)
        label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

        entry = tk.Entry(frame_form, font=("Calibri", 12), width=30)
        entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
        entry.insert(0, valor)
        entradas.append(entry)

    frame_botones = tk.LabelFrame(ventana_edicion, text="Acciones", bg="#f0f8ff", font=calibri_font, padx=10, pady=10)
    frame_botones.pack(pady=20)

    boton_guardar = tk.Button(
        frame_botones, text="Guardar Cambios", width="16",
        command=lambda: guardar_cambios_proveedor(entradas, ventana_edicion, ventana_lista, tree),
        bg="#add8e6", font=("Calibri", 12)
    )
    boton_guardar.grid(row=0, column=0, padx=10)

    boton_eliminar = tk.Button(frame_botones, text="Eliminar Proveedor", bg="#add8e6", font=("Calibri", 12), width="16",
                               command=lambda: eliminar_proveedor(entradas, ventana_edicion, ventana_lista, tree))
    boton_eliminar.grid(row=0, column=1, padx=10)

    boton_salir = tk.Button(
        frame_botones, text="Cancelar", width="16",
        command=lambda: cerrar_ventana(ventana_edicion, ventana_lista),
        bg="#add8e6", font=("Calibri", 12)
    )
    boton_salir.grid(row=0, column=2, padx=10)

def mostrar_lista_proveedores(ventana_padre):
    # Fuente Calibri
    calibri_font = font.Font(family="Calibri", size=14)

    ventana_padre.withdraw()
    ventana_lista = tk.Toplevel(ventana_padre)
    ventana_lista.title("Lista de Proveedores")
    ventana_lista.geometry("600x500")
    ventana_lista.configure(bg="#e6f7ff")

    label_listado_productos = tk.Label(ventana_lista, text="Listado de Proveedores", bg="#f0f8ff", font=calibri_font)
    label_listado_productos.pack(pady=5)

    # --- Configuración del Treeview ---
    frame_treeview = tk.Frame(ventana_lista, bg="#f0f8ff")
    frame_treeview.pack(pady=10, padx=10, fill="both", expand=True)

    columnas = ("id_proveedor", "Nombre", "Contacto", "Dirección")
    tree = ttk.Treeview(frame_treeview, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col, anchor=tk.CENTER)
        if col == "id_proveedor":
            tree.column(col, width=80, anchor=tk.CENTER)
        elif col == "Nombre":
            tree.column(col, width=100, anchor=tk.CENTER)
        elif col == "Contacto":
            tree.column(col, width=200, anchor=tk.CENTER)
        else:
            tree.column(col, width=100, anchor=tk.CENTER)

    tree.pack(side="left", fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", lambda event: formulario_edicion_proveedor(tree, ventana_lista))

    scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    frame_boton_salir = tk.Frame(ventana_lista, bg="#f0f8ff")
    frame_boton_salir.pack(pady=10)

    button_salir_listado_proveedores = tk.Button(frame_boton_salir, text="Salir",
                                               command=lambda: cerrar_ventana(ventana_lista,
                                                                              ventana_padre), bg="#add8e6",
                                               font=calibri_font, width=15)
    button_salir_listado_proveedores.pack()

    # --- Cargar datos ---
    refrescar_treeview(tree)

    ventana_lista.mainloop()

def refrescar_treeview(tree):
    # Borra datos actuales
    for item in tree.get_children():
        tree.delete(item)

    # Carga los datos actualizados
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT * from Proveedores")
            for fila in cursor.fetchall():
                tree.insert("", tk.END, values=fila)
        except conexion.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            conexion.close()

def cerrar_ventana(ventana_a_cerrar, ventana_a_mostrar=None):
    if messagebox.askokcancel("Cerrar", "¿Seguro que querés cerrar esta ventana?"):
        ventana_a_cerrar.destroy()
        if ventana_a_mostrar:
            ventana_a_mostrar.deiconify()

def guardar_cambios_proveedor(entradas, ventana_edicion, ventana_lista, tree):
    valores = [entry.get() for entry in entradas]
    id_proveedor = valores[0]
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Proveedores SET
                    Nombre = ?, Contacto = ?, Direccion = ?
                WHERE id_proveedor = ?
            """, (valores[1], valores[2], valores[3], id_proveedor))
            conn.commit()

        messagebox.showinfo("Éxito", "Proveedor actualizado correctamente.")

        ventana_edicion.destroy()
        ventana_lista.deiconify()
        refrescar_treeview(tree)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")

def eliminar_proveedor(entradas, ventana_edicion, ventana_lista, tree):
    valores = [entry.get() for entry in entradas]
    id_proveedor = valores[0]
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    DELETE FROM Proveedores WHERE id_proveedor = ?""", (id_proveedor,))
            conn.commit()

        messagebox.showinfo("Éxito", "Proveedot ELIMINADO correctamente.")

        ventana_edicion.destroy()
        ventana_lista.deiconify()
        refrescar_treeview(tree)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el proveedor: {e}")
