#  GOTTI Store - API E-commerce

API REST de comercio electrónico desarrollada con Django REST Framework.

##  Descripción

GOTTI Store es una plataforma de e-commerce completa que incluye gestión de productos con variantes, carrito de compras, órdenes, pagos con tarjeta de crédito/débito, reseñas, cupones de descuento y generación de facturas en PDF.

##  Tecnologías utilizadas

- Python 3.12
- Django 5.2
- Django REST Framework
- SQLite
- ReportLab (PDF)

##  Estructura del proyecto

##  Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/Tiagolopezbit/Trabajo-Practico-TL.git
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Aplicar migraciones:
```bash
cd gotti_backend
python manage.py migrate
```

4. Ejecutar el servidor:
```bash
python manage.py runserver
```

5. Abrir en el navegador:


##  Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | /api/auth/registro/ | Registro de usuario |
| POST | /api/auth/login/ | Login de usuario |
| GET | /api/productos/ | Listar productos |
| POST | /api/productos/ | Crear producto |
| GET | /api/productos/{id}/ | Detalle de producto |
| PUT | /api/productos/{id}/ | Actualizar producto |
| DELETE | /api/productos/{id}/ | Eliminar producto |
| GET | /api/carrito/ | Ver carrito |
| POST | /api/carrito/agregar/ | Agregar al carrito |
| DELETE | /api/carrito/{id}/ | Quitar del carrito |
| GET | /api/ordenes/ | Listar órdenes |
| POST | /api/ordenes/ | Crear orden |
| POST | /api/ordenes/pagos/{id}/ | Procesar pago |
| GET | /api/ordenes/facturas/{id}/ | Descargar factura PDF |
| GET | /api/cupones/{codigo}/ | Validar cupón |

##  Métodos de pago

- Tarjeta de crédito
- Tarjeta de débito

##  Autor

Tiago Lopez - [@Tiagolopezbit](https://github.com/Tiagolopezbit)