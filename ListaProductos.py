from tkinter import messagebox
from ConexionSQLite import conectar_db
import tkinter as tk
from tkinter import ttk
from tkinter import font

def insertar_producto(codigo, descripcion, precio_compra, precio_venta, stock_actual, talle, color, proveedor,
                      widgets_a_limpiar, selected_proveedor_id,
                      combobox_talle, combobox_color, combobox_proveedor):
    # Validación de campos
    if (
        not codigo or not descripcion or not precio_compra or not precio_venta or not stock_actual
        or talle == "Seleccionar"
        or color == "Seleccionar"
        or proveedor in ("", "Seleccionar Proveedor")
    ):
        messagebox.showerror("Error de Validación", "Por favor, completá todos los campos correctamente.")
        return False

    try:
        proveedor = int(proveedor)
        with conectar_db() as conn:
            cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Productos (
                cod_producto, descripcion, precio_compra, precio_venta,
                stock_actual, talle, color, proveedor_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo, descripcion, precio_compra, precio_venta, stock_actual, talle, color, proveedor))

        conn.commit()

        messagebox.showinfo("Éxito", "Producto agregado correctamente.")

        # Limpiar Entry y Spinbox
        for widget in widgets_a_limpiar:
            if isinstance(widget, (tk.Entry, tk.Text)):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Spinbox):
                widget.delete(0, tk.END)
                widget.insert(0, '0')

        # Limpiar comboboxes de forma directa
        combobox_talle.set("Seleccionar")
        combobox_color.set("Seleccionar")
        combobox_proveedor.set("Seleccionar Proveedor")

        selected_proveedor_id.set("")

        if widgets_a_limpiar and isinstance(widgets_a_limpiar[0], tk.Entry):
            widgets_a_limpiar[0].focus_set()

        return True

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el producto: {e}")
        return False

    finally:
        if 'conn' in locals():
            conn.close()

def ver_productos(ventana_productos):
    # Fuente Calibri
    calibri_font = font.Font(family="Calibri", size=14)

    ventana_productos.withdraw()
    ventana_emergente_lista_productos = tk.Toplevel(ventana_productos)
    ventana_emergente_lista_productos.title("Lista de Productos")
    ventana_emergente_lista_productos.geometry("1200x500")
    ventana_emergente_lista_productos.configure(bg="#e6f7ff")

    frame_formulario_productos = tk.LabelFrame(ventana_emergente_lista_productos, text="Listado de Productos",
                                               bg="#f0f8ff", font=calibri_font, padx=10, pady=10)
    frame_formulario_productos.pack(padx=20, pady=20, fill="x")

    # --- Configuración del Treeview ---
    frame_treeview = tk.Frame(frame_formulario_productos, bg="#f0f8ff")
    frame_treeview.pack(pady=10, padx=10, fill="both", expand=True)

    columnas = ("ID Producto", "Código", "Descripción", "Precio Compra", "Precio Venta", "Stock", "Talle", "Color",
                "ID Proveedor")
    tree = ttk.Treeview(frame_treeview, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col, anchor=tk.CENTER)
        if col == "Descripción":
            tree.column(col, width=200, anchor=tk.W)
        elif col == "Código":
            tree.column(col, width=100, anchor=tk.CENTER)
        elif col == "ID Producto" or col == "ID Proveedor":
            tree.column(col, width=80, anchor=tk.CENTER)
        else:
            tree.column(col, width=100, anchor=tk.CENTER)

    tree.pack(side="left", fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", lambda event: mostrar_formulario_edicion(tree, ventana_emergente_lista_productos))

    scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    frame_boton_salir = tk.Frame(ventana_emergente_lista_productos, bg="#f0f8ff")
    frame_boton_salir.pack(pady=10)

    button_salir_listado_productos = tk.Button(frame_boton_salir, text="Salir",
                                               command=lambda: cerrar_ventana(ventana_emergente_lista_productos,
                                                                              ventana_productos), bg="#add8e6",
                                               font=calibri_font, width=15)
    button_salir_listado_productos.pack()

    # --- Cargar datos ---
    refrescar_treeview(tree)

    ventana_emergente_lista_productos.mainloop()

def cerrar_ventana(ventana_a_cerrar, ventana_a_mostrar=None):
    if messagebox.askokcancel("Cerrar", "¿Seguro que querés cerrar esta ventana?"):
        ventana_a_cerrar.destroy()
        if ventana_a_mostrar:
            ventana_a_mostrar.deiconify()

def mostrar_formulario_edicion(tree, ventana_lista):
    # Fuente Calibri
    calibri_font = font.Font(family="Calibri", size=14)

    item_seleccionado = tree.focus()
    if not item_seleccionado:
        return

    datos = tree.item(item_seleccionado, "values")
    ventana_lista.withdraw()

    ventana_edicion = tk.Toplevel()
    ventana_edicion.title("Editar Producto")
    ventana_edicion.geometry("550x600")
    ventana_edicion.configure(bg="#e6f7ff")

    labels = [
        "ID Producto", "Código", "Descripción", "Precio Compra", "Precio Venta",
        "Stock", "Talle", "Color", "ID Proveedor"
    ]
    entradas = []

    frame_form = tk.LabelFrame(ventana_edicion, text="Edición de Producto", bg="#f0f8ff", font=calibri_font, padx=10,
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
    frame_botones.pack(padx=20, pady=20, fill="x")

    boton_guardar = tk.Button(
        frame_botones, text="Guardar Cambios", width="16",
        command=lambda: guardar_cambios_producto(entradas, ventana_edicion, ventana_lista, tree),
        bg="#add8e6", font=("Calibri", 12)
    )
    boton_guardar.grid(row=0, column=0, padx=10)

    boton_eliminar = tk.Button(frame_botones, text="Eliminar Producto", bg="#add8e6", font=("Calibri", 12), width="16",
                               command=lambda: eliminar_producto(entradas, ventana_edicion, ventana_lista, tree))
    boton_eliminar.grid(row=0, column=1, padx=10)

    boton_salir = tk.Button(
        frame_botones, text="Cancelar", width="16",
        command=lambda: cerrar_ventana(ventana_edicion, ventana_lista),
        bg="#add8e6", font=("Calibri", 12)
    )
    boton_salir.grid(row=0, column=2, padx=10)

def guardar_cambios_producto(entradas, ventana_edicion, ventana_lista, tree):
    valores = [entry.get() for entry in entradas]
    id_producto = valores[0]
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Productos SET
                    cod_producto = ?, descripcion = ?, precio_compra = ?, precio_venta = ?,
                    stock_actual = ?, talle = ?, color = ?, proveedor_id = ?
                WHERE id_producto = ?
            """, (valores[1], valores[2], valores[3], valores[4], valores[5],
                  valores[6], valores[7], valores[8], id_producto))
            conn.commit()

        messagebox.showinfo("Éxito", "Producto actualizado correctamente.")

        ventana_edicion.destroy()
        ventana_lista.deiconify()
        refrescar_treeview(tree)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el producto: {e}")

def eliminar_producto(entradas, ventana_edicion, ventana_lista, tree):
    valores = [entry.get() for entry in entradas]
    id_producto = valores[0]
    try:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM Productos WHERE id_producto = ?""", (id_producto,))
            conn.commit()

        messagebox.showinfo("Éxito", "Producto ELIMINADO correctamente.")

        ventana_edicion.destroy()
        ventana_lista.deiconify()
        refrescar_treeview(tree)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el producto: {e}")

def refrescar_treeview(tree):
    # Borra datos actuales
    for item in tree.get_children():
        tree.delete(item)

    # Carga los datos actualizados
    conexion = conectar_db()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT * from Productos")
            for fila in cursor.fetchall():
                tree.insert("", tk.END, values=fila)
        except conexion.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
        finally:
            conexion.close()

def listar_productos():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Productos")
    productos = cursor.fetchall()
    conn.close()
    return productos
