import pptx
from pptx.enum.shapes import MSO_SHAPE

prs = pptx.Presentation('ppt/Project_Review2-PPT_template.pptx')

with open('ppt/slides_detailed_analysis.txt', 'w', encoding='utf-8') as f:
    for s_idx, slide in enumerate(prs.slides):
        f.write(f"\n=================================================================\n")
        f.write(f"SLIDE {s_idx + 1}: Layout='{slide.slide_layout.name}'\n")
        f.write(f"=================================================================\n")
        for sh_idx, shape in enumerate(slide.shapes):
            f.write(f"\n--- Shape [{sh_idx}]: '{shape.name}' (Type: {shape.shape_type}) ---\n")
            f.write(f"    Left: {shape.left/914400:.2f}\", Top: {shape.top/914400:.2f}\", Width: {shape.width/914400:.2f}\", Height: {shape.height/914400:.2f}\"\n")
            
            # Check shape fill
            try:
                fill = shape.fill
                f.write(f"    Fill type: {fill.type}\n")
            except Exception:
                pass
            
            # Text Frame details
            if shape.has_text_frame:
                tf = shape.text_frame
                f.write(f"    TextFrame has {len(tf.paragraphs)} paragraphs:\n")
                for p_idx, p in enumerate(tf.paragraphs):
                    p_fonts = []
                    for r in p.runs:
                        font_str = f"'{r.text}' (Font: {r.font.name}, Size: {r.font.size.pt if r.font.size else 'None'}pt, Bold: {r.font.bold}, Color: {r.font.color.rgb if (r.font.color and hasattr(r.font.color, 'rgb') and r.font.color.type == 1) else 'None'})"
                        p_fonts.append(font_str)
                    f.write(f"      P[{p_idx}] (level={p.level}, align={p.alignment}): '{p.text}'\n")
                    if p_fonts:
                        f.write(f"          Runs: {p_fonts}\n")
            elif shape.has_table:
                f.write(f"    Table: {len(shape.table.rows)} rows x {len(shape.table.columns)} cols\n")
