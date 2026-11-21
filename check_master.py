import pptx

prs = pptx.Presentation('ppt/Project_Review2-PPT_template.pptx')
print(f"Total slides: {len(prs.slides)}")
print(f"Total slide masters: {len(prs.slide_masters)}")
for m_idx, master in enumerate(prs.slide_masters):
    print(f"Master {m_idx}: {len(master.shapes)} shapes")
    for s in master.shapes:
        print(f"   Master shape: {s.name}, type={s.shape_type}")

for idx, slide in enumerate(prs.slides):
    img_count = sum(1 for s in slide.shapes if s.shape_type == pptx.enum.shapes.MSO_SHAPE.PICTURE)
    print(f"Slide {idx+1}: {len(slide.shapes)} shapes, {img_count} images, Layout: {slide.slide_layout.name}")
