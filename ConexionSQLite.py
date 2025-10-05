import sqlite3

def conectar_db():
    return sqlite3.connect("Negocio.db")

def crear_tablas():
    conexion = sqlite3.connect("Negocio.db")
    cursor = conexion.cursor()

    tablas = [
        '''CREATE TABLE IF NOT EXISTS Clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            contacto TEXT
        );''',

        '''CREATE TABLE IF NOT EXISTS Proveedores (
            id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            contacto TEXT,
            direccion TEXT
        );''',

        '''CREATE TABLE IF NOT EXISTS Productos (
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            cod_producto TEXT,
            descripcion TEXT,
            precio_compra REAL,
            precio_venta REAL,
            stock_actual INTEGER,
            talle TEXT,
            color TEXT,
            proveedor_id INTEGER,
            FOREIGN KEY(proveedor_id) REFERENCES Proveedores(id_proveedor)
        );''',

        '''CREATE TABLE IF NOT EXISTS Ventas (
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            cliente_id INTEGER NOT NULL,
            total_obtenido REAL NOT NULL,
            FOREIGN KEY(cliente_id) REFERENCES Clientes(id_cliente)
        );''',

        '''CREATE TABLE IF NOT EXISTS Detalle_Ventas (
            id_detalle_venta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venta INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitariol REAL NOT NULL,
            sub_total REAL NOT NULL,
            FOREIGN KEY(id_venta) REFERENCES Ventas(id_venta),
            FOREIGN KEY(id_producto) REFERENCES Productos(id_producto)
        );''',

        '''CREATE TABLE IF NOT EXISTS Compras (
            id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            proveedor_id INTEGER,
            total_gastado REAL,
            FOREIGN KEY(proveedor_id) REFERENCES Proveedores(id_proveedor)
        );''',

        '''CREATE TABLE IF NOT EXISTS Detalle_Compra (
            id_detalle_compra INTEGER PRIMARY KEY AUTOINCREMENT,
            id_compra INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            sub_total REAL NOT NULL,
            FOREIGN KEY(id_compra) REFERENCES Compras(id_compra),
            FOREIGN KEY(id_producto) REFERENCES Productos(id_producto)
        );''',

        '''CREATE TABLE IF NOT EXISTS Finanzas (
            id_finanza INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL CHECK(tipo IN ('Ingreso', 'Egreso')),
            fecha TEXT NOT NULL,
            monto REAL NOT NULL,
            descripcion TEXT,
            id_venta INTEGER,
            id_compra INTEGER,
            FOREIGN KEY(id_venta) REFERENCES Ventas(id_venta),
            FOREIGN KEY(id_compra) REFERENCES Compras(id_compra)
        );''',

        '''CREATE TABLE IF NOT EXISTS Inventario (
            id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto INTEGER NOT NULL,
            tipo_movimiento TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY(id_producto) REFERENCES Productos(id_producto)
        );''',
        '''CREATE TABLE IF NOT EXISTS MovimientosFinancieros(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATE DEFAULT CURRENT_DATE,
            tipo TEXT CHECK(tipo IN('INGRESO', 'EGRESO')),
            monto REAL NOT NULL,
            descripcion TEXT
        );'''
    ]

    for sql in tablas:
        cursor.execute(sql)

    conexion.commit()
    conexion.close()
