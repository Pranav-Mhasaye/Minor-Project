import os
from PIL import Image, ImageDraw, ImageFont

def create_block_diagram():
    w, h = 1920, 960
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Fonts
    font_title = ImageFont.truetype('arialbd.ttf', 30)
    font_sub = ImageFont.truetype('arial.ttf', 18)
    font_col_title = ImageFont.truetype('arialbd.ttf', 20)
    font_box_title = ImageFont.truetype('arialbd.ttf', 16)
    font_box_desc = ImageFont.truetype('arial.ttf', 13)
    font_arrow = ImageFont.truetype('arialbd.ttf', 12)

    # Outer border & header
    draw.rectangle([10, 10, w - 10, h - 10], outline=(203, 213, 225), width=2)
    
    # Header banner
    draw.rectangle([10, 10, w - 10, 85], fill=(15, 23, 42))
    draw.text((w // 2, 35), "AI-POWERED MOBILE URBAN INTELLIGENCE PLATFORM", fill=(255, 255, 255), font=font_title, anchor="mm")
    draw.text((w // 2, 65), "End-to-End System Architecture: Edge Node → 4G/5G Uplink → Cloud Analytics → Municipal GIS Dashboard", fill=(148, 163, 184), font=font_sub, anchor="mm")

    # 4 Main Columns / Containers
    # Col 1: Bus Edge Node (x: 30 to 520)
    # Col 2: Telemetry & Uplink (x: 550 to 890)
    # Col 3: Cloud Analytics (x: 920 to 1340)
    # Col 4: Municipal Dashboard (x: 1370 to 1890)

    cols = [
        {
            "name": "1. ON-BUS EDGE AI NODE",
            "rect": [30, 105, 520, 920],
            "header_bg": (30, 58, 138),  # Blue
            "card_bg": (239, 246, 255),
            "border": (191, 219, 254),
            "boxes": [
                {"t": "Dashcam Video Feed", "d": "1080p @ 30 FPS Wide-Angle Camera\nFront-mounted on Municipal Transit Bus", "bg": (255, 255, 255), "y": 170, "h": 65},
                {"t": "OpenCV Frame Ingestion", "d": "Hardware-accelerated decoding & normalization\nReal-time frame pipeline (640x640 resize)", "bg": (255, 255, 255), "y": 255, "h": 65},
                {"t": "YOLO11n Edge Detector (INT8)", "d": "Lightweight quantized neural network (≥25 FPS)\nDetects Potholes, Cracks, Vehicles & Hazards", "bg": (219, 234, 254), "border": (59, 130, 246), "y": 340, "h": 75},
                {"t": "ByteTrack Multi-Object Tracker", "d": "Kalman-filter state estimation + IoU matching\nAssigns persistent defect IDs, prevents re-counts", "bg": (219, 234, 254), "border": (59, 130, 246), "y": 435, "h": 75},
                {"t": "15-Second Circular RAM Buffer", "d": "Lock-free FIFO ring buffer storing raw video frames\nZero disk wear-and-tear on edge memory", "bg": (254, 243, 199), "border": (245, 158, 11), "y": 530, "h": 75},
                {"t": "Kinematic & Anomaly Triggers", "d": "IMU harsh braking (>0.4g) / sudden lane deviations\nTriggers forensic incident window lock", "bg": (254, 243, 199), "border": (245, 158, 11), "y": 625, "h": 75},
                {"t": "High-Res ANPR Module", "d": "Laplacian sharpness frame selection (blur-free)\nYOLO license plate crop + EasyOCR extraction", "bg": (254, 226, 226), "border": (239, 68, 68), "y": 720, "h": 75},
                {"t": "Hardware GPS Sentence Sync", "d": "NMEA sentence binding: Lat, Lon, Speed, Heading\nAppended to every defect frame metadata", "bg": (255, 255, 255), "y": 815, "h": 65},
            ]
        },
        {
            "name": "2. COMMUNICATIONS LAYER",
            "rect": [550, 105, 900, 920],
            "header_bg": (109, 40, 217),  # Purple
            "card_bg": (245, 243, 255),
            "border": (221, 214, 254),
            "boxes": [
                {"t": "Lightweight MQTT Serializer", "d": "Serializes defect observations into compact JSON\nPayload: Defect ID, GPS, Class, Severity, Area (<5 KB)", "bg": (255, 255, 255), "y": 200, "h": 85},
                {"t": "Forensic Evidence Packager", "d": "Trigger-activated: Encodes 15s MP4 incident clip\nBundles GPS telemetry + OCR license plate result", "bg": (255, 255, 255), "y": 320, "h": 85},
                {"t": "4G / 5G Cellular Gateway", "d": "Low-bandwidth uplink with automatic offline queuing\n90%+ bandwidth savings vs streaming raw dashcam", "bg": (237, 233, 254), "border": (139, 92, 246), "y": 440, "h": 90},
                {"t": "TLS / AES-256 Encryption", "d": "Secure end-to-end telemetry transport\nTamper-proof digital signatures for forensic validity", "bg": (255, 255, 255), "y": 565, "h": 80},
                {"t": "Batch Telemetry Dispatch", "d": "Asynchronous publish-subscribe messaging\nQoS Level 1 guaranteed delivery to cloud brokers", "bg": (255, 255, 255), "y": 680, "h": 80},
            ]
        },
        {
            "name": "3. CLOUD ANALYTICS & GIS",
            "rect": [930, 105, 1370, 920],
            "header_bg": (13, 148, 136),  # Teal
            "card_bg": (240, 253, 250),
            "border": (153, 246, 228),
            "boxes": [
                {"t": "Cloud Ingestion API Gateway", "d": "FastAPI / MQTT Broker accepting fleet telemetry\nHigh-throughput concurrent multi-bus stream handler", "bg": (255, 255, 255), "y": 190, "h": 75},
                {"t": "Spatio-Temporal Deduplication", "d": "Haversine Distance Clustering (threshold d ≤ 3.5 m)\nMerges repeated sightings across multiple fleet passes", "bg": (204, 251, 241), "border": (20, 184, 166), "y": 285, "h": 85},
                {"t": "Bayesian Confidence Aggregator", "d": "Formula: P(Verified) = 1 - ∏(1 - ci)\n3 fleet observations (c ≥ 0.8) yield >99.2% certainty", "bg": (204, 251, 241), "border": (20, 184, 166), "y": 390, "h": 85},
                {"t": "Traffic Congestion Engine", "d": "Aggregates transit speeds and corridor transit times\nGenerates real-time municipal traffic density metrics", "bg": (255, 255, 255), "y": 495, "h": 75},
                {"t": "PostGIS Spatial Database", "d": "Geospatially indexed road defect & corridor records\nStores coordinates, bounding polygons, severity index", "bg": (255, 255, 255), "y": 590, "h": 80},
                {"t": "AWS S3 Evidence Repository", "d": "Cloud storage for incident video clips and plate crops\nTied to municipal incident case records", "bg": (255, 255, 255), "y": 690, "h": 75},
            ]
        },
        {
            "name": "4. MUNICIPAL STAKEHOLDER PORTAL",
            "rect": [1400, 105, 1890, 920],
            "header_bg": (194, 65, 12),  # Rust/Amber
            "card_bg": (255, 247, 237),
            "border": (254, 215, 170),
            "boxes": [
                {"t": "Interactive Leaflet GIS Dashboard", "d": "Interactive smart city command center\nMap visualization with color-coded hazard severity pins", "bg": (255, 237, 213), "border": (249, 115, 22), "y": 200, "h": 85},
                {"t": "Road Hazard Severity Heatmap", "d": "Visualizes severe pothole corridors and surface wear\nEnables predictive maintenance planning for PWD", "bg": (255, 255, 255), "y": 310, "h": 80},
                {"t": "Automated PWD Work Orders", "d": "Generates prioritized repair tickets with exact GPS,\nseverity rank, surface area & timestamped photographs", "bg": (255, 255, 255), "y": 415, "h": 85},
                {"t": "Traffic Mobility Analytics Hub", "d": "Displays average transit speeds, bottle-neck alerts\nand congestion indices across city arterial corridors", "bg": (255, 255, 255), "y": 525, "h": 80},
                {"t": "Law Enforcement Incident Dossier", "d": "Hit-and-run investigation portal with 15s clip replay,\nextracted license plate number & precise time/location", "bg": (255, 255, 255), "y": 630, "h": 85},
                {"t": "Transit Fleet Route Optimizer", "d": "Corridor roughness warnings to protect bus suspensions\nand optimize municipal transit dispatching", "bg": (255, 255, 255), "y": 740, "h": 80},
            ]
        }
    ]

    for col in cols:
        x1, y1, x2, y2 = col["rect"]
        # Container background
        draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=col["card_bg"], outline=col["border"], width=2)
        # Header box
        draw.rounded_rectangle([x1, y1, x2, y1 + 45], radius=10, fill=col["header_bg"])
        draw.rectangle([x1, y1 + 30, x2, y1 + 45], fill=col["header_bg"])  # flatten bottom corners
        draw.text(((x1 + x2) // 2, y1 + 22), col["name"], fill=(255, 255, 255), font=font_col_title, anchor="mm")

        # Inner boxes
        for b in col["boxes"]:
            bx1 = x1 + 15
            bx2 = x2 - 15
            by1 = b["y"]
            by2 = by1 + b["h"]
            b_bg = b.get("bg", (255, 255, 255))
            b_border = b.get("border", col["border"])
            draw.rounded_rectangle([bx1, by1, bx2, by2], radius=6, fill=b_bg, outline=b_border, width=1)
            # Title
            draw.text((bx1 + 10, by1 + 14), b["t"], fill=(15, 23, 42), font=font_box_title)
            # Desc lines
            desc_lines = b["d"].split("\n")
            for l_idx, line in enumerate(desc_lines):
                draw.text((bx1 + 10, by1 + 34 + l_idx * 16), line, fill=(71, 85, 105), font=font_box_desc)

    # Inter-column arrows
    # Arrow 1: Col 1 -> Col 2 (at y=250 and y=360)
    def draw_arrow(p1, p2, color=(100, 116, 139), width=3, text=""):
        draw.line([p1, p2], fill=color, width=width)
        # arrowhead
        x, y = p2
        draw.polygon([(x, y), (x - 10, y - 6), (x - 10, y + 6)], fill=color)
        if text:
            draw.text(((p1[0] + p2[0]) // 2, p1[1] - 12), text, fill=color, font=font_arrow, anchor="mm")

    draw_arrow((520, 242), (550, 242), color=(59, 130, 246), width=3, text="Telemetry")
    draw_arrow((520, 362), (550, 362), color=(239, 68, 68), width=3, text="Incidents")
    draw_arrow((900, 242), (930, 242), color=(109, 40, 217), width=3, text="MQTT/TLS")
    draw_arrow((900, 485), (930, 485), color=(109, 40, 217), width=3, text="4G Uplink")
    draw_arrow((1370, 327), (1400, 327), color=(13, 148, 136), width=3, text="Deduplicated")
    draw_arrow((1370, 532), (1400, 532), color=(13, 148, 136), width=3, text="GIS REST API")

    img.save("ppt/system_block_diagram.png", "PNG", dpi=(300, 300))
    print("Block diagram generated successfully: ppt/system_block_diagram.png")

create_block_diagram()
