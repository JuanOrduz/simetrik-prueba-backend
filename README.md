# Prueba Backend Simetrik
El presente repositorio contiene la solución a la prueba técnica de Simetrik para desarrollador backend.

### Descripción
Tenemos la necesidad de poder subir archivos (.csv) al sistema de almacenamiento de
amazon web services (AWS S3) y crear una tabla en una base de datos externa
(diferente a la que usa el ORM de Django Framework) basada en el archivo, las
columnas de esta tabla deben corresponder al del archivo, y cuyos tipos de datos
pueden ser todos varchar o text, una vez subido, se debe leer el archivo
implementando ejecución por hilos para almacenar su información en la tabla creada.
Se debe garantizar que los datos guardados en las tablas creadas deben poder ser
consultados desde un endpoint, el cual, debe tener implementado paginación,
búsqueda por filtros y ordenamiento por columna.
Se debe implementar pruebas unitarias al sistema.

## Solucion
El backend se diseño con las siguientes caracteristicas:
* Dos bases de datos locales con sqlite.
* Modelo ORM para almacenamiento de archivos csv en AWS-S3 utilizando base de datos principal.
* SQLAlchemy para crear y almacenar informacion de archivos csv en base de datos secundaria a travez de un hilo secundario.
* Django REST Framework para consultar base de datos principal y secundaria.
* Endpoints de ejemplo utilizando extension rest de VSCode.
* Pruebas unitarias aisladas sin contacto con S3 o las bases de datos.

### Modelo principal
Se tiene un modelo de datos que utiliza el ORM de Django para almacenar en la base de datos principal la siguiente informacion:
* Nombre del archivo unico.
* Columnas del archivo utilizadas para ordenamiento o filtrado.
* Ruta de almacenamiento del archivo en S3.
* Fecha de creacion.

### Endpoints
Se tienen endpoints de ejemplo en la carpeta .rest, los cuales son los siguientes:
* **GET {{base_url}}/csv-manager/:** Listado de informacion general de los archivos csv almacenados en S3 y cuya informacion esta en la base de datos secundaria. Este endpoint cuenta con paginacion, ordenamiento (nombre y fecha de creacion) y filtros (nombre)
* **POST {{base_url}}/csv-manager/:** Lee archivo csv que es almacenado en S3 y cuya informacion basica se almacena en la base de datos principal. En un hilo secundario se crea una tabla basada en las columnas del archivo csv en la base de datos secundaria, ademas de almacenar los datos del archivo para cada columna.
* **GET {{base_url}}/csv-manager/{{csv_file_id}}:** Lee informacion de un unico archivo csv.
* **PATCH {{base_url}}/csv-manager/{{csv_file_id}}:** Modifica informacion de un unico archivo csv.
* **DELETE {{base_url}}/csv-manager/{{csv_file_id}}:** Soft delete de informacion de un unico archivo csv.
* **GET {{base_url}}/csv-manager/data/{{secondary_database_table}}/:** Lista datos de tabla de base de datos secundaria basada en archivo csv con el mismo nombre. Este endpoint cuenta con paginacion, ordenamiento y filtros por cualquier columna (Consultar las columnas del endpoint GET {{base_url}}/csv-manager/)

### Despliegue local
A continuacion se indican los prerequisitos, variables de entorno y pasos para desplegar el proyecto localmente.
#### Prerequisitos
Para desplegar el proyecto localmente se requiere:
* Cuenta AWS
* Crear bucket en S3
* Configurar bucket para que sea publico o con las políticas de acceso necesarias para que se pueda acceder desde el exterior.

#### Variables de entorno
Para que el proyecto funcione correctamente se requieren las siguientes variables de entorno:
* **AWS_STORAGE_BUCKET_NAME:** Nombre del bucket creado en S3.
* **AWS_ACCESS_KEY_ID:** AWS ACCESS KEY ID de cuenta AWS con acceso al bucket de S3.
* **AWS_SECRET_ACCESS_KEY:** AWS SECRET ACCESS KEY de cuenta AWS con acceso al bucket de S3.
* **SQLALCHEMY_DATABASE_URL:** URL de base de datos secundaria, por defecto se tiene una base de datos con sqlite llamada data_csv.db. Se puede configurar diferentes tipos de bases de datos, por ejemplo, "postgresql://user:password@postgresserver/db".

#### Despliegue
El siguiente despliegue es en un ambiente local Ubuntu 18.04
* Clonar el repositorio, crear ambiente virtual e instalar paquetes:
```
git clone https://github.com/JuanOrduz/simetrik-prueba-backend.git
cd simetrik-prueba-backend/
python -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
* Migración de la base de datos principal
```
python manage.py migrate
```
* Inician variables de entorno
```
export AWS_STORAGE_BUCKET_NAME=[AWS_STORAGE_BUCKET_NAME]
export AWS_ACCESS_KEY_ID=[AWS_ACCESS_KEY_ID]
export AWS_SECRET_ACCESS_KEY=[AWS_SECRET_ACCESS_KEY]
export SQLALCHEMY_DATABASE_URL=[SQLALCHEMY_DATABASE_URL]
```
* Inicia servidor local
```
python manage.py runserver
```

#### Pruebas
Para desplegar las pruebas unitarias se ejecuta el siguiente comando
```
pytest
```
