# Servidor Backend de Descarga de Música y Video (yt-dlp + Python Flask)

Este servidor backend procesa cualquier enlace de **YouTube** o **YouTube Music** usando la librería oficial **`yt-dlp`** (la misma que usan los conversores web) y le devuelve el enlace de descarga MP3 o MP4 a tu aplicación de Android.

---

## 🚀 Despliegue Gratuito en Render.com (Paso a Paso en 3 Minutos)

### Paso 1: Subir la carpeta `backend` a GitHub
1. Crea un repositorio nuevo en GitHub (ejemplo: `mi-servidor-descargador`).
2. Sube los archivos de la carpeta `backend/`:
   - `app.py`
   - `requirements.txt`
   - `Procfile`

### Paso 2: Crear el Web Service en Render
1. Entra a [Render.com](https://render.com) y crea una cuenta gratuita.
2. Haz clic en **New +** > **Web Service**.
3. Conecta tu repositorio de GitHub recién creado.
4. Completa la configuración:
   - **Name**: `mi-servidor-musica` (o el nombre que gustes)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Haz clic en **Create Web Service**.

### Paso 3: Copiar la URL de tu Servidor
Render te entregará una URL pública gratuita similar a:
`https://mi-servidor-musica.onrender.com`

---

## 📱 Conectar con tu App de Android Studio
Abre la clase `MediaExtractor.java` en tu proyecto de Android Studio e ingresa la URL de tu servidor en la variable `CUSTOM_BACKEND_URL`:

```java
private static final String CUSTOM_BACKEND_URL = "https://mi-servidor-musica.onrender.com/download";
```

¡Listo! Tu aplicación usará tu propio servidor backend con `yt-dlp` en la nube para convertir cualquier canción en 2 segundos.
