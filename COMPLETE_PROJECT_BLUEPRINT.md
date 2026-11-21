# Complete Project Blueprint & Engineering Guide

**Project Title:** AI-Powered Mobile Urban Intelligence Platform Using Public Transport Fleet  
**Problem Statement Reference:** SIH 26124 (Bharat Electronics Limited - BEL)  
**Academic Level:** B.Tech Minor Project (2nd Year)  
**Theme:** Smart Automation | **Category:** Software  

---

## Executive Summary

Urban local bodies (ULBs) and transportation authorities struggle with fragmented, delayed, and expensive road monitoring. Currently, municipal bodies rely on manual road surveys, citizen grievances, and sparse fixed CCTV cameras covering under 3% of roads.

**The Core Insight:** Public transit buses traverse 80% to 90% of a city’s arterial and feeder road network multiple times every day on scheduled routes. By mounting intelligent edge-AI computer vision devices onto municipal buses, each bus becomes a **"Mobile Urban Sensing Unit" (Vehicle-as-a-Sensor)**. This platform continuously evaluates road surface health (potholes, cracks, waterlogging), monitors traffic density, and switches on an **event-triggered mode** to track safety incidents (rash driving, hit-and-run) with Automated Number Plate Recognition (ANPR) and GPS tagging.

---

## Chapter 1: The Bharat Electronics Limited (BEL) Mandate & Core Problem

### 1.1 Problem Background
- City buses already feature front, rear, and cabin cameras, but they function purely as passive CCTV recorders.
- Fixed CCTVs have massive spatial blind spots across feeder roads.
- Manual road condition surveys are slow, subjective, and infrequent (conducted once every 6–12 months).

### 1.2 The Three Fundamental Engineering Bottlenecks
1. **Cellular Bandwidth Saturation:** A fleet of 500 buses streaming 1080p video would generate ~1.5 Gbps of uplink traffic, costing lakhs monthly and overwhelming cellular networks. The edge must filter 99% of raw footage, transmitting only JSON telemetry and event-triggered video clips.
2. **Edge Hardware Constraints:** High temperatures and low power delivery restrict edge units to embedded single-board computers (Raspberry Pi 5 with Hailo-8 NPU or Jetson Orin Nano, <15W). Vision models must be quantized to INT8 and decoupled.
3. **Multi-Pass Fleet Redundancy:** Multiple buses traverse the same road segment daily. Naive databases record duplicate defects on every pass. The system must apply spatial clustering within a 3.5m radius to update a single verified physical defect.

---

## Chapter 2: Summary of Research Papers Literature Survey
*(For the full 21-paper master comparison table, refer to [LITERATURE_SURVEY_ANALYSIS_TABLE.md](file:///c:/Minor%20Project%202nd%20year/LITERATURE_SURVEY_ANALYSIS_TABLE.md) or [Literature_Survey_Completed.docx](file:///c:/Minor%20Project%202nd%20year/Literature_Survey_Completed.docx))*

The literature spans 6 technical pillars:
- **Pillar A: Road Defect & Pothole Detection:** Shiva Shankar (2025) proved INT8 quantized YOLO achieves 58 FPS on Pi 5. B.M.K. et al. (2024 - POT-YOLO) showed edge segmentation differentiates structural potholes from surface oil stains.
- **Pillar B: Vehicle-as-a-Sensor & Fleet Sensing:** Huang et al. (Elsevier 2024) proved that equipping just 15%–25% of city bus routes achieves >85% spatial urban coverage in 48 hours. Sruk et al. (Sensors 2025) validated repeat-pass anomaly filtering.
- **Pillar C: Edge-Cloud Bandwidth Optimization:** Dinesh Sahu et al. (Nature 2026) showed edge-level anomaly filtering slashes network bandwidth consumption by over 75%. Naveed Ejaz et al. (2025) proved lightweight edge detectors can trigger cloud report generation.
- **Pillar D: Traffic Flow & Congestion:** Mayouche & Azmani (2025) and Pudaruth et al. (2024) demonstrated fine-tuned YOLOv8 vehicle flow and virtual tripwire counting.
- **Pillar E: Incident Detection & Kinematics:** Durgesh Mishra (DRDO 2024) achieved 94.2% accuracy in rash driving detection using low-power IMU kinematics, providing an ideal trigger for video buffering.
- **Pillar F: ANPR & Deblurring:** Ahmad Ijaz et al. (2026) and Soppari et al. (2025) proved that selecting the sharpest frame from a 5-frame tracking history (Laplacian variance) overcomes dashcam motion blur.

---

## Chapter 3: GitHub Repositories Analysis & Architectural Borrowings

| Repository | What We Borrow & Implement |
|---|---|
| **lukekratz/raspberry-pi-5-hailo-8-pothole-detection-system** | GStreamer camera ingestion + Hailo-8 HEF INT8 compilation running at 30+ FPS under 10W. |
| **FarzadNekouee/YOLOv8_Pothole_Segmentation_Road_Damage** | Polygon defect masks to compute relative surface area for the Road Hazard Severity Index (RHSI). |
| **CityofEdmonton/AI-Pothole-Detection-Using-YOLO** | Municipal asset maintenance priority logic (Critical, Moderate, Minor) and work-order generation. |
| **thiagortk/Road-surface-detection-and-differentiation** | Multi-class road condition discrimination (asphalt vs. unpaved dirt tracks) to eliminate false alarms. |
| **Bryan-Japheth-Charles/RoadScan-AI (iProject1)** | Integration of ByteTrack with YOLO11n for persistent frame-to-frame tracking IDs and Streamlit player UI. |
| **jhasuman / Cyash / PeterHdd YOLO baselines** | Baseline hyperparameters, mosaic augmentation, and anchor box tuning on RDD2022. |

---

## Chapter 4: Core Technical Innovations Proposed

### Innovation 1: Asymmetric Dual-Pipeline Edge Engine
- **Continuous Mode (Low Compute):** Runs quantized YOLO11n at 20 FPS to detect road defects and compute traffic flow, emitting lightweight JSON telemetry (~200 bytes).
- **Event-Triggered Mode (High Compute on Demand):** An uncompressed 15-second circular RAM buffer is maintained. High-res ANPR (plate localization + perspective de-skew + OCR) activates only upon detected kinematic or trajectory anomalies, packaging a complete forensic evidence dossier.
- *Impact:* Saves 95% of GPU compute and 99% of cellular bandwidth.

### Innovation 2: Spatio-Temporal DBSCAN Deduplication (ST-DBSCAN)
- When multiple transit buses pass a defect, the cloud backend applies Haversine spatial thresholding ($d \le 3.5\text{ m}$) and vector heading alignment.
- Verification confidence updates asymptotically:
  $$P(\text{Verified}) = 1 - \prod_{i=1}^{k} (1 - c_i)$$
  Three independent passes with $c \ge 0.80$ reach $>99.2\%$ confidence, eliminating single-pass false positives.

### Innovation 3: Polygon-Derived Road Hazard Severity Index (RHSI)
$$\text{RHSI} = \alpha \cdot \frac{\text{Area}_{\text{defect}}}{\text{Area}_{\text{lane}}} + \beta \cdot \text{AspectRatio} + \gamma \cdot P_{\text{verified}}$$
- Scores range from 0.0 to 1.0, categorized into Critical (>0.70), Moderate (0.40–0.70), or Minor (<0.40).

---

## Chapter 5: Implementation Pathways

| Tier / Mode | Hardware & Stack | Suitability & Workflow |
|---|---|---|
| **Tier A (Development & Rapid Prototype)** | Dashcam/Phone video + Laptop GPU (RTX/GTX) + Python 3.11, OpenCV, YOLOv8/11, ByteTrack, Streamlit/FastAPI | Recommended for Semester Minor Project evaluation. Uses pre-recorded road footage with synchronized GPX GPS logs. Zero hardware procurement delays. |
| **Tier B (Physical Edge Field Prototype)** | Raspberry Pi 5 (8GB) + Hailo-8 M.2 AI Accel + USB Cam + USB GNSS Dongle + GStreamer, HailoRT (HEF INT8) | High-impact demonstration of true edge-computing constraints (<15W power profile, 35+ FPS). Ideal for Major Project. |
| **Tier C (Mobile Edge Smartphone App)** | Android / iOS Smartphone + ONNX Runtime Mobile + Flutter / React Native | Turnkey field test on actual college bus or two-wheeler using phone camera and built-in GPS/IMU. |

---

## Chapter 6: System Block Diagram & Workflow

```
                                  FULL SYSTEM WORKFLOW
                                  
  [ Bus-Mounted Camera ]               [ GNSS / GPS Receiver ]
            │                                     │
            ▼                                     ▼
 ┌──────────────────────┐              ┌──────────────────────┐
 │ Video Frame Reader   │              │ NMEA Sentence Parser │
 │ (OpenCV / GStreamer) │              │ (Lat, Lon, Velocity) │
 └──────────┬───────────┘              └──────────┬───────────┘
            │                                     │
            ▼                                     │
 ┌──────────────────────────────────────────────┐ │
 │      EDGE COMPUTING ENGINE (Onboard Bus)     │ │
 │                                              │ │
 │ ┌──────────────────┐    ┌──────────────────┐ │ │
 │ │  Circular RAM    │    │ YOLO11n / YOLOv8 │ │ │
 │ │  Ring Buffer     │    │ Lightweight Core │ │ │
 │ │  (15 sec Video)  │    │ (Defects+Traffic)│ │ │
 │ └────────┬─────────┘    └────────┬─────────┘ │ │
 │          │                       │           │ │
 │          │ Trigger Event?        ▼           │ │
 │          │   ┌───────┐      ┌───────────┐    │ │
 │          │   │ Rapid │      │ ByteTrack │    │ │
 │          │   │ Decel │      │ (Track IDs│    │ │
 │          │   └───┬───┘      └─────┬─────┘    │ │
 │          │       │                │          │ │
 │          ▼       ▼                ▼          │ │
 │    ┌───────────────────┐    ┌─────────────┐  │ │
 │    │ ANPR & OCR Engine │    │ Defect Area │  │ │
 │    │ (Plate Crop + STN)│    │ & Severity  │  │ │
 │    └─────────┬─────────┘    └──────┬──────┘  │ │
 └──────────────┼─────────────────────┼─────────┼─┘
                │                     │         │
                ▼                     ▼         ▼
    ┌─────────────────────────────────────────────────┐
    │     Teleport Gateway & Edge Data Packaging      │
    │  (Critical Video Snapshots + Compact JSON Telemetry)
    └────────────────────────┬────────────────────────┘
                             │ (Cellular MQTT / HTTPS)
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │            CENTRALIZED CLOUD / COMMAND BACKEND         │
 │                                                        │
 │ ┌────────────────────────────────────────────────────┐ │
 │ │ Spatio-Temporal Deduplication Engine (ST-DBSCAN)   │ │
 │ │ - Groups nearby detections within 3.5m radius     │ │
 │ │ - Updates Verification Score & Growth Rate         │ │
 │ └─────────────────────────┬──────────────────────────┘ │
 │                           ▼                            │
 │ ┌────────────────────────────────────────────────────┐ │
 │ │ Spatial Database (PostgreSQL / PostGIS / SQLite)   │ │
 │ └─────────────────────────┬──────────────────────────┘ │
 └───────────────────────────┼────────────────────────────┘
                             ▼
 ┌────────────────────────────────────────────────────────┐
 │           CENTRAL GIS & COMMAND WEB DASHBOARD          │
 │                                                        │
 │  • Interactive Map (Leaflet / Mapbox) with Heatmaps   │
 │  • Verified Pothole Markers with Defect Photos & Severity
 │  • Live Traffic Congestion Speeds by Road Segment      │
 │  • Incident Alert Center with Vehicle Plate & Evidence│
 └────────────────────────────────────────────────────────┘
```

---

## Chapter 7: Mathematical Formulations & Algorithms

### 7.1 Key Formulations
1. **Haversine Distance Metric ($R = 6,371,000\text{ m}$):**
   $$d = 2R \arcsin \left( \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)} \right)$$
2. **Bayesian Asymptotic Verification Confidence:**
   $$P(\text{Verified}) = 1 - \prod_{i=1}^{k}(1 - c_i)$$
3. **Road Hazard Severity Index (RHSI):**
   $$\text{RHSI} = \alpha \cdot \frac{\text{Area}_{\text{defect}}}{\text{Area}_{\text{lane}}} + \beta \cdot \text{AspectRatio} + \gamma \cdot P_{\text{verified}}$$
4. **Laplacian Blur Quality Metric:**
   $$\text{Sharpness} = \text{Var}(\nabla^2 I_{\text{gray}})$$

### 7.2 Algorithm 1: Onboard Edge Inference & Circular Ring Buffer
```python
def onboard_edge_pipeline(frame, gps_coords, ring_buffer):
    # Step 1: Push raw frame into rolling 15s memory buffer
    ring_buffer.append(frame)
    
    # Step 2: Continuous Road Defect & Traffic Inference
    detections = yolo_defect_model(frame, conf_threshold=0.45)
    tracked_defects = byte_tracker.update(detections)
    
    for defect in tracked_defects:
        if defect.is_new_track():
            severity = calculate_severity(defect.mask_polygon, defect.bbox)
            telemetry = {
                "track_id": defect.id,
                "class": defect.class_name,
                "severity_index": severity,
                "gps": gps_coords,
                "timestamp": current_utc_time()
            }
            mqtt_client.publish("bus/telemetry/defects", telemetry)
            
    # Step 3: Anomaly & Rash Driving Trigger Check
    incident_detected, offender_bbox = check_incident_conditions(frame, tracked_defects)
    
    if incident_detected:
        # Freeze ring buffer to extract 15-second incident evidence clip
        evidence_video = ring_buffer.export_clip(duration_sec=15)
        
        # Activate on-demand ANPR on offending vehicle
        plate_crop = crop_and_deskew_plate(frame, offender_bbox)
        plate_text, ocr_conf = run_enhanced_ocr(plate_crop)
        
        incident_bundle = {
            "event_type": "TRAFFIC_INCIDENT",
            "license_plate": plate_text,
            "plate_confidence": ocr_conf,
            "gps": gps_coords,
            "video_clip": evidence_video,
            "plate_image": plate_crop
        }
        mqtt_client.publish("bus/incidents/alerts", incident_bundle)
```

### 7.3 Algorithm 2: Centralized Spatial Deduplication (ST-DBSCAN)
```python
def ingest_and_deduplicate(incoming_defect):
    # Find existing records within 3.5 meters
    nearby_defects = db.query_within_radius(
        lat=incoming_defect.lat, 
        lon=incoming_defect.lon, 
        radius_meters=3.5
    )
    
    if nearby_defects.exists():
        matched = nearby_defects.closest()
        matched.pass_count += 1
        matched.last_seen = incoming_defect.timestamp
        # Update verification confidence asymptotically
        matched.verification_confidence = 1 - (1 - matched.verification_confidence) * (1 - incoming_defect.confidence)
        matched.severity_history.append(incoming_defect.severity_index)
        db.save(matched)
    else:
        # Register new unique road defect
        incoming_defect.pass_count = 1
        incoming_defect.verification_confidence = incoming_defect.confidence
        db.insert(incoming_defect)
```

---

## Chapter 8: Scope & Implementation Roadmap

| Milestone / Component | Minor Project MVP (Phase 1 - Present) | Major Project Full Scale (Phase 2 - Next Sem) |
|---|---|---|
| **Hardware Platform** | Laptop / Workstation GPU running Python, OpenCV, and pre-recorded road footage with GPX logs. | Physical edge deployment on Raspberry Pi 5 + Hailo-8 NPU / Jetson Orin Nano mounted in vehicle. |
| **Camera Architecture** | Single forward-facing dashcam video stream. | Multi-camera synchronized rig (forward road, rear traffic, cabin interior). |
| **Detection & Tracking** | YOLO11n + ByteTrack persistent defect ID tracking. | Multi-task network (Defects + Vehicles + Lane Markings) with INT8 edge compilation. |
| **Incident Buffer & ANPR** | Circular RAM buffer prototype + simulated trigger with plate crop & EasyOCR. | Real-time CAN-bus / IMU kinematic trigger with hardware-accelerated ANPR. |
| **Cloud & GIS Platform** | Localhost Streamlit / FastAPI web app with Leaflet map rendering defect pins. | Cloud-hosted PostGIS database with ST-DBSCAN fleet deduplication and municipal PWD API. |

---

## Chapter 9: Engineering Limitations & Practical Mitigations

1. **Night-time Headlight Glare & Low Light:**
   - *Limitation:* Overexposed headlights wash out road texture, causing false alarms.
   - *Mitigation:* Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) and train with night subsets of RDD2022.
2. **Bus Suspension Vibration & Motion Blur:**
   - *Limitation:* Road bumps blur camera frames, degrading OCR accuracy.
   - *Mitigation:* ByteTrack tracks vehicle across multiple frames; select the frame with highest Laplacian variance score ($\text{Var} > 100$) for OCR.
3. **Consumer GPS Drift in Urban Canyons:**
   - *Limitation:* Tall buildings cause GPS drift of 3–5 meters.
   - *Mitigation:* Spatial clustering threshold set to 3.5m combined with road heading vector matching.
4. **License Plate Variations (India):**
   - *Limitation:* Non-standard fonts, dirty plates, and angled two-wheeler plates cause OCR misreads.
   - *Mitigation:* Combine plate localization with Spatial Transformer Networks (STN) for perspective de-skewing; assign OCR confidence score to plate string.

---

## Chapter 10: Academic & Open-Source References

1. Shiva Shankar, *"Lightweight Real-Time Pothole Detection Using Quantized YOLO and Edge AI Deployment,"* 2025.
2. V. Sruk, S. Fajt et al., *"Vehicle-as-a-Sensor Approach for Urban Track Anomaly Detection,"* *Sensors*, MDPI, vol. 25, 2025.
3. Dinesh Sahu, Shiv Prakash et al., *"Edge Based Distributed Framework for Real Time Hazard Detection in Smart Transportation,"* *Nature Scientific Reports*, 2026.
4. R. R. Sahoo, S. Mishra et al., *"iWatchRoad: Scalable Detection and Geospatial Visualization of Potholes,"* 2025.
5. Ahmad Ijaz, Tayyba Sarfraz et al., *"AVNPR-Net: Real-Time Deep Learning Framework for Number Plate Recognition,"* *SJER*, 2026.
6. Meng Huang, Xi Kuai et al., *"Bus-Based Mobile Sensing for City Monitoring,"* *Computers, Environment and Urban Systems*, Elsevier, 2024.
7. Open-Source Edge NPU Implementation: `github.com/lukekratz/raspberry-pi-5-hailo-8-pothole-detection-system`
8. Open-Source YOLO Segmentation: `github.com/FarzadNekouee/YOLOv8_Pothole_Segmentation_Road_Damage_Assessment`
9. Municipal Pothole AI System: `github.com/CityofEdmonton/AI-Pothole-Detection-Using-YOLO`
10. RoadScan AI Video Tracker: `github.com/Bryan-Japheth-Charles/RoadScan-AI-Automated-Pothole-Detection-Tracking`
