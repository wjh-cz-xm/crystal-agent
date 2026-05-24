"""
从 Wikipedia API 获取晶体学词条补充知识库
"""
import wikipediaapi
import json
import os
import time

KB_DIR = os.path.dirname(os.path.abspath(__file__))

# 要抓取的 Wikipedia 词条（英文）
topics_en = [
    "Crystal_structure",
    "Bravais_lattice",
    "Miller_index",
    "Bragg's_law",
    "Reciprocal_lattice",
    "X-ray_crystallography",
    "Space_group",
    "Point_group",
    "Crystal_system",
    "Close-packing_of_equal_spheres",
    "Crystallographic_defect",
    "Dislocation",
    "Brillouin_zone",
    "Electronic_band_structure",
    "Bloch's_theorem",
    "Diamond_cubic",
    "Sodium_chloride_(structure)",
    "Caesium_chloride_(structure)",
    "Zincblende_(crystal_structure)",
    "Perovskite_(structure)",
    "Wurtzite_crystal_structure",
]

# 要抓取的 Wikipedia 词条（中文）
topics_zh = [
    "晶体结构",
    "布拉维晶格",
    "米勒指数",
    "布拉格定律",
    "倒易点阵",
    "X射线晶体学",
    "空间群",
    "点群",
    "晶系",
    "最密堆积",
]

def fetch_wiki_articles(lang, topics):
    """Fetch Wikipedia articles"""
    wiki = wikipediaapi.Wikipedia(
        language=lang,
        user_agent="CrystalKB/1.0 (educational project; contact@example.com)",
        extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    results = {}
    for topic in topics:
        try:
            page = wiki.page(topic)
            if page.exists():
                # Get summary (first ~500 chars) and full text
                results[topic] = {
                    "title": page.title,
                    "summary": page.summary[:800],
                    "url": page.fullurl,
                }
                print(f"  OK: {topic} ({lang})")
            else:
                print(f"  NOT FOUND: {topic} ({lang})")
        except Exception as e:
            print(f"  ERROR: {topic} ({lang}): {e}")
        time.sleep(0.3)  # Rate limiting

    return results

if __name__ == "__main__":
    print("Fetching English Wikipedia articles...")
    en_results = fetch_wiki_articles("en", topics_en)

    print(f"\nFetched {len(en_results)} English articles")

    # Save results
    output_path = os.path.join(KB_DIR, "wiki_raw.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(en_results, f, ensure_ascii=False, indent=2)

    print(f"Saved to {output_path}")

    print("\nFetching Chinese Wikipedia articles...")
    zh_results = fetch_wiki_articles("zh", topics_zh)

    print(f"\nFetched {len(zh_results)} Chinese articles")

    # Merge and save
    all_results = {"en": en_results, "zh": zh_results}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"All saved to {output_path}")
    print(f"Total: {len(en_results)} EN + {len(zh_results)} ZH")
