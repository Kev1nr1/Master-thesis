"""
generate_lda_html.py

Reads lda_topics_all.txt and generates one HTML file per category,
styled to match the real_estate.html template.

Usage:
    python generate_lda_html.py
    python generate_lda_html.py --input lda_topics_all.txt --output_dir ./html_output
"""

import re
import os
import argparse


# ── HTML template ────────────────────────────────────────────────────────────

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@400;500&display=swap');

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: #f5f0e8;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 24px;
    font-family: 'Inter', sans-serif;
  }}

  .card {{
    background: #faf6ed;
    border: 2.5px solid #c9a84c;
    border-radius: 22px;
    padding: 36px 32px 32px;
    width: 540px;
    box-shadow: 0 4px 24px rgba(180,140,40,0.10);
  }}

  h1 {{
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    color: #2b2200;
    text-align: center;
    line-height: 1.2;
    margin-bottom: 8px;
  }}

  .meta {{
    text-align: center;
    color: #b8860b;
    font-size: 13.5px;
    font-weight: 500;
    margin-bottom: 20px;
    letter-spacing: 0.01em;
  }}

  .divider {{
    border: none;
    border-top: 1.5px solid #d4b96a;
    margin-bottom: 22px;
  }}

  .topic-row {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin-bottom: 16px;
  }}

  .topic-num {{
    background: #f5e6b2;
    border: 1.5px solid #c9a84c;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    color: #7a5c00;
    width: 40px;
    min-width: 40px;
    height: 34px;
    display: flex;
    align-items: center;
    justify-content: center;
    letter-spacing: 0.04em;
  }}

  .tags {{
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
    align-items: center;
  }}

  .tag {{
    background: #faf6ed;
    border: 1.5px solid #c9a84c;
    border-radius: 20px;
    padding: 5px 13px;
    font-size: 13px;
    color: #2b2200;
    white-space: nowrap;
  }}
</style>
</head>
<body>
<div class="card">
  <h1>{title}</h1>
  <div class="meta">Coherence: {coherence}&nbsp;&nbsp;Diversity: {diversity}</div>
  <hr class="divider">

{topic_rows}
</div>
</body>
</html>
"""

TOPIC_ROW_TEMPLATE = """\
  <div class="topic-row">
    <div class="topic-num">{num:02d}</div>
    <div class="tags">
{tags}
    </div>
  </div>"""

TAG_TEMPLATE = '      <span class="tag">{word}</span>'


# ── Parser ────────────────────────────────────────────────────────────────────

def parse_txt(path: str) -> list[dict]:
    """
    Parse the LDA topics txt file into a list of category dicts:
      {
        'category': str,
        'coherence': str,
        'diversity': str,
        'topics': [[word, ...], ...]   # list of topics, each a list of words
      }
    """
    with open(path, encoding="utf-8") as f:
        content = f.read()

    # Split on the separator line (at least 10 dashes)
    blocks = re.split(r"-{10,}", content)

    categories = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Category name
        cat_match = re.search(r"Category:\s*(.+)", block)
        if not cat_match:
            continue
        category = cat_match.group(1).strip()

        # Best config line — extract coherence and diversity
        config_match = re.search(
            r"coherence=([\d.]+),\s*diversity=\s*([\d.]+)", block
        )
        coherence = config_match.group(1) if config_match else "N/A"
        diversity = config_match.group(2) if config_match else "N/A"

        # Topic lines: "Topic NN: word1, word2, ..."
        topics = []
        for topic_match in re.finditer(r"Topic \d+:\s*(.+)", block):
            words = [w.strip() for w in topic_match.group(1).split(",") if w.strip()]
            topics.append(words)

        categories.append({
            "category": category,
            "coherence": coherence,
            "diversity": diversity,
            "topics": topics,
        })

    return categories


# ── HTML builder ──────────────────────────────────────────────────────────────

def build_html(category_data: dict) -> str:
    topic_rows_html = []
    for i, words in enumerate(category_data["topics"], start=1):
        tags_html = "\n".join(TAG_TEMPLATE.format(word=w) for w in words[:5])
        topic_rows_html.append(
            TOPIC_ROW_TEMPLATE.format(num=i, tags=tags_html)
        )

    return HTML_TEMPLATE.format(
        title=category_data["category"],
        coherence=category_data["coherence"],
        diversity=category_data["diversity"],
        topic_rows="\n".join(topic_rows_html),
    )


def safe_filename(name: str) -> str:
    """Convert a category name to a safe filename."""
    return re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_").lower() + ".html"


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate HTML cards from LDA topics txt.")
    parser.add_argument("--input", default="lda_topics_all_IoT.txt", help="Path to the LDA txt file")
    parser.add_argument("--output_dir", default="html", help="Directory to write HTML files into")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    categories = parse_txt(args.input)
    if not categories:
        print("No categories found — check the input file format.")
        return

    for cat in categories:
        html = build_html(cat)
        filename = safe_filename(cat["category"])
        out_path = os.path.join(args.output_dir, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Written: {out_path}  (k={len(cat['topics'])} topics, coherence={cat['coherence']}, diversity={cat['diversity']})")

    print(f"\nDone — {len(categories)} file(s) generated in '{args.output_dir}'.")


if __name__ == "__main__":
    main()
