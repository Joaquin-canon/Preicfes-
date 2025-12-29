# 📘 PreICFES

Plataforma web para la **preparación del examen ICFES** desarrollada con **FastAPI**, enfocada en estudiantes, tests diagnósticos y un roadmap de aprendizaje por áreas.

---

## 🚀 Tecnologías utilizadas

* **Python 3.10+**
* **FastAPI**
* **Uvicorn**
* **Jinja2** (templates HTML)
* **HTML / CSS / JavaScript**
* **MySQL** (planeado / en integración)

---

## 📂 Estructura del proyecto

```
preicfes/
├── app/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── config.py            # Configuración general
│   ├── database.py          # Conexión a base de datos
│   ├── routers/             # Rutas (endpoints)
│   ├── services/            # Lógica de negocio
│   ├── models/              # Modelos de base de datos
│   ├── schemas/             # Esquemas Pydantic
│   ├── static/              # Archivos estáticos (CSS, JS)
│   └── templates/           # Templates HTML (Jinja2)
├── venv/                    # Entorno virtual (NO se sube a GitHub)
├── .gitignore
└── README.md
```

---

## ⚙️ Instalación y configuración

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Joaquin-canon/Preicfes.git
cd preicfes
```

### 2️⃣ Crear y activar entorno virtual

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux / Mac
```

### 3️⃣ Instalar dependencias

Si existe `requirements.txt`:

```bash
pip install -r requirements.txt
```

Si no existe:

```bash
pip install fastapi uvicorn jinja2 python-multipart
```

---

## ▶️ Ejecutar el proyecto

Desde la carpeta raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

Abrir en el navegador:

```
http://127.0.0.1:8000
```

---

## 🧭 Funcionalidades actuales

* ✅ Sistema de vistas con FastAPI + Jinja2
* ✅ Vista de estudiantes
* ✅ Test diagnóstico
* 🚧 Roadmap de aprendizaje (en desarrollo)
* 🚧 Sistema de progreso por áreas ICFES

---

## 📌 Convenciones importantes

* El entorno virtual **`venv/` nunca se sube a GitHub**
* Los archivos HTML deben ir **solo en `templates/`**
* Los archivos CSS y JS deben ir **solo en `static/`**
* El proyecto se ejecuta siempre con:

```bash
uvicorn app.main:app --reload
```

---

## 🛠️ Próximas mejoras

* 📊 Radar de progreso por áreas ICFES
* 🔐 Autenticación de usuarios
* 🧠 Recomendaciones personalizadas
* 📈 Seguimiento de resultados

---

## 👨‍💻 Autor

**Joaquín Canon**
Proyecto académico y educativo

---

## 📄 Licencia

Este proyecto es de uso académico y educativo.
