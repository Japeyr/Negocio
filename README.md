
# 🛒 Sistema de Gestión de un Negocio

Este proyecto realiza la gestión de un negocio. Se realizan Alta, Baja, Modificación y Lectura de Productos, Clienes y Proveedores. También maneja Stocks de Productos, permite ver los Movimientos de Inventario, realizar el Ajuste Manual del mismo y Ver el Stock Actual por Productos. En cuanto la Area de Finanzas, permite Registrar Movimientos Financieros, Ver un Resumen Financiero y Resultado Económico.

---

## 📌 Tecnologías y Librerías utilizadas

Este proyecto utiliza las siguientes librerías de **Python**🐍:

- **TKinter** 💻 → Para visualización del Sistema  
- **sqlite3** 💾 → Para el manejo de la base de datos **SQLite**  
- **tkcalendar** 📅 → Para la visualización y manejo de fechas  

---

## 🚀 Instalación y Configuración

**1️⃣ Instalar en su PC el Browser SQLite**

Descarguelo de Aquí:
[Descarga](https://sqlitebrowser.org/dl/)

**2️⃣ Clonar el repositorio**

```bash
git clone https://github.com/Japeyr/Negocio/Negocio.git
cd Negocio
```

**3️⃣ Instalar dependencias:**

```bash
pip install sqlite3 tkinter tkcalendar

**4️⃣ Ejecutar el script:**

```bash
python Sistema_Gestion.py
```

**5️⃣ Una vez que ejecute el Sistema haga click en Crear Base de Datos ***

---

## 📂 Estructura de archivos

- `Sistema_Gestion.py` → Script principal del Sistema
- `ConexionSQLite.py` → Script de conexión de Base de Datos
- `ListaProductos.py` → Script para productos
- `ListaProveedores.py` → Script para proveedores
- `ListaClientes.py` → Script para clientes
- `OperacionCompra.py` → Script para compras
- `OperacionVenta.py` → Script para ventas
- `Stock.py` → Script manejar el inventario
- `Finanzas.py` → Script para finanzas y resultados 
- `README.md` → Documentación del proyecto  

---

## ⚡ Uso del script

Ejecutá el script con:

```bash
python SistemaGestion.py
```

Verá un menú de operaciones. Allí se indica los pasos a seguir. Luego hay que ingresar el Capital de trabajo como un Ingreso en Finanzas.
Después dar de alta productos, proveedores y clientes para después realizar operaciones de compra y venta de productos.
