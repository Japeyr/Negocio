import tkinter as tk
from tkinter import ttk, messagebox, font
from ConexionSQLite import conectar_db

def registrar_movimiento_financiero(ventana_finanzas):
    # Fuente Calibri
    calibri_font = font.Font(family="Calibri", size=14)

    ventana_finanzas.withdraw()
    ventana_movimiento_financiero = tk.Toplevel(ventana_finanzas)
    ventana_movimiento_financiero.title("Gestión de Finanzas")
    ventana_movimiento_financiero.geometry("700x680")
    ventana_movimiento_financiero.configure(bg="#e6f7ff")

    # === Formulario de nuevo movimiento ===
    frame_form = tk.LabelFrame(ventana_movimiento_financiero, text="Registrar Movimiento", bg="#f0f8ff",
                               font=calibri_font, padx=10, pady=10)
    frame_form.pack(pady=10, fill="x", padx=20)

    tk.Label(frame_form, text="Monto:", bg="#e6f7ff").grid(row=0, column=0, padx=5, pady=5)
    entry_monto = tk.Entry(frame_form)
    entry_monto.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Descripción:", bg="#e6f7ff").grid(row=1, column=0, padx=5, pady=5)
    entry_desc = tk.Entry(frame_form)
    entry_desc.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_form, text="Tipo:", bg="#e6f7ff").grid(row=2, column=0, padx=5, pady=5)
    tipo_var = tk.StringVar(value="INGRESO")
    combo_tipo = ttk.Combobox(frame_form, textvariable=tipo_var, values=["INGRESO", "EGRESO"])
    combo_tipo.grid(row=2, column=1, padx=5, pady=5)

    def registrar_movimiento():
        monto = entry_monto.get()
        desc = entry_desc.get()
        tipo = tipo_var.get()
        if not monto or not desc:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        try:
            monto = float(monto)
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor a cero")
                return

            # Aquí se inserta en la BD MovimientosFinancieros
            conn = conectar_db()
            cursor = conn.cursor()

            cursor.execute("""
                    INSERT INTO MovimientosFinancieros (tipo, monto, descripcion)
                    VALUES (?, ?, ?)
                """, (tipo, monto, desc))

            conn.commit()
            conn.close()
            ver_movimientos_financieros()
            print(f"Movimiento registrado: {tipo} - ${monto} ({desc})")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido")

    tk.Button(frame_form, text="Registrar", command=registrar_movimiento, bg="#add8e6").grid(row=3, column=0, columnspan=2, pady=10)

    # === Tabla de movimientos ===

    frame_form_list = tk.LabelFrame(ventana_movimiento_financiero, text="Movimientos Financieros", bg="#f0f8ff",
                               font=calibri_font, padx=10, pady=10)
    frame_form_list.pack(pady=10, fill="x", padx=20)

    columnas = ("Fecha", "Tipo", "Monto", "Descripción")
    tabla = ttk.Treeview(frame_form_list, columns=columnas, show="headings", height=10)
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(fill="both", expand=True, padx=20, pady=10)

    def ver_movimientos_financieros():
        conn = conectar_db()
        cursor = conn.cursor()

        cursor.execute("SELECT fecha, tipo, monto, descripcion FROM MovimientosFinancieros")
        movimientos = cursor.fetchall()
        conn.close()

        # limpiar tabla
        for item in tabla.get_children():
            tabla.delete(item)

        # insertar filas
        for mov in movimientos:
            tabla.insert("", "end", values=mov)

    # Botones adicionales
    frame_form_acciones = tk.LabelFrame(ventana_movimiento_financiero, text="Acciones", bg="#f0f8ff",
                                    font=calibri_font, padx=10, pady=10)
    frame_form_acciones.pack(pady=10, fill="x", padx=20)

    tk.Button(frame_form_acciones, text="Movimientos Financieros", bg="#add8e6",
              command=ver_movimientos_financieros).pack(side="left", padx=10)
    tk.Button(frame_form_acciones, text="Eliminar Movimiento", bg="#add8e6").pack(side="left", padx=10)
    button_cerrar = tk.Button(frame_form_acciones, text="Cerrar",
                        command=lambda: cerrar_ventana(ventana_movimiento_financiero, ventana_finanzas),
                              bg="#add8e6", width=15)
    button_cerrar.pack(padx=10)


def ver_resumen_financiero(ventana_finanzas):
    # Fuente Calibri
    calibri_font = font.Font(family="Calibri", size=14)

    ventana_finanzas.withdraw()
    ventana_resumen_financiero = tk.Toplevel(ventana_finanzas)
    ventana_resumen_financiero.title("Resumen Financiero")
    ventana_resumen_financiero.geometry("700x170")
    ventana_resumen_financiero.configure(bg="#e6f7ff")

    frame_resumen = tk.LabelFrame(ventana_resumen_financiero, text="Resumen Financiero", font= calibri_font,
                                  bg="#f0f8ff")
    frame_resumen.pack(pady=10, fill="x", padx=20)

    # === Resumen Financiero ===
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(monto) FROM MovimientosFinancieros WHERE tipo='INGRESO'")
    ingresos = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(monto) FROM MovimientosFinancieros WHERE tipo='EGRESO'")
    egresos = cursor.fetchone()[0] or 0

    conn.close()

    saldo = ingresos - egresos

    tk.Label(frame_resumen, text=f"Ingresos: ${ingresos}",bg="#e6f7ff", font=("Calibri", 16)).grid(row=0, column=0,
                                                                                                   padx=20)
    tk.Label(frame_resumen, text=f"Egresos: ${egresos}",bg="#e6f7ff", font=("Calibri", 16)).grid(row=0, column=1,
                                                                                                 padx=20)
    tk.Label(frame_resumen, text=f"Saldo: ${saldo}",bg="#e6f7ff", font=("Calibri", 16, "bold")).grid(row=0, column=2,
                                                                                                     padx=20)

    frame_boton_salir = tk.Frame(ventana_resumen_financiero, bg="#f0f8ff")
    frame_boton_salir.pack(pady=10)
    button_salir_resumen = tk.Button(frame_boton_salir, text="Cerar",
                                     command=lambda: cerrar_ventana(ventana_resumen_financiero, ventana_finanzas),
                                     bg="#add8e6", width=15)
    button_salir_resumen.grid(row=1, column=0, columnspan=3, pady=10)

def resultados_obtenidos(ventana_finanzas):
    # Fuente Calibri
    calibri_font = font.Font(family="Calibri", size=14)

    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("""
            SELECT v.id_venta, v.fecha, c.nombre,
                   SUM(dv.cantidad * dv.precio_unitario) AS ingreso,
                   SUM(dv.cantidad * p.precio_compra) AS costo,
                   SUM((dv.precio_unitario - p.precio_compra) * dv.cantidad) AS ganancia
            FROM Ventas v
            JOIN Detalle_Ventas dv ON v.id_venta = dv.id_venta
            JOIN Productos p ON dv.id_producto = p.id_producto
            JOIN Clientes c ON v.cliente_id = c.id_cliente
            GROUP BY v.id_venta, v.fecha, c.nombre
            ORDER BY v.fecha DESC
        """)
    rows = cursor.fetchall()
    conn.close()

    # Crear ventana
    ventana_finanzas.withdraw()
    ventana_resultado_financiero = tk.Toplevel(ventana_finanzas)
    ventana_resultado_financiero.title("Ganancias por Ventas")
    ventana_resultado_financiero.geometry("700x420")
    ventana_resultado_financiero.configure(bg="#e6f7ff")

    frame_form_resultados = tk.LabelFrame(ventana_resultado_financiero, text="Resultados por Producto", bg="#f0f8ff",
                               font=calibri_font, padx=10, pady=10)
    frame_form_resultados.pack(pady=10, fill="x", padx=20)

    frame_treeview_contenedor = tk.Frame(frame_form_resultados)
    frame_treeview_contenedor.pack(fill="both", expand=True, padx=5, pady=5)
    tree = ttk.Treeview(frame_treeview_contenedor, columns= ("ID", "Fecha", "Cliente", "Ingreso", "Costo", "Resultado"),
                        show="headings")

    scrollbar = ttk.Scrollbar(frame_treeview_contenedor, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    tree.heading("ID", text="ID")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Cliente", text="Cliente")
    tree.heading("Ingreso", text="Ingreso")
    tree.heading("Costo", text="Costo")
    tree.heading("Resultado", text="Resultado")

    tree.column("ID", width=40)
    tree.column("Fecha", width=80)
    tree.column("Cliente", width=150)
    tree.column("Ingreso", width=100)
    tree.column("Costo", width=100)
    tree.column("Resultado", width=100)

    for col in ("ID", "Fecha", "Cliente", "Ingreso", "Costo", "Resultado"):
        tree.heading(col, text=col)

    for row in rows:
        tree.insert("", "end", values=row)

    boton_cerrar = tk.Button(frame_form_resultados, text="Cerrar Ventana",
                           command=lambda: cerrar_ventana(ventana_resultado_financiero, ventana_finanzas), bg="#add8e6",
                             font=calibri_font,
                             width=15)
    boton_cerrar.pack(side="left", padx=5)


def cerrar_ventana(ventana_a_cerrar, ventana_a_mostrar=None):
    ventana_a_cerrar.destroy()
    if ventana_a_mostrar:
        ventana_a_mostrar.deiconify()
