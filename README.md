# Práctica de Aula: AlumnosCRUD con FastAPI

Este proyecto es una API REST para la gestión de alumnos, desarrollada con FastAPI. A lo largo de la práctica, la aplicación ha evolucionado desde una ejecución local simple hasta su despliegue en la nube con contenedores.

🔗 **Repositorio:** [GitHub - AlumnosCRUD-FASTAPI](https://github.com/GNicolas21/AlumnosCRUD-FASTAPI)

---

### Puntos 1 y 2: Rutas y Formularios
Implementación de las rutas básicas y formularios HTML para la creación y visualización de alumnos.

* **Commit:** `24bc6f596101de41f7be1d9c26e7846994801616`
* **Ejecución:**
    1. Levantar entorno con Docker Compose.
    2. Activar entorno virtual: `.\.venv\Scripts\Activate.ps1`
    3. Lanzar aplicación:
       ```bash
       uvicorn src.main:app --reload
       ```
    4. Verificación: Mensaje `Application startup complete`.

<p align="center">
  <img src="Practica python 1.jpg" width="600">
</p>

---

### Punto 3: Dockerización con MySQL
Separación de servicios en contenedores: uno para la base de datos MySQL y otro para la aplicación FastAPI.

* **Commit:** `b3795a5d4d4db65a67745da9a49c3c88de22acf8`
* **Ejecución:**
    ```bash
    docker compose build fastapi-app
    docker compose up
    ```
* **Resultado:** Endpoints respondiendo con código `200 OK`.
<p align="center">
  <img src="Practica python 2.jpg" width="600">
</p>

---

### Punto 4: Migración a PostgreSQL (Rama PostgreSQL)
Cambio del Sistema Gestor de Base de Datos a PostgreSQL (imagen:15) y mejoras en la interfaz.

* **Commit:** `57ceda77fd7050f8c336e696c306b03d42b19eac`
* **Configuración:**
    * Puerto actualizado a `5432`.
    * Variables de entorno actualizadas en `.env` (DB_URL).
    * Eliminación de `MYSQL_ROOT_PASSWORD` (innecesaria en Postgres).
* **Estilos:** Se añadieron estilos Bootstrap (asistencia mediante IA Claude Sonnet 4).
* **Ejecución:**
    ```bash
    docker compose up --build -d
    ```

---

### Punto 5: Despliegue en Render (Estado Actual)
Despliegue de la aplicación en producción utilizando la plataforma Render.
Deberías poder ver la página web en el siguiente enlace:
**[https://alumnoscrud-fastapi.onrender.com/alumnos](https://alumnoscrud-fastapi.onrender.com/alumnos)**

* **Estado:** Disponible en el último commit.
* **Configuración:**
    * Creación de servicio **PostgreSQL** en Render.
    * Configuración de variables de entorno (`DATABASE_URL`) para conectar la API con la base de datos en la nube.
    * Corrección del prefijo de conexión para compatibilidad con SQLAlchemy (`postgresql://`).

<p align="center">
  <img src="Practica python 3.jpg" width="600">
</p>