import json
import openai
import os
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un experto en medios. Resume esta noticia de forma clara, breve y objetiva."},
                {"role": "user", "content": text}
            ],
            temperature=0.5,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error en resumen: {e}")
        return text

def thematic_similarity(t1, t2):
    try:
        prompt = f"¿Estas dos frases hablan de lo mismo? Devuelve solo 'sí' o 'no'.\n1: {t1}\n2: {t2}"
        resp = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=5
        )
        answer = resp.choices[0].message.content.strip().lower()
        return "sí" in answer
    except Exception as e:
        print(f"Error comparando temas: {e}")
        return False

def main():
    with open("final_news.json", encoding="utf-8") as f:
        full_data = json.load(f)

    all_entries = []
    for source in full_data["sources"]:
        for item in source["headlines"]:
            all_entries.append({
                "title": item["title"],
                "link": item["link"],
                "image_url": item["image"],
                "sources": [source["name"]]
            })

    summarized = []
    for item in tqdm(all_entries, desc="Resumiendo titulares"):
        summary = summarize_text(item["title"])
        item["summary"] = summary
        summarized.append(item)

    deduped = []
    for entry in tqdm(summarized, desc="Fusionando similares"):
        matched = False
        for d in deduped:
            if thematic_similarity(entry["summary"], d["summary"]):
                d["sources"] = list(set(d["sources"] + entry["sources"]))
                d["links"].append(entry["link"])
                matched = True
                break
        if not matched:
            deduped.append({
                "summary": entry["summary"],
                "image_url": entry["image_url"],
                "sources": entry["sources"],
                "links": [entry["link"]]
            })

    with open("final_summarized.json", "w", encoding="utf-8") as f:
        json.dump(deduped, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
