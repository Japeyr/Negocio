import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import ttk  # Importa ttk para los Comboboxes
from ConexionSQLite import crear_tablas
from Finanzas import registrar_movimiento_financiero, ver_resumen_financiero, resultados_obtenidos
from ListaClientes import insertar_cliente, listar_clientes
from ListaProductos import insertar_producto, ver_productos
from ListaProveedores import listar_proveedores, insertar_proveedor, mostrar_lista_proveedores
from OperacionCompra import registrar_compra, ver_compra
from OperacionVenta import registrar_venta, ver_venta
from Stock import ver_stock_actual, ajuste_manual_inventario, ver_movimiento_inventario

# Crea la ventana principal

root = tk.Tk()
root.title("Gestión de Negocio")
root.geometry("680x780")
root.configure(bg="#e6f7ff")

# Fuente Calibri
calibri_font = font.Font(family="Calibri", size=14)

# --- Variable global para almacenar el ID del proveedor seleccionado ---
# Esto es útil si necesitas acceder al ID del proveedor en otras partes de tu función `insertar_producto`
# Fuera de la función, para que su valor persista
selected_proveedor_id = tk.StringVar()  # Para almacenar el ID del proveedor seleccionado
selected_proveedor_id.set("")   # Inicialmente vacío


def ventana_productos():
    root.withdraw()
    ventana_emergente_productos = tk.Toplevel(root)
    ventana_emergente_productos.title("Productos")
    ventana_emergente_productos.geometry("610x640")
    ventana_emergente_productos.configure(bg="#e6f7ff")

    # Frame principal
    frame_formulario_productos = tk.LabelFrame(ventana_emergente_productos, text="Nuevo Producto",
                                     bg="#f0f8ff", font=calibri_font, padx=10, pady=10)
    frame_formulario_productos.pack(padx=20, pady=20, fill="x")

    label_productos = tk.Label(frame_formulario_productos, text="Producto", bg="#f0f8ff", font=calibri_font)
    label_productos.grid(row=0, column=0, columnspan=2, pady=10)

    # ===== CAMPOS CON ENTRADAS DE TEXTO =====
    label_cod = tk.Label(frame_formulario_productos, text="Código:", bg="#f0f8ff", font=calibri_font)
    label_cod.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_cod = tk.Entry(frame_formulario_productos, font=calibri_font)
    entry_cod.grid(row=1, column=1, sticky="w", padx=5, pady=5)

    label_descripcion = tk.Label(frame_formulario_productos, text="Descripción:", bg="#f0f8ff", font=calibri_font)
    label_descripcion.grid(row=2, column=0, sticky="e", padx=5, pady=5)
    entry_descripcion = tk.Entry(frame_formulario_productos, font=calibri_font)
    entry_descripcion.grid(row=2, column=1, sticky="w", padx=5, pady=5)

    label_precio_compra = tk.Label(frame_formulario_productos, text="Precio de Compra:", bg="#f0f8ff",
                                   font=calibri_font)
    label_precio_compra.grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_precio_compra = tk.Entry(frame_formulario_productos, font=calibri_font)
    entry_precio_compra.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    label_precio_venta = tk.Label(frame_formulario_productos, text="Precio de Venta:", bg="#f0f8ff", font=calibri_font)
    label_precio_venta.grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_precio_venta = tk.Entry(frame_formulario_productos, font=calibri_font)
    entry_precio_venta.grid(row=4, column=1, sticky="w", padx=5, pady=5)

    label_stock_actual = tk.Label(frame_formulario_productos, text="Stock actual:", bg="#f0f8ff", font=calibri_font)
    label_stock_actual.grid(row=5, column=0, sticky="e", padx=5, pady=5)
    entry_stock_actual = tk.Entry(frame_formulario_productos, font=calibri_font)
    entry_stock_actual.grid(row=5, column=1, sticky="w", padx=5, pady=5)

    # --- AQUÍ: Combobox para Talle ---


    label_talle = tk.Label(frame_formulario_productos, text="Talle:", bg="#f0f8ff", font=calibri_font)
    label_talle.grid(row=6, column=0, sticky="e", padx=5, pady=5)


    opciones_talle_display = ["85", "90", "95", "100"]

    combobox_talle = ttk.Combobox(frame_formulario_productos, values=opciones_talle_display, font=calibri_font,
                                  state="readonly")
    combobox_talle.grid(row=6, column=1, sticky="w", padx=5, pady=5)
    combobox_talle.set("Seleccionar")


    # ===== COMBOBOX COLOR =====
    label_color = tk.Label(frame_formulario_productos, text="Color:", bg="#f0f8ff", font=calibri_font)
    label_color.grid(row=7, column=0, sticky="e", padx=5, pady=5)

    opciones_color_display = ["Seleccionar", "Blanco", "Negro", "Rojo", "Rosa", "Azul", "Verde"]
    combobox_color = ttk.Combobox(frame_formulario_productos, values=opciones_color_display, font=calibri_font,
                                  state="readonly")
    combobox_color.grid(row=7, column=1, sticky="w", padx=5, pady=5)
    combobox_color.set("Seleccionar")

    # ===== COMBOBOX PROVEEDOR =====
    label_proveedor = tk.Label(frame_formulario_productos, text="Proveedor:", bg="#f0f8ff", font=calibri_font)
    label_proveedor.grid(row=8, column=0, sticky="e", padx=5, pady=5)

    proveedores_db = listar_proveedores()
    proveedores_map = {p[1]: p[0] for p in proveedores_db}
    nombres_proveedores = [p[1] for p in proveedores_db]
    opciones_proveedor_display = ["Seleccionar Proveedor"] + nombres_proveedores

    combobox_proveedor = ttk.Combobox(frame_formulario_productos, values=opciones_proveedor_display, font=calibri_font,
                                      state="readonly")
    combobox_proveedor.grid(row=8, column=1, sticky="w", padx=5, pady=5)
    combobox_proveedor.set("Seleccionar Proveedor")

    widgets_a_limpiar = [
        entry_cod,
        entry_descripcion,
        entry_precio_compra,
        entry_precio_venta,
        entry_stock_actual,  # entry_stock_actual es un Entry, no un Spinbox en tu código principal
        combobox_talle,
        combobox_color,
        combobox_proveedor
    ]

    # ===== BOTONES =====

    # Frame para formulario
    frame_formulario_productos = tk.LabelFrame(ventana_emergente_productos, text="Acciones", bg="#f0f8ff",
                                               font=calibri_font, padx=10, pady=10)
    frame_formulario_productos.pack(padx=20, pady=20, fill="x")

    button_agregar_productos = tk.Button(frame_formulario_productos, text="Agregar\n Producto",
                                         command=lambda: insertar_producto(
                                             entry_cod.get(),
                                             entry_descripcion.get(),
                                             entry_precio_compra.get(),
                                             entry_precio_venta.get(),
                                             entry_stock_actual.get(),
                                             combobox_talle.get(),
                                             combobox_color.get(),
                                             proveedores_map.get(combobox_proveedor.get(), ""),
                                             widgets_a_limpiar,
                                             selected_proveedor_id,
                                             combobox_talle,
                                             combobox_color,
                                             combobox_proveedor
                                         ),
                                         bg="#add8e6", font=calibri_font, width=16)
    button_agregar_productos.grid(row=0, column=0, padx=5, pady=5)

    button_ver_productos = tk.Button(frame_formulario_productos, text="Ver Productos\n a Editar",
                                     command=lambda: ver_productos(ventana_emergente_productos),
                                     bg="#add8e6", font=calibri_font, width=16)
    button_ver_productos.grid(row=0, column=1, padx=5, pady=5)

    button_salir_productos = tk.Button(frame_formulario_productos, text="Salir", height="2",
                                       command=lambda: cerrar_ventana_emergente(ventana_emergente_productos),
                                       bg="#add8e6", font=calibri_font, width=16)
    button_salir_productos.grid(row=0, column=2, padx=5, pady=5)

def ventana_proveedores():
    root.withdraw()  # Oculta la ventana principal
    ventana_emergente_proveedores = tk.Toplevel(root)
    ventana_emergente_proveedores.title("Proveedor")
    ventana_emergente_proveedores.geometry("680x350")
    ventana_emergente_proveedores.configure(bg="#e6f7ff")

    # Frame para formulario
    frame_formulario_proveedores = tk.LabelFrame(ventana_emergente_proveedores, text="Nuevo Proveedor",
                                               bg="#f0f8ff", font=calibri_font, padx=10, pady=10)
    frame_formulario_proveedores.pack(padx=20, pady=20, fill="x")

    # Elementos de la interfaz de la ventana

    label_proveedores = tk.Label(frame_formulario_proveedores, text="Proveedor", bg="#f0f8ff", font=calibri_font)
    label_proveedores.grid(row=0, column=0, columnspan=4, pady=5, sticky="n")

    frame_proveedor_nombre = tk.Frame(frame_formulario_proveedores, bg="#f0f8ff")
    frame_proveedor_nombre.grid(row=1, column=0, columnspan=4, pady=5)

    label_proveedor_nombre = tk.Label(frame_proveedor_nombre, text="Nombre:", bg="#f0f8ff", font=calibri_font)
    label_proveedor_nombre.pack(side="left", padx=5)

    entry_proveedor_nombre = tk.Entry(frame_proveedor_nombre, font=calibri_font)
    entry_proveedor_nombre.pack(side="left", padx=5)

    frame_proveedor_direccion = tk.Frame(frame_formulario_proveedores, bg="#f0f8ff")
    frame_proveedor_direccion.grid(row=2, column=0, columnspan=4, pady=5)

    label_proveedor_direccion = tk.Label(frame_proveedor_direccion, text="Dirección:", bg="#f0f8ff",
                                         font=calibri_font)
    label_proveedor_direccion.pack(side="left", padx=5)

    entry_proveedor_direccion = tk.Entry(frame_proveedor_direccion, font=calibri_font)
    entry_proveedor_direccion.pack(side="left", padx=5)

    frame_proveedor_contacto = tk.Frame(frame_formulario_proveedores, bg="#f0f8ff")
    frame_proveedor_contacto.grid(row=3, column=0, columnspan=4, pady=5)

    label_proveedor_contacto = tk.Label(frame_proveedor_contacto, text="Contacto:", bg="#f0f8ff",
                                        font=calibri_font)
    label_proveedor_contacto.pack(side="left", padx=5)

    entry_proveedor_contacto = tk.Entry(frame_proveedor_contacto, font=calibri_font)
    entry_proveedor_contacto.pack(side="left", padx=5)

    # Frame para agrupar los botones horizontalmente

    frame_botones_proveedores = tk.LabelFrame(
        ventana_emergente_proveedores,
        text="Acciones",
        bg="#f0f8ff",
        font=calibri_font,
        padx=10,
        pady=10
    )
    frame_botones_proveedores.pack(padx=20, pady=10, fill="x")

    widget_proveedores_a_limpiar = [entry_proveedor_nombre, entry_proveedor_direccion, entry_proveedor_contacto]

    button_agregar_proveedor = tk.Button(frame_botones_proveedores, text="Agregar Proveedor",
                                         command=lambda: insertar_proveedor(entry_proveedor_nombre.get(),
                                                                            entry_proveedor_contacto.get(),
                                                                            entry_proveedor_direccion.get(),
                                                                            widget_proveedores_a_limpiar), bg="#add8e6",
                                         font=calibri_font, width=15)
    button_agregar_proveedor.pack(side="left", padx=5)

    button_ver_proveedor = tk.Button(frame_botones_proveedores, text="Ver Proveedores",
                                     command=lambda: mostrar_lista_proveedores(ventana_emergente_proveedores),
                                     bg="#add8e6", font=calibri_font, width=15)
    button_ver_proveedor.pack(side="left", padx=5)

    button_salir_proveedor = tk.Button(frame_botones_proveedores, text="Salir",
                                       command=lambda: cerrar_ventana_emergente(ventana_emergente_proveedores),
                                       bg="#add8e6", font=calibri_font, width=15)
    button_salir_proveedor.pack(side="left", padx=5)


def ventana_clientes():
    root.withdraw()  # Oculta la ventana principal
    ventana_emergente_clientes = tk.Toplevel(root)
    ventana_emergente_clientes.title("Clientes")
    ventana_emergente_clientes.geometry("580x330")
    ventana_emergente_clientes.configure(bg="#e6f7ff")

    # Frame para formulario
    frame_formulario_clientes = tk.LabelFrame(ventana_emergente_clientes, text="Nuevo Cliente", bg="#f0f8ff",
                                              font=calibri_font, padx=10, pady=10)
    frame_formulario_clientes.pack(padx=20, pady=20, fill="x")

    # Elementos de la interfaz de la ventana

    label_cliente = tk.Label(frame_formulario_clientes, text="Cliente", bg="#f0f8ff", font=calibri_font)
    label_cliente.grid(row=0, column=0, columnspan=4, pady=5, sticky="n")

    frame_cliente_nombre = tk.Frame(frame_formulario_clientes, bg="#f0f8ff")
    frame_cliente_nombre.grid(row=1, column=0, columnspan=4, pady=5)

    label_cliente_nombre = tk.Label(frame_cliente_nombre, text="Nombre:", bg="#f0f8ff", font=calibri_font)
    label_cliente_nombre.pack(side="left", padx=5)

    entry_cliente_nombre = tk.Entry(frame_cliente_nombre, font=calibri_font)
    entry_cliente_nombre.pack(side="left", padx=5)

    frame_cliente_contacto = tk.Frame(frame_formulario_clientes, bg="#f0f8ff")
    frame_cliente_contacto.grid(row=3, column=0, columnspan=4, pady=5)

    label_cliente_contacto = tk.Label(frame_cliente_contacto, text="Contacto:", bg="#f0f8ff", font=calibri_font)
    label_cliente_contacto.pack(side="left", padx=5)

    entry_cliente_contacto = tk.Entry(frame_cliente_contacto, font=calibri_font)
    entry_cliente_contacto.pack(side="left", padx=5)

    widget_clientes_a_limpiar = [entry_cliente_nombre, entry_cliente_contacto]

    # Frame para agrupar los botones horizontalmente

    frame_botones_clientes = tk.LabelFrame(ventana_emergente_clientes, text="Acciones", bg="#f0f8ff", font=calibri_font,
                                           padx=10, pady=10)
    frame_botones_clientes.pack(padx=20, pady=10, fill="x")

    button_agregar_clientes = tk.Button(frame_botones_clientes, text="Agregar Cliente",
                                        command=lambda: insertar_cliente(entry_cliente_nombre.get(),
                                                                         entry_cliente_contacto.get(),
                                                                         widget_clientes_a_limpiar), bg="#add8e6",
                                        font=calibri_font, width=15)
    button_agregar_clientes.pack(side="left", padx=5)

    button_ver_clientes = tk.Button(frame_botones_clientes, text="Ver Clientes",
                                    command=lambda: listar_clientes(ventana_emergente_clientes),
                                    bg="#add8e6", font=calibri_font, width=15)
    button_ver_clientes.pack(side="left", padx=5)

    button_salir_clientes = tk.Button(frame_botones_clientes, text="Salir",
                                      command=lambda: cerrar_ventana_emergente(ventana_emergente_clientes),
                                      bg="#add8e6", font=calibri_font, width=15)
    button_salir_clientes.pack(side="left", padx=5)

def ventana_compras():
    root.withdraw()  # Oculta la ventana principal
    ventana_emergente_compras = tk.Toplevel(root)
    ventana_emergente_compras.title("Compras")
    ventana_emergente_compras.geometry("680x180")
    ventana_emergente_compras.configure(bg="#e6f7ff")

    # Frame para formulario
    frame_formulario_compras = tk.LabelFrame(ventana_emergente_compras, text="Acciones", bg="#f0f8ff",
                                             font=calibri_font, padx=10, pady=10)
    frame_formulario_compras.pack(padx=20, pady=20, fill="x")

    # Elementos de la interfaz de la ventana

    label_compras = tk.Label(frame_formulario_compras, text="Compras", bg="#f0f8ff", font=calibri_font)
    label_compras.grid(row=0, column=0, columnspan=4, pady=5, sticky="n")

    # Frame para agrupar los botones horizontalmente

    frame_botones_compras = tk.Frame(frame_formulario_compras, bg="#f0f8ff")
    frame_botones_compras.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    button_registrar_compra = tk.Button(frame_botones_compras, text="Registrar Compra",
                                        command=lambda: registrar_compra(ventana_emergente_compras), bg="#add8e6",
                                        font=calibri_font, width=15)
    button_registrar_compra.pack(side="left", padx=5)

    button_ver_compras = tk.Button(frame_botones_compras, text="Ver Compras", command=ver_compra, bg="#add8e6",
                                   font=calibri_font, width=15)
    button_ver_compras.pack(side="left", padx=5)

    button_salir_compras = tk.Button(frame_botones_compras, text="Salir",
                                     command=lambda: cerrar_ventana_emergente(ventana_emergente_compras), bg="#add8e6",
                                     font=calibri_font, width=15)
    button_salir_compras.pack(side="left", padx=5)

def ventana_ventas():
    root.withdraw()  # Oculta la ventana principal
    ventana_emergente_ventas = tk.Toplevel(root)
    ventana_emergente_ventas.title("Ventas")
    ventana_emergente_ventas.geometry("680x180")
    ventana_emergente_ventas.configure(bg="#e6f7ff")

    # Frame para formulario
    frame_formulario_ventas = tk.LabelFrame(ventana_emergente_ventas, text="Acciones", bg="#f0f8ff", font=calibri_font,
                                            padx=10, pady=10)
    frame_formulario_ventas.pack(padx=20, pady=20, fill="x")

    # Elementos de la interfaz de la ventana

    label_ventas = tk.Label(frame_formulario_ventas, text="Ventas", bg="#f0f8ff", font=calibri_font)
    label_ventas.grid(row=0, column=0, columnspan=4, pady=5, sticky="n")

    # Frame para agrupar los botones horizontalmente

    frame_botones_ventas = tk.Frame(frame_formulario_ventas, bg="#f0f8ff")
    frame_botones_ventas.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    button_registrar_venta = tk.Button(frame_botones_ventas, text="Registrar Venta",
                                       command=lambda: registrar_venta(ventana_emergente_ventas), bg="#add8e6",
                                       font=calibri_font, width=15)
    button_registrar_venta.pack(side="left", padx=5)

    button_ver_venta = tk.Button(frame_botones_ventas, text="Ver Ventas", command=ver_venta, bg="#add8e6",
                                 font=calibri_font, width=15)
    button_ver_venta.pack(side="left", padx=5)

    button_salir_venta = tk.Button(frame_botones_ventas, text="Salir",
                                   command=lambda: cerrar_ventana_emergente(ventana_emergente_ventas), bg="#add8e6",
                                   font=calibri_font, width=15)
    button_salir_venta.pack(side="left", padx=5)

def ventana_inventario():
    root.withdraw()  # Oculta la ventana principal
    ventana_emergente_inventario = tk.Toplevel(root)
    ventana_emergente_inventario.title("Inventario")
    ventana_emergente_inventario.geometry("800x230")
    ventana_emergente_inventario.configure(bg="#e6f7ff")

    # Frame para formulario
    frame_formulario_inventario = tk.LabelFrame(ventana_emergente_inventario, text="Acciones",
                                               bg="#f0f8ff", font=calibri_font, padx=10, pady=10)
    frame_formulario_inventario.pack(padx=20, pady=20, fill="x")

    # Elementos de la interfaz de la ventana

    label_inventario = tk.Label(frame_formulario_inventario, text="Inventario", bg="#f0f8ff", font=calibri_font)
    label_inventario.grid(row=0, column=0, columnspan=4, pady=5, sticky="n")

    # Frame para agrupar los botones horizontalmente

    frame_botones_inventario = tk.Frame(frame_formulario_inventario, bg="#f0f8ff")
    frame_botones_inventario.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    button_movimiento_inventario = tk.Button(frame_botones_inventario, text="Ver Movimientos\nde Inventario",
                                             command= lambda: ver_movimiento_inventario(ventana_emergente_inventario),
                                             bg="#add8e6", font=calibri_font, width=16)
    button_movimiento_inventario.pack(side="left", padx=5)

    button_ajuste_manual_inventario = tk.Button(frame_botones_inventario, text="Ajuste Manual\nde Inventario",
                                                command=lambda: ajuste_manual_inventario(ventana_emergente_inventario),
                                                bg="#add8e6", font=calibri_font, width=16)
    button_ajuste_manual_inventario.pack(side="left", padx=5)

    button_stock_actual = tk.Button(frame_botones_inventario, text="Ver Stock\nActual",
                                    command=lambda: ver_stock_actual(ventana_emergente_inventario), bg="#add8e6",
                                    font=calibri_font, width=16)
    button_stock_actual.pack(side="left", padx=5)

    button_salir_inventario = tk.Button(frame_botones_inventario, text="Salir", height="2",
                                   command=lambda: cerrar_ventana_emergente(ventana_emergente_inventario), bg="#add8e6",
                                   font=calibri_font, width=16)
    button_salir_inventario.pack(side="left", padx=5)

def ventana_finanzas():
    root.withdraw()  # Oculta la ventana principal
    ventana_emergente_finanzas = tk.Toplevel(root)
    ventana_emergente_finanzas.title("Finanzas")
    ventana_emergente_finanzas.geometry("800x230")
    ventana_emergente_finanzas.configure(bg="#e6f7ff")

    # Frame para formulario
    frame_formulario_finanzas = tk.LabelFrame(ventana_emergente_finanzas, text="Acciones", bg="#f0f8ff",
                                              font=calibri_font, padx=10, pady=10)
    frame_formulario_finanzas.pack(padx=20, pady=20, fill="x")

    # Elementos de la interfaz de la ventana

    label_finanzas = tk.Label(frame_formulario_finanzas, text="Finanzas", bg="#f0f8ff", font=calibri_font)
    label_finanzas.grid(row=0, column=0, columnspan=4, pady=5, sticky="n")

    # Frame para agrupar los botones horizontalmente

    frame_botones_finanzas = tk.Frame(frame_formulario_finanzas, bg="#f0f8ff")
    frame_botones_finanzas.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    button_registrar_movimiento_financiero = tk.Button(frame_botones_finanzas, text="Registrar Movimiento\nFinanciero",
                                            command=lambda: registrar_movimiento_financiero(ventana_emergente_finanzas),
                                                       bg="#add8e6", font=calibri_font, width=16)
    button_registrar_movimiento_financiero.pack(side="left", padx=5)

    button_ver_movimientos_financieros = tk.Button(frame_botones_finanzas, text="Ver Resumen\nFinanciero",
                                                command=lambda: ver_resumen_financiero(ventana_emergente_finanzas),
                                                   bg="#add8e6", font=calibri_font, width=16)
    button_ver_movimientos_financieros.pack(side="left", padx=5)

    button_resultados_financieros = tk.Button(frame_botones_finanzas, text="Resultado\nEconómico",
                                              command=lambda: resultados_obtenidos(ventana_emergente_finanzas),
                                              bg="#add8e6", font=calibri_font, width=16)
    button_resultados_financieros.pack(side="left", padx=5)

    button_salir_finanzas = tk.Button(frame_botones_finanzas, text="Salir", height="2",
                                   command=lambda: cerrar_ventana_emergente(ventana_emergente_finanzas), bg="#add8e6",
                                   font=calibri_font, width=16)
    button_salir_finanzas.pack(side="left", padx=5)

def cerrar_ventana_emergente(ventana):
    if messagebox.askokcancel("Cerrar", "¿Seguro que querés cerrar esta ventana?"):
        ventana.destroy()
        root.deiconify()  # Vuelve a mostrar la principal

def productos():
    ventana_productos()

def proveedores():
    ventana_proveedores()

def clientes():
    ventana_clientes()

def compras():
    ventana_compras()

def ventas():
    ventana_ventas()

def inventario():
    ventana_inventario()

def finanzas():
    ventana_finanzas()

def salir():
    if messagebox.askokcancel("Salir", "¿Seguro que querés salir del sistema?"):
        root.destroy()  # Esto cierra la ventana



# Elementos de la interfaz
frame_formulario_menu = tk.LabelFrame(root, text="Menú del Sistema", bg="#f0f8ff", font=calibri_font, padx=10, pady=10)
frame_formulario_menu.pack(padx=20, pady=20, fill="x")
label_name = tk.Label(root, text="Sistema de Gestion de Negocio", bg="#f0f8ff", font=calibri_font)
label_name.pack(pady=5)

label_aviso = tk.Label(frame_formulario_menu, text='''Si es la primera vez que usa esta aplicación, 
HAGA CLICK EN CREAR BASE DE DATOS. 
Luego ingrese los productos, los clientes y los provedores.
Lo siguiente a realizar es ir a Finanzas y en Ingresar Movimientos 
crear un movimeinto de tipo "INGRESOS" de descripción Capital, para 
posteriormente registar productos, proveedores y clientes. En 
productos se recomienda poner la cantidad en cero para ir sumando 
productos al stock a medidad que se compran, salvo que se tenga de 
antes un stock anterior''',
                       bg="#f0f8ff", font=calibri_font)
label_aviso.pack(pady=50)

# Frame para agrupar los botones horizontalmente
frame_formulario_botones = tk.LabelFrame(root, text="Botones del Sistema", bg="#f0f8ff", font=calibri_font, padx=10,
                                         pady=10)
frame_formulario_botones.pack(padx=20, pady=20, fill="x")
frame_botones = tk.Frame(frame_formulario_botones, bg="#f0f8ff")
frame_botones.pack(pady=20)

button_productos = tk.Button(frame_botones, text="Productos", command=productos, bg="#add8e6", font=calibri_font,
                       width=15)
button_productos.pack(side="left", padx=5)

button_proveedores = tk.Button(frame_botones, text="Proveedores", command=proveedores, bg="#add8e6",
                          font=calibri_font, width=15)
button_proveedores.pack(side="left", padx=5)

button_clientes = tk.Button(frame_botones, text="Clientes", command=clientes, bg="#add8e6", font=calibri_font, width=15)
button_clientes.pack(side="left", padx=5)

# Frame para agrupar los botones horizontalmente
frame_botones = tk.Frame(frame_formulario_botones, bg="#f0f8ff")
frame_botones.pack(pady=20)

button_compras = tk.Button(frame_botones, text="Compras", command=compras, bg="#add8e6", font=calibri_font, width=15)
button_compras.pack(side="left", padx=5)

button_ventas = tk.Button(frame_botones, text="Ventas", command=ventas, bg="#add8e6", font=calibri_font, width=15)
button_ventas.pack(side="left", padx=5)

button_inventario = tk.Button(frame_botones, text="Inventario", command=inventario, bg="#add8e6", font=calibri_font,
                              width=15)
button_inventario.pack(side="left", padx=5)

frame_botones = tk.Frame(frame_formulario_botones, bg="#f0f8ff")
frame_botones.pack(pady=20)

button_finanzas = tk.Button(frame_botones, text="Finanzas", command=finanzas, bg="#add8e6", font=calibri_font, width=15)
button_finanzas.pack(side="left", padx=5)

button_base_datos = tk.Button(frame_botones, text="Crear Base de Datos", command=crear_tablas, bg="#add8e6",
                              font=calibri_font, width=15)
button_base_datos.pack(side="left", padx=5)

button_salir = tk.Button(frame_botones, text="Salir", command=salir, bg="#add8e6", font=calibri_font, width=15)
button_salir.pack(side="left", padx=5)

# Ejecutar la aplicación
root.mainloop()
