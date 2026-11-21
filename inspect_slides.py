import json

with open('ppt/slide_dump.json', 'r', encoding='utf-8') as f:
    slides = json.load(f)

with open('ppt/slide_summary.txt', 'w', encoding='utf-8') as out:
    for s in slides:
        out.write(f"\n==================== SLIDE {s['slide_num']} ====================\n")
        for sh in s['shapes']:
            if 'text' in sh and sh['text'].strip():
                out.write(f"--- [Text Shape {sh['id']} - {sh['name']}] ---\n")
                for line in sh['text'].split('\n'):
                    if line.strip():
                        out.write(f"  {line.strip()}\n")
            elif 'table' in sh:
                out.write(f"--- [Table Shape {sh['id']} - {sh['name']}] ---\n")
                for r_idx, row in enumerate(sh['table']):
                    out.write("  | " + " | ".join(c.replace('\n', ' ') for c in row) + " |\n")

