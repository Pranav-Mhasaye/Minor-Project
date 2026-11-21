import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Dark contrasting colors for text on Sky Blue (#87CEEB) background:
COLOR_DARK_TITLE = RGBColor(15, 23, 42)      # Deep Slate/Navy #0F172A
COLOR_HEADER = RGBColor(20, 35, 75)          # Deep Navy #14234B
COLOR_TEXT = RGBColor(30, 41, 59)            # Slate 800 #1E293B
COLOR_MUTED = RGBColor(71, 85, 105)          # Slate 600 #475569
COLOR_ACCENT = RGBColor(14, 116, 144)        # Deep Cyan/Teal #0E7490
COLOR_BLUE = RGBColor(29, 78, 216)           # Deep Blue #1D4ED8

FONT_HEADING = "Times New Roman"
FONT_BODY = "Times New Roman"

def set_para_font(p, text, size=16, bold=False, italic=False, color=COLOR_TEXT, align=PP_ALIGN.LEFT, space_after=Pt(6)):
    p.text = text
    p.alignment = align
    p.space_after = space_after
    if p.runs:
        for r in p.runs:
            r.font.name = FONT_BODY
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = color

def add_bullet_run(p, bold_text, normal_text, size=15, bold_color=COLOR_HEADER, text_color=COLOR_TEXT, space_after=Pt(6)):
    p.space_after = space_after
    p.alignment = PP_ALIGN.LEFT
    # clear existing runs
    p.text = ""
    r1 = p.add_run()
    r1.text = bold_text + " " if bold_text else ""
    r1.font.name = FONT_BODY
    r1.font.size = Pt(size)
    r1.font.bold = True
    r1.font.color.rgb = bold_color

    r2 = p.add_run()
    r2.text = normal_text
    r2.font.name = FONT_BODY
    r2.font.size = Pt(size)
    r2.font.bold = False
    r2.font.color.rgb = text_color

def clear_text_frame(tf):
    for i in range(len(tf.paragraphs) - 1, 0, -1):
        p_elem = tf.paragraphs[i]._p
        p_elem.getparent().remove(p_elem)
    if tf.paragraphs:
        tf.paragraphs[0].text = ""

def remove_shape_if_empty(slide, shape_name_prefix):
    for s in list(slide.shapes):
        if s.name.startswith(shape_name_prefix):
            if s.has_text_frame and not s.text_frame.text.strip():
                sp_elem = s._element
                sp_elem.getparent().remove(sp_elem)

def main():
    prs = pptx.Presentation("ppt/Project_Review2-PPT_template_ORIGINAL_BACKUP.pptx")
    print(f"Total slides in presentation: {len(prs.slides)}")

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides[0]
    
    # Shape 3: 副标题 -> "SY-Project Design Presentation (Review II)"
    for s in s1.shapes:
        if s.name == "副标题":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "SY-Project Design Presentation (Review II)", size=32, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)
            s.top = Inches(0.40)
            s.left = Inches(1.0)
            s.width = Inches(11.33)
            s.height = Inches(0.80)

    # Shape 0: Google Shape;87;p1 -> "Department of Computer Engineering"
    for s in s1.shapes:
        if s.name == "Google Shape;87;p1":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "Department of Computer Engineering", size=24, bold=True, color=COLOR_DARK_TITLE, align=PP_ALIGN.CENTER)
            s.top = Inches(1.20)
            s.left = Inches(1.0)
            s.width = Inches(11.33)
            s.height = Inches(0.50)

    # Shape 2: 标题 -> "AY 2026-27 (Semester-III)"
    for s in s1.shapes:
        if s.name == "标题":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "Academic Year 2026-27 (Semester-III)", size=20, bold=False, color=COLOR_MUTED, align=PP_ALIGN.CENTER)
            s.top = Inches(1.75)
            s.left = Inches(1.0)
            s.width = Inches(11.33)
            s.height = Inches(0.45)

    # Shape 4: Title 54 -> Project Title
    for s in s1.shapes:
        if s.name == "Title 54":
            clear_text_frame(s.text_frame)
            p0 = s.text_frame.paragraphs[0]
            set_para_font(p0, "AI-Powered Mobile Urban Intelligence Platform\nUsing Public Transport Fleet", size=26, bold=True, color=COLOR_BLUE, align=PP_ALIGN.CENTER, space_after=Pt(6))
            p1 = s.text_frame.add_paragraph()
            set_para_font(p1, "Problem Statement: SIH 26124 | Organization: Bharat Electronics Limited (BEL)", size=16, bold=True, color=COLOR_DARK_TITLE, align=PP_ALIGN.CENTER)
            s.top = Inches(2.40)
            s.left = Inches(1.0)
            s.width = Inches(11.33)
            s.height = Inches(1.50)

    # Shape 1: Google Shape;88;p1 -> Guide Details
    for s in s1.shapes:
        if s.name == "Google Shape;88;p1":
            clear_text_frame(s.text_frame)
            p0 = s.text_frame.paragraphs[0]
            set_para_font(p0, "Project Guide:", size=20, bold=True, color=COLOR_HEADER, align=PP_ALIGN.LEFT, space_after=Pt(4))
            p1 = s.text_frame.add_paragraph()
            set_para_font(p1, "Prof. / Dr. [Faculty Guide Name]", size=16, bold=True, color=COLOR_TEXT, align=PP_ALIGN.LEFT, space_after=Pt(2))
            p2 = s.text_frame.add_paragraph()
            set_para_font(p2, "Department of Computer Engineering", size=14, bold=False, color=COLOR_MUTED, align=PP_ALIGN.LEFT, space_after=Pt(2))
            p3 = s.text_frame.add_paragraph()
            set_para_font(p3, "MIT Academy of Engineering, Pune", size=14, bold=False, color=COLOR_MUTED, align=PP_ALIGN.LEFT)
            s.top = Inches(4.30)
            s.left = Inches(0.80)
            s.width = Inches(4.50)
            s.height = Inches(2.50)

    # Shape 5: Text Box 61 -> Team Details
    for s in s1.shapes:
        if s.name == "Text Box 61":
            clear_text_frame(s.text_frame)
            p_head = s.text_frame.paragraphs[0]
            set_para_font(p_head, "Team Details:", size=20, bold=True, color=COLOR_HEADER, align=PP_ALIGN.LEFT, space_after=Pt(6))

            members = [
                ("Pranav Mhasaye (CS)", "PRN: 202501040309 | Ph: 7721886564", "202501040309@mitaoe.ac.in"),
                ("Abhishree Nalgintwar (CS)", "PRN: 202501040306 | Ph: 8767369374", "202501040306@mitaoe.ac.in"),
                ("Jayesh Nehete (CS)", "PRN: 202501040322 | Ph: 9340071421", "202501040322@mitaoe.ac.in"),
                ("Loni Yash Shrishail (E&TC)", "PRN: 202501070063 | Ph: 7666850976", "202501070063@mitaoe.ac.in"),
            ]
            for idx, (m_name, m_prn, m_email) in enumerate(members):
                p_m = s.text_frame.add_paragraph()
                p_m.space_after = Pt(4)
                p_m.alignment = PP_ALIGN.LEFT
                
                r1 = p_m.add_run()
                r1.text = f"• {m_name} — "
                r1.font.name = FONT_BODY
                r1.font.size = Pt(13)
                r1.font.bold = True
                r1.font.color.rgb = COLOR_DARK_TITLE

                r2 = p_m.add_run()
                r2.text = f"{m_prn}\n   Email: {m_email}"
                r2.font.name = FONT_BODY
                r2.font.size = Pt(12)
                r2.font.bold = False
                r2.font.color.rgb = COLOR_TEXT

            s.top = Inches(4.30)
            s.left = Inches(5.60)
            s.width = Inches(7.00)
            s.height = Inches(2.70)

    print("Slide 1 updated successfully.")

    # =========================================================================
    # SLIDE 2: INDEX
    # =========================================================================
    s2 = prs.slides[1]
    remove_shape_if_empty(s2, "Content Placeholder")
    for s in s2.shapes:
        if s.name == "Title 25":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "Presentation Index", size=32, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)
            s.top = Inches(0.40)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(0.80)
        elif s.name == "Google Shape;95;p2":
            clear_text_frame(s.text_frame)
            index_items = [
                ("1.", "Introduction & Project Background", "Public transport bus sensing reality & Vehicle-as-a-Sensor edge paradigm"),
                ("2.", "Problem Statement & Urban Challenges", "SIH 26124 (BEL), delayed road repairs, static CCTV blind spots & bandwidth bottleneck"),
                ("3.", "Objectives & Scope of Work", "Edge AI defect detection, ByteTrack tracking, RAM circular buffer & phase division"),
                ("4.", "Applications & Real-World Impact", "Municipal PWD road registry, traffic mobility heatmaps & forensic police dossiers"),
                ("5.", "Literature Review & Research Gaps", "23 peer-reviewed papers analyzed (2024–2026) & unified edge-cloud system gap"),
                ("6.", "System Architecture & Block Diagram", "End-to-end edge inference, MQTT cellular uplink, PostGIS & Leaflet GIS dashboard"),
                ("7.", "Implementation Methodology & Core Algorithms", "YOLO11n ONNX INT8, ByteTrack Kalman association, RAM FIFO & Haversine clustering"),
                ("8.", "Expected Outcomes & Review II Progress", "Review II achieved milestones (~45% progress) & final technical performance targets"),
                ("9.", "Selected Academic References", "IEEE-formatted peer-reviewed references from Nature, IEEE, Elsevier & MDPI"),
            ]
            for idx, (num, title, desc) in enumerate(index_items):
                p = s.text_frame.paragraphs[0] if idx == 0 else s.text_frame.add_paragraph()
                p.space_after = Pt(8)
                p.alignment = PP_ALIGN.LEFT

                r0 = p.add_run()
                r0.text = f"{num}  "
                r0.font.name = FONT_BODY
                r0.font.size = Pt(17)
                r0.font.bold = True
                r0.font.color.rgb = COLOR_BLUE

                r1 = p.add_run()
                r1.text = f"{title}"
                r1.font.name = FONT_BODY
                r1.font.size = Pt(17)
                r1.font.bold = True
                r1.font.color.rgb = COLOR_HEADER

                r2 = p.add_run()
                r2.text = f"  —  {desc}"
                r2.font.name = FONT_BODY
                r2.font.size = Pt(14)
                r2.font.bold = False
                r2.font.color.rgb = COLOR_MUTED

            s.top = Inches(1.40)
            s.left = Inches(1.00)
            s.width = Inches(11.33)
            s.height = Inches(5.20)

    print("Slide 2 updated successfully.")

    # =========================================================================
    # SLIDE 3: INTRODUCTION
    # =========================================================================
    s3 = prs.slides[2]
    remove_shape_if_empty(s3, "Content Placeholder")
    remove_shape_if_empty(s3, "Google Shape;103;p3")

    for s in s3.shapes:
        if s.name == "Title 32":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "Introduction & Project Context", size=32, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)
            s.top = Inches(0.40)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(0.80)
        elif s.name == "Google Shape;102;p3":
            clear_text_frame(s.text_frame)
            # Left column text box
            s.top = Inches(1.40)
            s.left = Inches(0.80)
            s.width = Inches(6.80)
            s.height = Inches(5.20)

            p0 = s.text_frame.paragraphs[0]
            add_bullet_run(p0, "• Problem Statement Context:", "SIH 26124 (Bharat Electronics Limited - BEL)", size=15, bold_color=COLOR_BLUE)

            p1 = s.text_frame.add_paragraph()
            add_bullet_run(p1, "• Urban Ground Reality:", "Routine public transit buses traverse 80%–90% of urban arterial road networks every 15–30 minutes, providing unprecedented temporal and spatial coverage.", size=14)

            p2 = s.text_frame.add_paragraph()
            add_bullet_run(p2, "• Fixed CCTV Limitations:", "Stationary surveillance cameras cover <3% of road grids, suffer from static blind spots, and cost crores to deploy and maintain.", size=14)

            p3 = s.text_frame.add_paragraph()
            add_bullet_run(p3, "• 'Vehicle-as-a-Sensor' Paradigm:", "Turning public transit buses into mobile edge-AI computing nodes converts everyday municipal transit into a live urban sensing grid at zero additional vehicular transit cost.", size=14, bold_color=COLOR_HEADER)

            p4 = s.text_frame.add_paragraph()
            add_bullet_run(p4, "• Multi-Task Sensing Capabilities:", "Our system simultaneously executes three critical urban functions at the edge:", size=14)

            p5 = s.text_frame.add_paragraph()
            add_bullet_run(p5, "   1. Road Hazard Detection:", "Real-time identification of potholes, cracks, and surface wear.", size=13, bold_color=COLOR_BLUE)

            p6 = s.text_frame.add_paragraph()
            add_bullet_run(p6, "   2. Dynamic Traffic Monitoring:", "Continuous estimation of congestion density & transit speeds.", size=13, bold_color=COLOR_BLUE)

            p7 = s.text_frame.add_paragraph()
            add_bullet_run(p7, "   3. Incident Forensics & ANPR:", "Rolling RAM buffer preserving critical event clips with plate OCR.", size=13, bold_color=COLOR_BLUE)

    # Add Figure image to Slide 3 on the right
    fig_path_1 = "iProject1/output_clips/executing.png"
    if os.path.exists(fig_path_1):
        s3.shapes.add_picture(fig_path_1, Inches(7.80), Inches(1.50), width=Inches(4.70))
        # Add caption box below picture
        cap_box = s3.shapes.add_textbox(Inches(7.80), Inches(4.90), Inches(4.70), Inches(1.50))
        cap_tf = cap_box.text_frame
        cap_tf.word_wrap = True
        p_cap = cap_tf.paragraphs[0]
        set_para_font(p_cap, "Figure 1: RoadScan AI Live Edge Vision Pipeline", size=13, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER, space_after=Pt(2))
        p_cap2 = cap_tf.add_paragraph()
        set_para_font(p_cap2, "Real-time YOLO11n detection with ByteTrack persistent ID tracking on live dashcam road footage.", size=12, bold=False, color=COLOR_MUTED, align=PP_ALIGN.CENTER)

    print("Slide 3 updated successfully.")

    # =========================================================================
    # SLIDE 4: PROBLEM STATEMENT
    # =========================================================================
    s4 = prs.slides[3]
    remove_shape_if_empty(s4, "Content Placeholder")
    for s in s4.shapes:
        if s.name == "Google Shape;120;p6":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "Problem Statement & Urban Challenges", size=32, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)
            s.top = Inches(0.40)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(0.80)
        elif s.name == "Google Shape;122;p6":
            clear_text_frame(s.text_frame)
            s.top = Inches(1.35)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(5.30)

            p0 = s.text_frame.paragraphs[0]
            add_bullet_run(p0, "Problem Statement Reference:", "Smart India Hackathon SIH 26124 | Organization: Bharat Electronics Limited (BEL)", size=16, bold_color=COLOR_BLUE, space_after=Pt(10))

            challenges = [
                ("1. Delayed Road Hazard Remediation & High Survey Costs:",
                 "Potholes, damaged dividers, and waterlogging persist for weeks without inspection, causing fatal accidents and vehicle damage. Inspection currently relies on slow citizen complaints or costly dedicated survey vehicles ($$$)."),
                ("2. Severe Spatial Blind Spots of Static CCTVs:",
                 "Fixed surveillance cameras cover <3% of the municipal road network; scaling static cameras across entire cities costs tens of crores of rupees and leaves vast coverage gaps on arterial and suburban streets."),
                ("3. Cellular Bandwidth & Cloud Saturation Bottleneck:",
                 "Streaming raw 1080p dashcam video from 500 transit buses would demand ~1.5 Gbps continuous uplink, collapsing 4G/5G cellular towers and creating huge recurring cloud egress and storage bills."),
                ("4. Multi-Bus Spatial Duplication & False Positive Clutter:",
                 "Multiple buses traveling the same transit corridor report identical defects dozens of times daily. Naive systems flood municipal databases with duplicate entries and overwhelm maintenance work crews.")
            ]

            for c_title, c_desc in challenges:
                p = s.text_frame.add_paragraph()
                add_bullet_run(p, f"• {c_title}", c_desc, size=14, bold_color=COLOR_HEADER, space_after=Pt(8))

            p_sol = s.text_frame.add_paragraph()
            add_bullet_run(p_sol, "• The Proposed Paradigm:", "Decentralized edge-AI processing on transit fleets transmitting lightweight telemetry (<5 KB JSON) with event-driven incident recording and spatio-temporal deduplication in the cloud.", size=14, bold_color=COLOR_BLUE, space_after=Pt(4))

    print("Slide 4 updated successfully.")

    # =========================================================================
    # SLIDE 5: OBJECTIVES AND SCOPE
    # =========================================================================
    s5 = prs.slides[4]
    remove_shape_if_empty(s5, "Content Placeholder")
    for s in s5.shapes:
        if s.name == "Title 28":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "Project Objectives & Scope of Work", size=32, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)
            s.top = Inches(0.40)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(0.80)
        elif s.name == "Text Placeholder 2":
            clear_text_frame(s.text_frame)
            s.top = Inches(1.35)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(5.30)

            p_head1 = s.text_frame.paragraphs[0]
            set_para_font(p_head1, "Primary Technical Objectives:", size=18, bold=True, color=COLOR_HEADER, space_after=Pt(6))

            objs = [
                ("Objective 1: Lightweight Edge-AI Vision Pipeline",
                 "Develop and calibrate an INT8-quantized YOLO11n computer vision detector capable of real-time road hazard detection (potholes, cracks, waterlogging) at ≥25 FPS on low-power edge compute."),
                ("Objective 2: Persistent Multi-Object Tracking (ByteTrack)",
                 "Implement ByteTrack Kalman-filter multi-object tracking to assign consistent track IDs across consecutive video frames, computing defect surface area and eliminating intra-video double counting."),
                ("Objective 3: Circular RAM Buffer & Kinematic-Triggered ANPR",
                 "Maintain a rolling 15-second uncompressed video buffer in edge RAM, triggered by kinematic/trajectory anomalies for automated high-res ANPR and incident clip capture."),
                ("Objective 4: Centralized GIS Dashboard & Spatial Deduplication",
                 "Build an interactive Web GIS dashboard with Haversine / ST-DBSCAN spatio-temporal clustering to consolidate repeat fleet observations into verified municipal repair tickets.")
            ]
            for o_title, o_desc in objs:
                p = s.text_frame.add_paragraph()
                add_bullet_run(p, f"• {o_title}:", o_desc, size=14, bold_color=COLOR_BLUE, space_after=Pt(6))

            p_head2 = s.text_frame.add_paragraph()
            set_para_font(p_head2, "Scope Division Across Project Phases:", size=17, bold=True, color=COLOR_HEADER, space_after=Pt(4))

            p_scope1 = s.text_frame.add_paragraph()
            add_bullet_run(p_scope1, "• Minor Project (Review II / Phase 1):", "Core edge-AI detection pipeline, ByteTrack persistent tracking, GPS sentence binding, and interactive Leaflet GIS dashboard prototype.", size=13, bold_color=COLOR_HEADER, space_after=Pt(2))

            p_scope2 = s.text_frame.add_paragraph()
            add_bullet_run(p_scope2, "• Major Project (Phase 2):", "Physical edge hardware deployment on Raspberry Pi 5 + Hailo-8 NPU, vehicle CAN-bus integration, and direct municipal PWD API integration.", size=13, bold_color=COLOR_MUTED, space_after=Pt(2))

    print("Slide 5 updated successfully.")

    # =========================================================================
    # SLIDE 6: APPLICATIONS
    # =========================================================================
    s6 = prs.slides[5]
    remove_shape_if_empty(s6, "Content Placeholder")
    for s in s6.shapes:
        if s.name == "Title 28":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "Applications & Real-World Stakeholder Impact", size=32, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)
            s.top = Inches(0.40)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(0.80)
        elif s.name == "Text Placeholder 2":
            clear_text_frame(s.text_frame)
            s.top = Inches(1.35)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(5.30)

            apps = [
                ("1. Municipal Corporations & Public Works Department (PWD):",
                 "• Automated Road Asset Inventory: Living digital registry of all road hazards with GPS coordinates and defect severity.\n• Prioritized Repair Dispatch: Data-driven budgeting and work-order dispatch based on Road Hazard Severity Index, reducing municipal road survey costs by up to 40%."),
                ("2. Smart City Traffic & Urban Mobility Authorities:",
                 "• Fleet-Derived Traffic Density Heatmaps: Real-time congestion monitoring, bottleneck identification, and average corridor transit speeds without expensive stationary inductive loop detectors."),
                ("3. Law Enforcement & Traffic Police:",
                 "• Tamper-Evident Forensic Incident Dossiers: Automated capture of pre-buffered 15-second incident video clips, verified vehicle license plates, and synchronized GPS timestamps for hit-and-run investigations."),
                ("4. Public Transit Corporations (PMPML / BMTC / BEST / DTC):",
                 "• Fleet Suspension Protection: Corridor roughness mapping to avoid heavily degraded road corridors and optimize bus preventive maintenance schedules, extending vehicle lifespan.")
            ]
            for idx, (a_title, a_desc) in enumerate(apps):
                p_t = s.text_frame.paragraphs[0] if idx == 0 else s.text_frame.add_paragraph()
                set_para_font(p_t, a_title, size=16, bold=True, color=COLOR_HEADER, space_after=Pt(2))
                for line in a_desc.split("\n"):
                    p_d = s.text_frame.add_paragraph()
                    colon_idx = line.find(":")
                    if colon_idx != -1:
                        add_bullet_run(p_d, line[:colon_idx+1], line[colon_idx+1:].strip(), size=13, bold_color=COLOR_BLUE, space_after=Pt(3))
                    else:
                        set_para_font(p_d, line, size=13, bold=False, color=COLOR_TEXT, space_after=Pt(3))

    print("Slide 6 updated successfully.")

    # =========================================================================
    # SLIDE 7: LITERATURE REVIEW
    # =========================================================================
    s7 = prs.slides[6]
    remove_shape_if_empty(s7, "Content Placeholder")
    remove_shape_if_empty(s7, "Google Shape;129;g16432b3a3c0_0_0")
    for s in s7.shapes:
        if s.name == "Title 32":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "Literature Review & State of the Art", size=32, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)
            s.top = Inches(0.40)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(0.80)
        elif s.name == "Google Shape;128;g16432b3a3c0_0_0":
            clear_text_frame(s.text_frame)
            s.top = Inches(1.35)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(5.30)

            p_survey = s.text_frame.paragraphs[0]
            add_bullet_run(p_survey, "Comprehensive Literature Review:", "Analysis of 23 Peer-Reviewed Papers (2024–2026) across Nature, IEEE, Elsevier, and MDPI:", size=15, bold_color=COLOR_BLUE, space_after=Pt(8))

            papers = [
                ("Paper 1: Shiva Shankar (2025) — Edge AI Feasibility",
                 "Proved that INT8-quantized YOLO achieves 58 FPS on a Raspberry Pi 5 with a tiny 48 MB footprint, confirming real-time edge feasibility without high-power GPUs."),
                ("Paper 2: Meng Huang, Xi Kuai et al. (Elsevier CEUS, 2024) — Transit Fleet Coverage",
                 "Demonstrated that instrumenting just 15%–25% of municipal bus routes achieves >85% spatial coverage of urban road networks within 48 hours, establishing fleet superiority over static sensors."),
                ("Paper 3: Dinesh Sahu, Shiv Prakash et al. (Nature Scientific Reports, 2026) — Bandwidth Reduction",
                 "Verified that edge-level anomaly filtering slashes network bandwidth consumption by over 75%, proving the necessity of lightweight edge telemetry over raw video streaming."),
                ("Paper 4: Ahmad Ijaz, Tayyba Sarfraz et al. (2026) — Motion-Blur Robust ANPR",
                 "Proved that multi-frame Laplacian variance selection overcomes vehicle motion blur and camera vibration, ensuring accurate OCR extraction from moving transit vehicles.")
            ]
            for p_title, p_desc in papers:
                p = s.text_frame.add_paragraph()
                add_bullet_run(p, f"• {p_title}:", p_desc, size=13, bold_color=COLOR_HEADER, space_after=Pt(6))

            p_gap = s.text_frame.add_paragraph()
            add_bullet_run(p_gap, "• Critical Research Gap Identified:", "Existing literature investigates road damage, traffic density, or license plate recognition in silos. No existing system unifies multi-task edge CV, in-memory circular buffering, and spatio-temporal multi-bus deduplication into an end-to-end urban platform.", size=13, bold_color=COLOR_BLUE, space_after=Pt(2))

    print("Slide 7 updated successfully.")

    # =========================================================================
    # SLIDE 8: BLOCK DIAGRAM
    # =========================================================================
    s8 = prs.slides[7]
    remove_shape_if_empty(s8, "Content Placeholder")
    for s in s8.shapes:
        if s.name == "Title 33":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "System Architecture & Block Diagram", size=32, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)
            s.top = Inches(0.40)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(0.80)
        elif s.name == "Google Shape;135;p8":
            clear_text_frame(s.text_frame)
            # Minimize this text box as the image is the primary diagram
            s.top = Inches(6.80)
            s.left = Inches(0.80)
            s.width = Inches(1.0)
            s.height = Inches(0.1)

    diagram_path = "ppt/system_block_diagram.png"
    if os.path.exists(diagram_path):
        s8.shapes.add_picture(diagram_path, Inches(0.80), Inches(1.30), width=Inches(11.73), height=Inches(5.25))

    print("Slide 8 updated successfully.")

    # =========================================================================
    # SLIDE 9: METHODOLOGY / ALGORITHMS
    # =========================================================================
    s9 = prs.slides[8]
    for s in s9.shapes:
        if s.name == "Title 1":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "Implementation Methodology & Core Algorithms", size=32, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)
            s.top = Inches(0.40)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(0.80)
        elif s.name == "Content Placeholder 2":
            clear_text_frame(s.text_frame)
            s.top = Inches(1.35)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(5.30)

            methods = [
                ("Method 1: Edge Computer Vision & ByteTrack Multi-Object Association",
                 "• Model Pipeline: YOLO11n fine-tuned on Indian road datasets (RDD2022 + Roboflow) and quantized to INT8 ONNX (≥25 FPS inference).\n• Tracking Algorithm: ByteTrack Kalman filter state estimation [u, v, s, r, u', v', s']^T with two-stage IoU association. Matches high- and low-confidence detections to maintain persistent defect IDs and compute surface area without duplicate counting."),
                ("Method 2: Kinematic-Triggered RAM Ring Buffer & Laplacian Sharpness ANPR",
                 "• Circular Buffer: 15-second FIFO circular queue in edge RAM preserving pre- and post-incident frames with zero flash drive wear.\n• Trigger Logic: Deceleration anomaly (>0.4g) or trajectory deviation locks incident video window.\n• Sharpness Score: Laplacian variance Var(∇² I_gray) selects the sharpest vehicle crop for OCR license plate extraction, eliminating motion blur."),
                ("Method 3: Spatio-Temporal Deduplication & Asymptotic Bayesian Verification",
                 "• Haversine Distance Clustering: Observations within d ≤ 3.5 m update existing records: d = 2R · arcsin(√(sin²(Δφ/2) + cos φ1 · cos φ2 · sin²(Δλ/2))).\n• Bayesian Confidence Accumulation: Formula P(Verified) = 1 - ∏(1 - c_i) — three independent fleet passes with c ≥ 0.80 achieve >99.2% verification confidence, filtering out spurious false positives.")
            ]
            for idx, (m_title, m_desc) in enumerate(methods):
                p_t = s.text_frame.paragraphs[0] if idx == 0 else s.text_frame.add_paragraph()
                set_para_font(p_t, m_title, size=15, bold=True, color=COLOR_HEADER, space_after=Pt(2))
                for line in m_desc.split("\n"):
                    p_d = s.text_frame.add_paragraph()
                    colon_idx = line.find(":")
                    if colon_idx != -1:
                        add_bullet_run(p_d, line[:colon_idx+1], line[colon_idx+1:].strip(), size=13, bold_color=COLOR_BLUE, space_after=Pt(3))
                    else:
                        set_para_font(p_d, line, size=13, bold=False, color=COLOR_TEXT, space_after=Pt(3))

    print("Slide 9 updated successfully.")

    # =========================================================================
    # SLIDE 10: EXPECTED OUTCOME
    # =========================================================================
    s10 = prs.slides[9]
    for s in s10.shapes:
        if s.name == "Title 1":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "Expected Outcomes & Review II Progress", size=32, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)
            s.top = Inches(0.40)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(0.80)
        elif s.name == "Content Placeholder 2":
            clear_text_frame(s.text_frame)
            # Left column text box
            s.top = Inches(1.35)
            s.left = Inches(0.80)
            s.width = Inches(6.80)
            s.height = Inches(5.30)

            p_stat = s.text_frame.paragraphs[0]
            add_bullet_run(p_stat, "Project Review II Status:", "~45% Completed (Functional Prototype Stage)", size=16, bold_color=COLOR_BLUE, space_after=Pt(6))

            p_h1 = s.text_frame.add_paragraph()
            set_para_font(p_h1, "A. Achieved Outcomes (Current Review II Milestones):", size=15, bold=True, color=COLOR_HEADER, space_after=Pt(3))

            achieved = [
                ("• Road Defect Detection:", "YOLO11n model fine-tuned and verified on Indian road footage for pothole and crack localization."),
                ("• Persistent Object Tracking:", "ByteTrack tracking logic implemented, ensuring stable defect IDs across frames."),
                ("• Edge Buffer & Telemetry Schema:", "Circular RAM buffer architecture and MQTT JSON payload schema completed."),
                ("• Interactive Web Dashboard Prototype:", "Built functional dashboard interface displaying real-time detection telemetry and defect coordinates.")
            ]
            for a_title, a_desc in achieved:
                p = s.text_frame.add_paragraph()
                add_bullet_run(p, a_title, a_desc, size=13, bold_color=COLOR_BLUE, space_after=Pt(3))

            p_h2 = s.text_frame.add_paragraph()
            set_para_font(p_h2, "B. Expected Final Deliverables & Performance Targets:", size=15, bold=True, color=COLOR_HEADER, space_after=Pt(3))

            targets = [
                ("• Edge Processing Throughput:", "Real-time edge inference at ≥25 FPS with <50ms processing latency."),
                ("• Cellular Uplink Savings:", "≥90% bandwidth reduction compared to streaming raw dashcam video (<5 KB JSON metadata)."),
                ("• Deduplication Accuracy:", "≥95% accuracy in clustering repeat sightings across fleet passes."),
                ("• Municipal Integration:", "Automated export of PWD repair work-orders prioritized by Road Hazard Severity Index.")
            ]
            for t_title, t_desc in targets:
                p = s.text_frame.add_paragraph()
                add_bullet_run(p, t_title, t_desc, size=13, bold_color=COLOR_HEADER, space_after=Pt(3))

    # Add Figure image to Slide 10 on the right
    fig_path_2 = "iProject1/output_clips/Front-end.png"
    if os.path.exists(fig_path_2):
        s10.shapes.add_picture(fig_path_2, Inches(7.80), Inches(1.50), width=Inches(4.70))
        cap_box_10 = s10.shapes.add_textbox(Inches(7.80), Inches(4.90), Inches(4.70), Inches(1.50))
        cap_tf_10 = cap_box_10.text_frame
        cap_tf_10.word_wrap = True
        p_cap = cap_tf_10.paragraphs[0]
        set_para_font(p_cap, "Figure 2: Functional RoadScan AI Web Dashboard", size=13, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER, space_after=Pt(2))
        p_cap2 = cap_tf_10.add_paragraph()
        set_para_font(p_cap2, "Interactive web interface providing video ingestion, threshold tuning, defect tracking preview, and quantitative output metrics.", size=12, bold=False, color=COLOR_MUTED, align=PP_ALIGN.CENTER)

    print("Slide 10 updated successfully.")

    # =========================================================================
    # SLIDE 11: SELECTED REFERENCES
    # =========================================================================
    s11 = prs.slides[10]
    remove_shape_if_empty(s11, "Content Placeholder")
    for s in s11.shapes:
        if s.name == "Title 26":
            clear_text_frame(s.text_frame)
            p = s.text_frame.paragraphs[0]
            set_para_font(p, "Selected Academic & Technical References", size=32, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)
            s.top = Inches(0.40)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(0.80)
        elif s.name == "Google Shape;141;p11":
            clear_text_frame(s.text_frame)
            s.top = Inches(1.35)
            s.left = Inches(0.80)
            s.width = Inches(11.73)
            s.height = Inches(5.30)

            refs = [
                ("[1]", "Shiva Shankar,", "\"Lightweight Real-Time Pothole Detection Using Quantized YOLO and Edge AI Deployment,\"", "in Proc. IEEE Conference on Computational Intelligence, 2025."),
                ("[2]", "Meng Huang, Xi Kuai, et al.,", "\"Bus-Based Mobile Sensing for City Monitoring: A Geospatial Coverage Analysis,\"", "Computers, Environment and Urban Systems, Elsevier, vol. 108, pp. 102061, 2024."),
                ("[3]", "Dinesh Sahu, Shiv Prakash, et al.,", "\"Edge Based Distributed Framework for Real Time Hazard Detection in Smart Transportation Systems,\"", "Nature Scientific Reports, vol. 16, no. 1, pp. 1042–1058, 2026."),
                ("[4]", "V. Sruk, S. Fajt, et al.,", "\"Vehicle-as-a-Sensor Approach for Urban Track and Road Anomaly Detection,\"", "Sensors, MDPI, vol. 25, no. 4, pp. 1189–1205, 2025."),
                ("[5]", "Ahmad Ijaz, Tayyba Sarfraz, et al.,", "\"AVNPR-Net: Real-Time Deep Learning Framework for Automatic Vehicle Number Plate Recognition,\"", "SJER, 2026."),
                ("[6]", "R. R. Sahoo, S. Mishra, et al.,", "\"iWatchRoad: Scalable Detection and Geospatial Visualization of Potholes in Smart Cities,\"", "IEEE Transactions on Intelligent Transportation Systems, vol. 26, 2025."),
                ("[7]", "City of Edmonton,", "\"AI Pothole Detection Using Mobile Cameras & YOLO Architecture,\"", "Open Municipal Technical Framework, 2024.")
            ]
            for idx, (num, authors, title, venue) in enumerate(refs):
                p = s.text_frame.paragraphs[0] if idx == 0 else s.text_frame.add_paragraph()
                p.space_after = Pt(7)
                p.alignment = PP_ALIGN.LEFT

                r0 = p.add_run()
                r0.text = f"{num}  "
                r0.font.name = FONT_BODY
                r0.font.size = Pt(13)
                r0.font.bold = True
                r0.font.color.rgb = COLOR_BLUE

                r1 = p.add_run()
                r1.text = f"{authors} "
                r1.font.name = FONT_BODY
                r1.font.size = Pt(13)
                r1.font.bold = True
                r1.font.color.rgb = COLOR_DARK_TITLE

                r2 = p.add_run()
                r2.text = f"{title} "
                r2.font.name = FONT_BODY
                r2.font.size = Pt(13)
                r2.font.italic = True
                r2.font.color.rgb = COLOR_HEADER

                r3 = p.add_run()
                r3.text = f"{venue}"
                r3.font.name = FONT_BODY
                r3.font.size = Pt(13)
                r3.font.bold = False
                r3.font.color.rgb = COLOR_MUTED

    print("Slide 11 updated successfully.")

    # =========================================================================
    # SLIDE 12: THANK YOU
    # =========================================================================
    s12 = prs.slides[11]
    remove_shape_if_empty(s12, "署名")
    
    # Hide or clear Title 36 so it doesn't overlap
    for s in s12.shapes:
        if s.name == "Title 36":
            clear_text_frame(s.text_frame)
            s.top = Inches(6.80)
            s.left = Inches(0.80)
            s.width = Inches(1.0)
            s.height = Inches(0.1)

    for s in s12.shapes:
        if s.name == "标题":
            clear_text_frame(s.text_frame)
            p0 = s.text_frame.paragraphs[0]
            set_para_font(p0, "Thank You!", size=44, bold=True, color=COLOR_BLUE, align=PP_ALIGN.CENTER, space_after=Pt(6))
            
            p1 = s.text_frame.add_paragraph()
            set_para_font(p1, "Questions & Discussion", size=24, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER, space_after=Pt(14))

            p2 = s.text_frame.add_paragraph()
            set_para_font(p2, "AI-Powered Mobile Urban Intelligence Platform Using Public Transport Fleet", size=18, bold=True, color=COLOR_DARK_TITLE, align=PP_ALIGN.CENTER, space_after=Pt(4))

            p3 = s.text_frame.add_paragraph()
            set_para_font(p3, "Problem Statement: SIH 26124 | Organization: Bharat Electronics Limited (BEL)", size=14, bold=False, color=COLOR_MUTED, align=PP_ALIGN.CENTER, space_after=Pt(14))

            p_t = s.text_frame.add_paragraph()
            set_para_font(p_t, "Project Team Members:", size=16, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER, space_after=Pt(4))

            p4_a = s.text_frame.add_paragraph()
            set_para_font(p4_a, "Pranav Mhasaye (CS) [PRN: 202501040309]   •   Abhishree Nalgintwar (CS) [PRN: 202501040306]", size=13, bold=False, color=COLOR_TEXT, align=PP_ALIGN.CENTER, space_after=Pt(4))

            p4_b = s.text_frame.add_paragraph()
            set_para_font(p4_b, "Jayesh Nehete (CS) [PRN: 202501040322]   •   Loni Yash Shrishail (E&TC) [PRN: 202501070063]", size=13, bold=False, color=COLOR_TEXT, align=PP_ALIGN.CENTER, space_after=Pt(14))

            p5 = s.text_frame.add_paragraph()
            set_para_font(p5, "Department of Computer Engineering | MIT Academy of Engineering, Pune", size=14, bold=True, color=COLOR_HEADER, align=PP_ALIGN.CENTER)

            s.top = Inches(0.80)
            s.left = Inches(1.00)
            s.width = Inches(11.33)
            s.height = Inches(5.80)

    print("Slide 12 updated successfully.")

    # Save presentation
    output_path = "ppt/Project_Review2-PPT_template.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    main()
