import json
import os
import openai
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_image_from_summary(summary):
    prompt = f"{summary}. Estilo cómic, portada de periódico, colores vivos, narrativa visual clara"
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        print(f"Error generando imagen: {e}")
        return None

def main():
    with open("final_summarized.json", encoding="utf-8") as f:
        data = json.load(f)

    enriched = []
    for item in tqdm(data, desc="Generando imágenes estilo cómic"):
        summary = item.get("summary")
        if not summary:
            continue

        image_url = generate_image_from_summary(summary)
        if image_url:
            item["image_url"] = image_url
            item["image_generated"] = True
            enriched.append(item)
        else:
            print("⚠️ Imagen no generada.")

    with open("final_summarized_with_images.json", "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
