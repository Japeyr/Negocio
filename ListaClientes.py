from ConexionSQLite import conectar_db
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from tkinter import font

def insertar_cliente(nombre, contacto, widgets_clientes_a_limpiar):
    if not nombre or not contacto:
        messagebox.showerror("Error de Validación", "Por favor, completá todos los campos correctamente.")
        return False

    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
        messagebox.showinfo("Datos del Cliente",
                            f"Nombre: {nombre}\nContacto: {contacto}\n")
        cursor.execute("INSERT INTO Clientes (nombre, contacto) VALUES (?, ?)", (nombre, contacto))

        conn.commit()
        messagebox.showinfo("Éxito!", f"Cliente Registrado con Éxito\n")

        # Limpiar Entry y Spinbox
        for widget_clientes in widgets_clientes_a_limpiar:
            if isinstance(widget_clientes, (tk.Entry, tk.Text)):
                widget_clientes.delete(0, tk.END)

        if widgets_clientes_a_limpiar and isinstance(widgets_clientes_a_limpiar[0], tk.Entry):
            widgets_clientes_a_limpiar[0].focus_set()
        return True
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el cliente: {e}")
        return False

def listar_clientes(ventana_clientes):
    # Fuente Calibri
    calibri_font = font.Font(family="Calibri", size=14)

    ventana_clientes.withdraw()
    ventana_emergente_lista_clientes = tk.Toplevel(ventana_clientes)
    ventana_emergente_lista_clientes.title("Lista de Clientes")
    ventana_emergente_lista_clientes.geometry("600x500")
    ventana_emergente_lista_clientes.configure(bg="#e6f7ff")

    # Frame para formulario
    frame_formulario_lista_clientes = tk.LabelFrame(ventana_emergente_lista_clientes, text="Listado de Clientes",
                                                 bg="#f0f8ff", font=calibri_font, padx=10, pady=10)
    frame_formulario_lista_clientes.pack(padx=20, pady=20, fill="x")

    label_listado_clientes = tk.Label(frame_formulario_lista_clientes, text="Listado de Clientes", bg="#f0f8ff",
                                      font=calibri_font)
    label_listado_clientes.pack(pady=5)

    # --- Configuración del Treeview ---
    frame_treeview = tk.Frame(frame_formulario_lista_clientes, bg="#f0f8ff")
    frame_treeview.pack(pady=10, padx=10, fill="both", expand=True)

    # Definir las columnas
    columnas = ("ID Cliente", "Nombre", "Contacto")
    tree = ttk.Treeview(frame_treeview, columns=columnas, show="headings")

    # Configurar los encabezados de las columnas
    for col in columnas:
        tree.heading(col, text=col, anchor=tk.CENTER)
        # Puedes ajustar el ancho de las columnas aquí si lo necesitas
        if col == "ID Cliente":
            tree.column(col, width=10, anchor=tk.CENTER)  # Ancho
        elif col == "Nombre":
            tree.column(col, width=50, anchor=tk.CENTER)
        else:
            tree.column(col, width=50, anchor=tk.CENTER)

    tree.pack(side="left", fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", lambda event: mostrar_formulario_edicion(tree, ventana_emergente_lista_clientes))

    # Añadir un scrollbar
    scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    frame_boton_salir = tk.Frame(ventana_emergente_lista_clientes, bg="#f0f8ff")
    frame_boton_salir.pack(pady=10)

    button_salir_listado_clientes = tk.Button(frame_boton_salir, text="Salir",
                                              command=lambda: cerrar_ventana(ventana_emergente_lista_clientes,
                                                                             ventana_clientes), bg="#add8e6",
                                              font=calibri_font, width=15)
    button_salir_listado_clientes.pack()

    # --- Cargar datos ---
    refrescar_treeview(tree)

    ventana_emergente_lista_clientes.mainloop()

def mostrar_formulario_edicion(tree, ventana_lista):
    # Fuente Calibri
    calibri_font = font.Font(family="Calibri", size=14)

    item_seleccionado = tree.focus()
    if not item_seleccionado:
        return

    datos = tree.item(item_seleccionado, "values")
    ventana_lista.withdraw()

    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Cliente")
    ventana_edicion.geometry("540x360")
    ventana_edicion.configure(bg="#e6f7ff")

    labels = ["ID Cliente", "Nombre", "Contacto"]
    entradas = []

    # Frame para formulario
    frame_formulario_edicion_clientes = tk.LabelFrame(ventana_edicion, text="Proveedor",
                                                 bg="#f0f8ff", font=calibri_font, padx=10, pady=10)
    frame_formulario_edicion_clientes.pack(padx=20, pady=20, fill="x")

    label_edicion_cliente = tk.Label(
        frame_formulario_edicion_clientes, text="Formulario de Edición de Cliente",
        bg="#f0f8ff", font=("Calibri", 14, "bold")
    )
    label_edicion_cliente.grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky="we")

    for i, valor in enumerate(datos, start=1):
        label = tk.Label(frame_formulario_edicion_clientes, text=labels[i-1], bg="#f0f8ff",
                         font=("Calibri", 12), anchor="e", width=18)
        label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

        entry = tk.Entry(frame_formulario_edicion_clientes, font=("Calibri", 12), width=30)
        entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
        entry.insert(0, valor)
        entradas.append(entry)

    frame_botones = tk.LabelFrame(ventana_edicion, text="Acciones", bg="#f0f8ff", font=calibri_font, padx=10, pady=10)
    frame_botones.pack(pady=20)

    boton_guardar = tk.Button(
        frame_botones, text="Guardar Cambios", width="16",
        command=lambda: guardar_cambios_cliente(entradas, ventana_edicion, ventana_lista, tree),
        bg="#add8e6", font=("Calibri", 12)
    )
    boton_guardar.grid(row=0, column=0, padx=10)

    boton_eliminar = tk.Button(frame_botones, text="Eliminar Cliente", bg="#add8e6", font=("Calibri", 12), width="16",
                               command=lambda: eliminar_cliente(entradas, ventana_edicion, ventana_lista, tree))
    boton_eliminar.grid(row=0, column=1, padx=10)

    boton_salir = tk.Button(
        frame_botones, text="Cancelar", width="16",
        command=lambda: cerrar_ventana(ventana_edicion, ventana_lista),
        bg="#add8e6", font=("Calibri", 12)
    )
    boton_salir.grid(row=0, column=2, padx=10)

def guardar_cambios_cliente(entradas, ventana_edicion, ventana_lista, tree):
    valores = [entry.get() for entry in entradas]
    id_cliente = valores[0]
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Clientes SET
                    nombre = ?, contacto = ?
                WHERE id_cliente = ?
            """, (valores[1], valores[2], id_cliente))
            conn.commit()

        messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")

        ventana_edicion.destroy()
        ventana_lista.deiconify()
        refrescar_treeview(tree)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")

def refrescar_treeview(tree):
    # Borra datos actuales
    for item in tree.get_children():
        tree.delete(item)

    # Carga los datos actualizados
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT * from Clientes")
            for fila in cursor.fetchall():
                tree.insert("", tk.END, values=fila)
        except conexion.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            conexion.close()

def actualizar_stock():
    pass

def eliminar_cliente(entradas, ventana_edicion, ventana_lista, tree):
    valores = [entry.get() for entry in entradas]
    id_cliente = valores[0]
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    DELETE FROM Clientes WHERE id_cliente = ?""", (id_cliente,))
            conn.commit()

        messagebox.showinfo("Éxito", "Cliente ELIMINADO correctamente.")

        ventana_edicion.destroy()
        ventana_lista.deiconify()
        refrescar_treeview(tree)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")

def cerrar_ventana(ventana_a_cerrar, ventana_a_mostrar=None):
    if messagebox.askokcancel("Cerrar", "¿Seguro que querés cerrar esta ventana?"):
        ventana_a_cerrar.destroy()
        if ventana_a_mostrar:
            ventana_a_mostrar.deiconify()

def lista_clientes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes
