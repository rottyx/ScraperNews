
from playwright.sync_api import sync_playwright
import json
from datetime import date

def get_attr(elem, attrs):
    for a in attrs:
        v = elem.get_attribute(a)
        if v:
            return v.split()[0]
    return None

def scrape_source(name, url, container_selector, max_items=5):
    items = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=60000)

            blocks = page.query_selector_all(container_selector)
            for block in blocks:
                if len(items) >= max_items:
                    break

                title = None
                for sel in ["h2", "h3", "a[title]", "a span"]:
                    el = block.query_selector(sel)
                    if el:
                        try:
                            t = el.inner_text().strip()
                            if t:
                                title = t
                                break
                        except:
                            continue

                if not title:
                    continue

                href_el = block.query_selector("a[href]")
                link = href_el.get_attribute("href") if href_el else url
                if link and link.startswith("/"):
                    link = url.rstrip("/") + link

                img = None
                for img_sel in ["img", "picture img", "source"]:
                    img_el = block.query_selector(img_sel)
                    if img_el:
                        img = get_attr(img_el, ["src", "data-src", "srcset"])
                        if img:
                            break

                items.append({"title": title, "link": link, "image": img})

            browser.close()
    except Exception as e:
        items = [{"title": f"ERROR: {e}", "link": url, "image": None}]

    return {"name": name, "url": url, "headlines": items}

def main():
    today = date.today().isoformat()
    sources = [
        ("El País", "https://elpais.com", "article"),
        ("El Mundo", "https://www.elmundo.es", ".ue-c-cover-content, article"),
        ("ABC", "https://www.abc.es", "article"),
        ("La Vanguardia", "https://www.lavanguardia.com", "article, div.lvd-noticia"),
        ("El Confidencial", "https://www.elconfidencial.com", "article")
    ]

    data = {"date": today, "sources": []}
    for name, url, sel in sources:
        data["sources"].append(scrape_source(name, url, sel))

    with open("final_news.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
