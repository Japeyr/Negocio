import tkinter as tk
from ConexionSQLite import conectar_db
from tkinter import ttk, font, messagebox

def ver_movimiento_inventario(ventana_padre):
    calibri_font = font.Font(family="Calibri", size=14)

    ventana_padre.withdraw()
    ventana_movimiento_inventario = tk.Toplevel(ventana_padre)
    ventana_movimiento_inventario.title("Gestión de Inventario")
    ventana_movimiento_inventario.geometry("750x550")
    ventana_movimiento_inventario.configure(bg="#e6f7ff")

    # === LabelFrame general ===
    frame_form = tk.LabelFrame(ventana_movimiento_inventario, text="Ver Movimientos de Inventario", bg="#f0f8ff",
                               font=calibri_font, padx=10, pady=10)
    frame_form.pack(pady=15, padx=20, fill="both", expand=True)

    # --- Combobox selección de producto ---
    tk.Label(frame_form, text="Seleccione Producto:", bg="#f0f8ff", font=calibri_font).grid(row=0, column=0, padx=5,
                                                                                            pady=5, sticky="w")

    combo_producto = ttk.Combobox(frame_form, font=calibri_font, state="readonly", width=30)
    combo_producto.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # --- Cargar productos ---
    conn_prod = conectar_db()
    cursor_prod = conn_prod.cursor()
    cursor_prod.execute('''SELECT id_producto, descripcion || ' - ' || color || ' - ' || talle FROM Productos 
    ORDER BY descripcion ASC''')

    productos = cursor_prod.fetchall()
    conn_prod.close()

    mapa_productos = {desc: pid for pid, desc in productos}
    combo_producto["values"] = [desc for _, desc in productos]

    # === Tabla de movimientos dentro del mismo LabelFrame ===
    columnas = ("Fecha", "Tipo de Movimiento", "Cantidad", "Producto")
    tabla = ttk.Treeview(frame_form, columns=columnas, show="headings", height=12)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150, anchor="center")

    # Ubicamos la tabla con grid
    tabla.grid(row=1, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")

    # Scrollbar
    scrollbar = ttk.Scrollbar(frame_form, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=1, column=2, sticky="ns")

    # Ajuste de expansión del grid
    frame_form.grid_rowconfigure(1, weight=1)
    frame_form.grid_columnconfigure(1, weight=1)

    # === Función para cargar movimientos ===
    def cargar_movimientos():
        for item in tabla.get_children():
            tabla.delete(item)

        producto_sel = combo_producto.get()
        if not producto_sel:
            messagebox.showwarning("Atención", "Seleccione un producto")
            return

        id_producto = mapa_productos[producto_sel]

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.fecha, i.tipo_movimiento, i.cantidad, p.descripcion
            FROM Inventario i
            JOIN Productos p ON i.id_producto = p.id_producto
            WHERE i.id_producto = ?
            ORDER BY i.fecha DESC
        """, (id_producto,))
        rows = cursor.fetchall()
        conn.close()

        if rows:
            for r in rows:
                tabla.insert("", "end", values=r)
        else:
            messagebox.showinfo("Sin datos", "No hay movimientos para este producto.")

    # === Botones (afuera del recuadro) ===
    frame_botones = tk.LabelFrame(
        ventana_movimiento_inventario,
        text="Acciones",
        bg="#f0f8ff",
        font=calibri_font,
        padx=10,
        pady=10
    )
    frame_botones.pack(padx=20, pady=10, fill="x")

    tk.Button(frame_botones, text="Ver Movimientos", command=cargar_movimientos,
              bg="#add8e6", font=calibri_font, width=15).pack(side="left", padx=10)

    tk.Button(frame_botones, text="Salir",
              command=lambda: cerrar_ventana(ventana_movimiento_inventario, ventana_padre),
              bg="#add8e6", font=calibri_font, width=15).pack(side="left", padx=10)





def ajuste_manual_inventario(ventana_padre):
    calibri_font = font.Font(family="Calibri", size=14)

    ventana_padre.withdraw()
    ventana_ajuste = tk.Toplevel(ventana_padre)
    ventana_ajuste.title("Ajuste Manual de Inventario")
    ventana_ajuste.geometry("500x300")

    # === Formulario de ajuste ===
    frame_form = tk.LabelFrame(
        ventana_ajuste,
        text="Modificar Stock",
        padx=10, pady=10
    )
    frame_form.pack(pady=20, padx=20, fill="x")

    tk.Label(frame_form, text="Producto:", font=calibri_font).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    combo_producto = ttk.Combobox(frame_form, font=calibri_font, state="readonly", width=30)
    combo_producto.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Nuevo Stock:", font=calibri_font).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_stock = tk.Entry(frame_form, font=calibri_font, width=10)
    entry_stock.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # === Cargar productos ===
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT id_producto, descripcion || ' - ' || color || ' - ' || talle FROM Productos 
    ORDER BY descripcion ASC''')
    productos = cursor.fetchall()
    conn.close()

    mapa_productos = {desc: pid for pid, desc in productos}
    combo_producto["values"] = [desc for _, desc in productos]

    # === Función de ajuste ===
    def guardar_ajuste():
        producto_sel = combo_producto.get()
        nuevo_stock = entry_stock.get()

        if not producto_sel or not nuevo_stock.isdigit():
            messagebox.showwarning("Atención", "Seleccione un producto y un stock válido.")
            return

        id_producto = mapa_productos[producto_sel]

        try:
            conn_mov = conectar_db()
            cursor_mov = conn_mov.cursor()
            cursor_mov.execute("""
                UPDATE Productos
                SET stock_actual = ?
                WHERE id_producto = ?
            """, (int(nuevo_stock), id_producto))
            conn_mov.commit()
            conn_mov.close()
            messagebox.showinfo("Éxito", "Stock ajustado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ajustar el stock: {e}")

    # === Botones ===
    frame_botones = tk.LabelFrame(ventana_ajuste, text="Acciones", bg="#f0f8ff", font=calibri_font, padx=10, pady=10)
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Guardar", command=guardar_ajuste,
              bg="#add8e6", font=calibri_font, width=15).pack(side="left", padx=10)

    tk.Button(frame_botones, text="Salir",
              command=lambda: cerrar_ventana(ventana_ajuste, ventana_padre),
              bg="#add8e6", font=calibri_font, width=15).pack(side="left", padx=10)



def ver_stock_actual(ventana_emergente_inventario):
    # Fuente Calibri
    calibri_font = font.Font(family="Calibri", size=14)

    ventana_emergente_inventario.withdraw()
    ventana_ver_stocks_productos = tk.Toplevel(ventana_emergente_inventario)
    ventana_ver_stocks_productos.title("Stocks de Productos")
    ventana_ver_stocks_productos.geometry("1300x500")
    ventana_ver_stocks_productos.configure(bg="#e6f7ff")

    frame_formulario_stock_actual = tk.LabelFrame(ventana_ver_stocks_productos, text="Stock Actual", bg="#f0f8ff",
                                                  font=calibri_font, padx=10, pady=10)
    frame_formulario_stock_actual.pack(padx=20, pady=20, fill="x")

    label_listado_productos_stock = tk.Label(
        frame_formulario_stock_actual,
        text="Listado de Productos y Stock Actual",
        bg="#f0f8ff",
        font=calibri_font
    )
    label_listado_productos_stock.pack(pady=5)

    # --- Configuración del Treeview ---
    frame_treeview = tk.Frame(frame_formulario_stock_actual, bg="#f0f8ff")
    frame_treeview.pack(pady=10, padx=10, fill="both", expand=True)

    columnas = ("ID Producto", "Código", "Producto", "Precio Compra", "Precio Venta", "Stock", "Talle", "Color")
    tree = ttk.Treeview(frame_treeview, columns=columnas, show="headings")

    for col in columnas:
        tree.heading(col, text=col, anchor=tk.CENTER)
        tree.column(col, width=150, anchor=tk.CENTER)

    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_treeview, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    # --- Botón Salir ---

    button_cerrar_stock_productos = tk.Button(
        frame_formulario_stock_actual,
        text="Cerrar",
        command=lambda: cerrar_ventana(ventana_ver_stocks_productos, ventana_emergente_inventario),
        bg="#add8e6",
        font=calibri_font,
        width=15
    )
    button_cerrar_stock_productos.pack()

    # --- Cargar datos desde la base ---
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT p.id_producto, p.cod_producto, p.descripcion, 
               p.precio_compra, p.precio_venta, p.stock_actual, p.talle, p.color
        FROM Productos p
        ORDER BY p.descripcion
    """)
    rows = cursor.fetchall()
    conn.close()

    # Insertar los datos en el Treeview
    for r in rows:
        tree.insert("", "end", values=r)

    ventana_ver_stocks_productos.mainloop()


def cerrar_ventana(ventana_a_cerrar, ventana_a_mostrar=None):
    ventana_a_cerrar.destroy()
    if ventana_a_mostrar:
        ventana_a_mostrar.deiconify()
