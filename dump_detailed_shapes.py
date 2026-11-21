import sys
import pptx
from pptx.util import Inches, Pt

prs = pptx.Presentation('ppt/Project_Review2-PPT_template.pptx')

with open('ppt/detailed_shapes_dump.txt', 'w', encoding='utf-8') as f:
    f.write(f"Slide width: {prs.slide_width}, height: {prs.slide_height}\n")
    f.write(f"Inches: {prs.slide_width / 914400:.2f} x {prs.slide_height / 914400:.2f}\n\n")
    for idx, slide in enumerate(prs.slides):
        f.write(f"==================== SLIDE {idx+1} (Layout: {slide.slide_layout.name}) ====================\n")
        for s_idx, shape in enumerate(slide.shapes):
            f.write(f"Shape {s_idx}: Name='{shape.name}', Type={shape.shape_type}\n")
            f.write(f"  Pos: Left={shape.left} ({shape.left/914400:.2f}in), Top={shape.top} ({shape.top/914400:.2f}in), Width={shape.width} ({shape.width/914400:.2f}in), Height={shape.height} ({shape.height/914400:.2f}in)\n")
            if shape.has_text_frame:
                tf = shape.text_frame
                f.write(f"  TextFrame: word_wrap={tf.word_wrap}, margin_l={tf.margin_left}, margin_t={tf.margin_top}\n")
                for p_idx, p in enumerate(tf.paragraphs):
                    runs_info = []
                    for r in p.runs:
                        font_name = r.font.name if r.font else None
                        font_size = r.font.size.pt if (r.font and r.font.size) else None
                        bold = r.font.bold if r.font else None
                        runs_info.append(f"['{r.text}', {font_name}, {font_size}pt, bold={bold}]")
                    f.write(f"    P{p_idx} (level={p.level}): '{p.text}' | Runs: {', '.join(runs_info)}\n")
            elif shape.has_table:
                f.write(f"  Table: {len(shape.table.rows)} rows x {len(shape.table.columns)} cols\n")
                for r_idx, row in enumerate(shape.table.rows):
                    row_txt = [c.text.replace('\n', ' ') for c in row.cells]
                    f.write(f"    R{r_idx}: {' | '.join(row_txt)}\n")
            else:
                f.write(f"  Other shape: {shape.shape_type}\n")
            f.write("\n")
print("Detailed dump completed.")
