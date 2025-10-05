import tkinter as tk
from tkinter import ttk, font, messagebox
from tkcalendar import DateEntry
import sqlite3
from ListaClientes import lista_clientes
from ListaProductos import listar_productos

DB_PATH = "Negocio.db"

def registrar_venta(ventana_emergente_ventas):
    calibri_font = font.Font(family="Calibri", size=14)

    ventana_emergente_ventas.withdraw()
    ventana_form = tk.Toplevel(ventana_emergente_ventas)
    ventana_form.title("Formulario de Venta")
    ventana_form.geometry("800x740")
    ventana_form.configure(bg="#e6f7ff")

    frame_formulario = tk.LabelFrame(ventana_form, text="Registro de Nueva Ventaa", padx=10, pady=10, bg="#f0f8ff",
                                     font=("Calibri", 18, "bold"))
    frame_formulario.pack(pady=20, padx=20, fill="x")

    # ===== Fecha =====
    label_fecha = tk.Label(frame_formulario, text="Fecha", bg="#f0f8ff", font=calibri_font)
    label_fecha.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_fecha = DateEntry(frame_formulario, date_pattern='dd/mm/yyyy', width=12,
                            background="darkblue", foreground="white", borderwidth=2, year=2025, font=calibri_font)
    entry_fecha.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    # ===== Cliente =====
    label_cliente = tk.Label(frame_formulario, text="Cliente:", bg="#f0f8ff", font=calibri_font)
    label_cliente.grid(row=2, column=0, sticky="e", padx=5, pady=5)

    clientes_db = lista_clientes()
    clientes_map = {p[1]: p[0] for p in clientes_db}  # nombre: id
    opciones_cliente = ["Seleccionar Cliente"] + [p[1] for p in clientes_db]

    combobox_clientes = ttk.Combobox(frame_formulario, values=opciones_cliente, font=calibri_font, state="readonly")
    combobox_clientes.grid(row=2, column=1, sticky="w", padx=5, pady=5)
    combobox_clientes.set("Seleccionar Cliente")

    def seleccionar_cliente(event):
        if combobox_clientes.get() != "Seleccionar Cliente":
            combobox_clientes.config(state="disabled")

    combobox_clientes.bind("<<ComboboxSelected>>", seleccionar_cliente)

    # ===== Sección Productos =====
    label_producto = tk.Label(frame_formulario, text="Producto:", bg="#f0f8ff", font=calibri_font)
    label_producto.grid(row=3, column=0, sticky="e", padx=5, pady=5)

    productos_db = listar_productos()
    productos_map = {f"{p[2]} - {p[7]} - {p[6]}": (p[0], p[5], p[4]) for p in productos_db}  # descripcion: id
    opciones_producto = ["Seleccionar Producto"] + [f"{p[2]} - {p[7]} - {p[6]}" for p in productos_db]

    combobox_producto = ttk.Combobox(frame_formulario, values=opciones_producto,
                                     font=calibri_font, state="readonly", width=25)
    combobox_producto.grid(row=3, column=1, sticky="w", padx=5, pady=5)
    combobox_producto.set("Seleccionar Producto")

    label_cantidad = tk.Label(frame_formulario, text="Cantidad:", bg="#f0f8ff", font=calibri_font)
    label_cantidad.grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_cantidad = tk.Entry(frame_formulario, font=calibri_font, width=8)
    entry_cantidad.grid(row=4, column=1, sticky="w", padx=5, pady=5)

    label_precio = tk.Label(frame_formulario, text="Precio Unitario:", bg="#f0f8ff", font=calibri_font)
    label_precio.grid(row=5, column=0, sticky="e", padx=5, pady=5)
    entry_precio = tk.Entry(frame_formulario, font=calibri_font, width=10)
    entry_precio.grid(row=5, column=1, sticky="w", padx=5, pady=5)

    # ===== Treeview (Carrito) =====
    frame_tree = tk.Frame(frame_formulario, bg="#f0f8ff")
    frame_tree.grid(row=6, column=0, columnspan=4, pady=10, sticky="ew")

    columnas = ("producto", "cantidad", "precio", "subtotal")
    tree = ttk.Treeview(frame_tree, columns=columnas, show="headings", height=8)
    tree.heading("producto", text="Producto")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("precio", text="Precio Unitario")
    tree.heading("subtotal", text="Subtotal")
    tree.column("producto", width=260)
    tree.column("cantidad", width=110)
    tree.column("precio", width=170)
    tree.column("subtotal", width=170)
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # ===== Total =====
    label_total = tk.Label(ventana_form, text="Total: 0.00", bg="#e6f7ff", font=("Calibri", 16, "bold"))
    label_total.pack(pady=10)

    # ===== Funciones =====
    def agregar_producto():
        producto = combobox_producto.get()
        cantidad = entry_cantidad.get()
        precio = entry_precio.get()

        if producto == "Seleccionar Producto" or not cantidad or not precio:
            messagebox.showwarning("Atención", "Debe completar producto, cantidad y precio")
            return

        try:
            cantidad = int(cantidad)
            precio = float(precio)
            subtotal = cantidad * precio
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser número entero y precio un número válido")
            return

        # === AÑADIR VERIFICACIÓN DE STOCK AQUÍ ===
        try:
            # Obtiene (id_producto, stock_actual, precio_venta) del producto seleccionado
            producto_data = productos_map[producto]
            stock_actual = producto_data[1]

            # Sumar la cantidad que ya está en el carrito para este producto
            cantidad_en_carrito = 0
            for item in tree.get_children():
                prod_en_carrito, cant_en_carrito, _, _ = tree.item(item, "values")
                if prod_en_carrito == producto:
                    cantidad_en_carrito += int(cant_en_carrito)

            stock_despues_de_agregar = stock_actual - (cantidad_en_carrito + cantidad)

            if stock_despues_de_agregar < 0:
                messagebox.showwarning(
                    "Stock Insuficiente",
                    f"Solo quedan {stock_actual} unidades de '{producto}'. "
                    f"Ya tienes {cantidad_en_carrito} en el carrito."
                )
                combobox_producto.set("Seleccionar Producto")
                entry_cantidad.delete(0, tk.END)
                entry_precio.delete(0, tk.END)
                return

        except KeyError:
            messagebox.showerror("Error", "Error al obtener datos del producto seleccionado.")
            return
        # ========================================

        tree.insert("", "end", values=(producto, cantidad, f"{precio: .2f}", f"{subtotal: .2f}"))

        actualizar_total()

        # Limpiar inputs
        combobox_producto.set("Seleccionar Producto")
        entry_cantidad.delete(0, tk.END)
        entry_precio.delete(0, tk.END)

    def actualizar_total():
        total = 0
        for item in tree.get_children():
            subtotal = float(tree.item(item, "values")[3])
            total += subtotal
        label_total.config(text=f"Total: {total: .2f}")

    def registrar_en_bd():
        fecha = entry_fecha.get_date().strftime("%Y-%m-%d")
        cliente = combobox_clientes.get()

        if cliente == "Seleccionar Cliente" or not tree.get_children():
            messagebox.showwarning("Atención", "Debe seleccionar un Cliente y agregar al menos un producto")
            return

        cliente_id = clientes_map[cliente]
        total_obtenido = float(label_total.cget("text").replace("Total: ", ""))

        try:
            conn = sqlite3.connect("Negocio.db")
            cursor = conn.cursor()

            # Insertar en Ventas
            cursor.execute("""
                INSERT INTO Ventas (fecha, cliente_id, total_obtenido)
                VALUES (?, ?, ?)
            """, (fecha, cliente_id, total_obtenido))
            id_venta = cursor.lastrowid

            # Insertar en Detalle_Ventas
            for item in tree.get_children():
                producto, cantidad, precio, subtotal = tree.item(item, "values")
                producto_data = productos_map[producto]
                producto_id = producto_data[0]
                cursor.execute("""
                    INSERT INTO Detalle_Ventas (id_venta, id_producto, cantidad, precio_unitario, sub_total)
                    VALUES (?, ?, ?, ?, ?)
                """, (id_venta, producto_id, cantidad, precio, subtotal))

                #  Registrar automáticamente el movimiento en Inventario
                cursor.execute("""
                                INSERT INTO Inventario (id_producto, tipo_movimiento, cantidad, fecha)
                                VALUES (?, ?, ?, ?)
                            """, (producto_id, "venta", cantidad, fecha))

                #  Aquí actualizamos stock
                cursor.execute("""UPDATE Productos SET stock_actual = stock_actual - ? WHERE id_producto = ?""",
                               (cantidad, producto_id))

            # Registrar automáticamente el egreso en Finanzas
            cursor.execute("""
                            INSERT INTO MovimientosFinancieros (fecha, tipo, monto, descripcion)
                            VALUES (?, ?, ?,?)
                        """, (fecha, "INGRESO", total_obtenido, "Venta"))
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Venta registrada correctamente")
            ventana_form.destroy()
            ventana_emergente_ventas.deiconify()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta.\n{e}")

    # ===== Botones =====
    frame_botones = tk.LabelFrame(ventana_form, text="Acciones", bg="#f0f8ff", font=calibri_font, padx=10, pady=10)
    frame_botones.pack(pady=10)

    btn_agregar = tk.Button(frame_formulario, text="Agregar Producto", command=agregar_producto,
                            bg="#add8e6", font=calibri_font, width=15)
    btn_agregar.grid(row=7, column=0, columnspan=1, pady=10, sticky="e")

    btn_registrar = tk.Button(frame_botones, text="Registrar Venta", command=registrar_en_bd,
                              bg="#add8e6", font=calibri_font, width=15)
    btn_registrar.pack(side="left", padx=5)

    def cancelar_venta():
        combobox_clientes.set("Seleccionar Cliente")
        combobox_clientes.config(state="readonly")  # Habilita de nuevo
        combobox_producto.set("Seleccionar Producto")
        entry_cantidad.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        for item in tree.get_children():
            tree.delete(item)
        label_total.config(text="Total: 0.00")

    btn_cancelar = tk.Button(frame_botones, text="Cancelar Venta", command=cancelar_venta, bg="#add8e6",
                             font=calibri_font, width=15)
    btn_cancelar.pack(side="left", padx=5)

    btn_salir = tk.Button(frame_botones, text="Salir",
                          command=lambda: (ventana_form.destroy(), ventana_emergente_ventas.deiconify()),
                          bg="#add8e6", font=calibri_font, width=15)
    btn_salir.pack(side="left", padx=5)

def registrar_venta_db(fecha, cliente_id, productos):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO Ventas (fecha, cliente_id, total_obtenido)
            VALUES (?, ?, 0)
        """, (fecha, cliente_id))
        id_venta = cursor.lastrowid

        total = 0
        for id_producto, cantidad, precio_unitario in productos:
            subtotal = cantidad * precio_unitario
            total += subtotal

            cursor.execute("""
                INSERT INTO Detalle_Ventas (id_venta, id_producto, cantidad, precio_unitario, sub_total)
                VALUES (?, ?, ?, ?, ?)
            """, (id_venta, id_producto, cantidad, precio_unitario, subtotal))

            cursor.execute("""
                UPDATE Productos
                SET stock_actual = stock_actual - ?
                WHERE id_producto = ?
            """, (cantidad, id_producto))

        cursor.execute("""
            UPDATE Ventas
            SET total_gastado = ?
            WHERE id_venta = ?
        """, (total, id_venta))

        conn.commit()
        messagebox.showinfo("Éxito", f"Ventaa registrada correctamente.\nTotal: ${total: .2f}")

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"No se pudo registrar la Venta: {e}")
    finally:
        conn.close()

def ver_venta():
    calibri_font = font.Font(family="Calibri", size=14)
    ventana = tk.Toplevel()
    ventana.title("Ventas registradas")
    ventana.geometry("700x400")
    ventana.configure(bg="#e6f7ff")

    frame_formulario = tk.LabelFrame(ventana, text="Listados de Ventas", padx=10, pady=10, bg="#f0f8ff",
                                     font=("Calibri", 18, "bold"))
    frame_formulario.pack(pady=20, padx=20, fill="x")

    frame_treeview_contenedor = tk.Frame(frame_formulario)
    frame_treeview_contenedor.pack(fill="both", expand=True, padx=5, pady=5)
    tree = ttk.Treeview(frame_treeview_contenedor, columns=("id", "fecha", "cliente", "total"), show="headings")

    scrollbar = ttk.Scrollbar(frame_treeview_contenedor, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    tree.heading("id", text="ID Compra")
    tree.heading("fecha", text="Fecha")
    tree.heading("cliente", text="Cliente")
    tree.heading("total", text="Total Gastado")

    tree.column("id", width=80)
    tree.column("fecha", width=120)
    tree.column("cliente", width=200)
    tree.column("total", width=120)

    tree.pack(fill="both", expand=True)

    # --- Cargar datos desde la base ---
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id_venta, v.fecha, cl.nombre AS cliente, v.total_obtenido
            FROM Ventas v
            JOIN Clientes cl ON cl.id_cliente = v.cliente_id
            ORDER BY v.id_venta DESC
        """)
        ventas = cursor.fetchall()
        conn.close()

        for venta in ventas:
            tree.insert("", tk.END, values=venta)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar las ventas: {e}")

    # --- Evento doble clic para ver detalle ---
    def abrir_detalle(event):
        item = tree.selection()
        if not item:
            return
        valores = tree.item(item, "values")
        id_venta = valores[0]
        detalle_venta(id_venta)

    tree.bind("<Double-1>", abrir_detalle)

    btn_cerrar = tk.Button(frame_formulario, text="Cerrar Ventana",
                           command=lambda: ventana.destroy(), bg="#add8e6", font=calibri_font, width=15)
    btn_cerrar.pack(side="left", padx=5)

def detalle_venta(id_venta):
    calibri_font = font.Font(family="Calibri", size=14)
    ventana = tk.Toplevel()
    ventana.title(f"Detalle de la Ventaa {id_venta}")
    ventana.geometry("700x380")
    ventana.configure(bg="#e6f7ff")

    frame_formulario = tk.LabelFrame(ventana, text="Detalle de la Venta", padx=10, pady=10, bg="#f0f8ff",
                                     font=("Calibri", 18, "bold"))
    frame_formulario.pack(pady=20, padx=20, fill="x")

    frame_treeview_contenedor = tk.Frame(frame_formulario)
    frame_treeview_contenedor.pack(fill="both", expand=True, padx=5, pady=5)
    tree = ttk.Treeview(frame_treeview_contenedor, columns=("producto", "cantidad", "preciounitario", "total"),
                        show="headings")

    scrollbar = ttk.Scrollbar(frame_treeview_contenedor, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.heading("producto", text="Producto")
    tree.heading("cantidad", text="Cantidad")
    tree.heading("preciounitario", text="Precio Unitario")
    tree.heading("total", text="Total")

    tree.column("producto", width=80)
    tree.column("cantidad", width=120)
    tree.column("preciounitario", width=200)
    tree.column("total", width=120)

    tree.pack(fill="both", expand=True)

    btn_cerrar = tk.Button(frame_formulario, text="Cerrar Ventana",
                          command=lambda: ventana.destroy(), bg="#add8e6", font=calibri_font, width=15)
    btn_cerrar.pack(side="left", padx=5)

    # --- Cargar datos desde la base ---
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pr.descripcion, v.cantidad, v.precio_unitario, v.sub_total
            FROM Detalle_Ventas v
            JOIN Productos pr ON v.id_producto = pr.id_producto
            WHERE v.id_venta = ?
        """, (id_venta,))
        detalles = cursor.fetchall()
        conn.close()

        for det in detalles:
            tree.insert("", tk.END, values=det)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el detalle: {e}")
