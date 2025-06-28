# ScraperNews

**ScraperNews** es una herramienta que genera una portada diaria de noticias relevantes de los principales peri��dicos espa?oles. Extrae, resume y agrupa titulares similares, y los ilustra con im��genes generadas al estilo c��mic.

## Flujo de trabajo

1. **Scraping (`main.py`)**  
   Extrae titulares de El Pa��s, El Mundo, ABC, La Vanguardia y El Confidencial. Guarda los resultados en `final_news.json`.

2. **Resumen y deduplicaci��n (`summarizer.py`)**  
   Usa GPT-4 para resumir cada titular y fusionar los que tratan sobre el mismo tema. Guarda los resultados en `final_summarized.json`.

3. **Generaci��n de im��genes (`generate_images.py`)**  
   Genera ilustraciones al estilo c��mic con DALL-E para los res��menes sintetizados. Guarda los resultados exitosos en `final_summarized_with_images.json`.

4. **Visualizaci��n (`index.html`)**  
   Muestra la portada del d��a con los res��menes y sus ilustraciones en un grid atractivo.

## Requisitos

```bash
pip install -r requirements.txt
playwright install
```

> Recuerda ejecutar `playwright install` despu��s de instalar las dependencias. Esto descargar�� los navegadores necesarios para que `main.py` funcione correctamente.
> Recuerda crear un archivo .env en el directorio y guardar tu apikey: OPENAI_API_KEY=skXXXXXXX...

## Notas adicionales

- Este proyecto **podr��a automatizarse** para ejecutarse diariamente (por ejemplo con un cron job), y as�� generar una portada diaria de forma continua.
- **Sin embargo, no se ha implementado dicha automatizaci��n** deliberadamente, ya que los res��menes, las comparaciones sem��nticas y la generaci��n de im��genes usan la API de OpenAI y consumen una cantidad considerable de tokens.
- Prefiero mantener el control manual del proceso y lanzar el flujo solo cuando lo necesite.

## Visualizaci��n

Una vez generados los datos, puedes abrir `index.html` en tu navegador y ver una portada bajo el t��tulo: **ScraperNews**.

---

 2025 Proyecto personal creado para explorar scraping, s��ntesis sem��ntica e ilustraci��n autom��tica.

## Sugerencia: script de ejecuci��n manual

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

Esto puede facilitar la ejecuci��n del flujo completo sin depender de automatizaciones complejas.

## C��mo ver la portada en tu navegador

Para evitar errores al cargar el archivo `final_summarized_with_images.json`, **no abras `index.html` con doble clic** (lo que lanza una URL `file://`).  
Esto puede causar que el navegador bloquee el acceso al archivo JSON por razones de seguridad.

En su lugar, abre un servidor local desde la terminal:

```bash
python -m http.server 8000
```

Luego abre tu navegador en esta direcci��n:

 [http://localhost:8000/index.html](http://localhost:8000/index.html)

Esto permitir�� que `fetch()` funcione correctamente y las noticias se carguen sin problema.