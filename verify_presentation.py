import pptx
from pptx.enum.shapes import MSO_SHAPE_TYPE

prs = pptx.Presentation('ppt/Project_Review2-PPT_template.pptx')
print(f"Total slides: {len(prs.slides)}")

with open('ppt/verify_updated_slides.txt', 'w', encoding='utf-8') as f:
    for idx, s in enumerate(prs.slides):
        f.write(f"\n==================== SLIDE {idx+1} ====================\n")
        f.write(f"Layout: {s.slide_layout.name}\n")
        for sh in s.shapes:
            sh_type = str(sh.shape_type)
            f.write(f"--- Shape: '{sh.name}' ({sh_type}) ---\n")
            f.write(f"    Left={sh.left/914400:.2f}\", Top={sh.top/914400:.2f}\", Width={sh.width/914400:.2f}\", Height={sh.height/914400:.2f}\"\n")
            if sh.has_text_frame:
                f.write(f"    Text ({len(sh.text_frame.paragraphs)} paragraphs):\n")
                for p in sh.text_frame.paragraphs:
                    if p.text.strip():
                        f.write(f"      • {p.text}\n")
            elif sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
                f.write(f"    [PICTURE]: {sh.image.filename if hasattr(sh.image, 'filename') else 'image'}\n")

print("Verification written to ppt/verify_updated_slides.txt")
