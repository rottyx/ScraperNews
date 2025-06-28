# 📰 ScraperNews

**ScraperNews** es una herramienta que genera una portada diaria de noticias relevantes de los principales periódicos españoles. Extrae, resume y agrupa titulares similares, y los ilustra con imágenes generadas al estilo cómic.

## 🚀 Flujo de trabajo

1. **Scraping (`main.py`)**  
   Extrae titulares de El País, El Mundo, ABC, La Vanguardia y El Confidencial. Guarda los resultados en `final_news.json`.

2. **Resumen y deduplicación (`summarizer.py`)**  
   Usa GPT-4 para resumir cada titular y fusionar los que tratan sobre el mismo tema. Guarda los resultados en `final_summarized.json`.

3. **Generación de imágenes (`generate_images.py`)**  
   Genera ilustraciones al estilo cómic con DALL·E para los resúmenes sintetizados. Guarda los resultados exitosos en `final_summarized_with_images.json`.

4. **Visualización (`index.html`)**  
   Muestra la portada del día con los resúmenes y sus ilustraciones en un grid atractivo.

## 🔧 Requisitos

```bash
pip install -r requirements.txt
playwright install
```

> ⚠️ Recuerda ejecutar `playwright install` después de instalar las dependencias. Esto descargará los navegadores necesarios para que `main.py` funcione correctamente.

> ⚠️Recuerda crear un archivo .env en el directorio y guardar tu apikey: OPENAI_API_KEY=skXXXXXXX...

## 🧠 Notas adicionales

- Este proyecto **podría automatizarse** para ejecutarse diariamente (por ejemplo con un cron job), y así generar una portada diaria de forma continua.
- **Sin embargo, no se ha implementado dicha automatización** deliberadamente, ya que los resúmenes y comparaciones semánticas usan la API de OpenAI y consumen una cantidad considerable de tokens.
- Prefiero mantener el control manual del proceso y lanzar el flujo solo cuando lo necesite.

## 🌐 Visualización

Una vez generados los datos, puedes abrir `index.html` en tu navegador y ver una portada bajo el título: **ScraperNews**.

---

© 2025 �?Proyecto personal creado para explorar scraping, síntesis semántica e ilustración automática.

## 🖱�?Sugerencia: script de ejecución manual

Si prefieres ejecutar todo con un solo comando manual, puedes crear un archivo `.bat` (Windows) o `.sh` (Linux/Mac) con el siguiente contenido:

**Windows (`run.bat`)**:
```bat
@echo off
python main.py
python summarizer.py
python generate_images.py
pause
```

**Linux/Mac (`run.sh`)**:
```bash
#!/bin/bash
python main.py
python summarizer.py
python generate_images.py
```

Esto puede facilitar la ejecución del flujo completo sin depender de automatizaciones complejas.

## 🌍 Cómo ver la portada en tu navegador

Para evitar errores al cargar el archivo `final_summarized_with_images.json`, **no abras `index.html` con doble clic** (lo que lanza una URL `file://`).  
Esto puede causar que el navegador bloquee el acceso al archivo JSON por razones de seguridad.

En su lugar, abre un servidor local desde la terminal:

```bash
python -m http.server 8000
```

Luego abre tu navegador en esta dirección:

👉 [http://localhost:8000/index.html](http://localhost:8000/index.html)

Esto permitirá que `fetch()` funcione correctamente y las noticias se carguen sin problema.