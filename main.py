from fastapi import FastAPI, Request, UploadFile, File, Depends, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
import cv2
import numpy as np
from ultralytics import YOLO
from deepface import DeepFace
import uuid
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

# Import database components
from database import get_db, Analysis, create_tables

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static folder for serving static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Create static folders for uploaded and processed images
UPLOAD_FOLDER = "static/uploads"
PROCESSED_FOLDER = "static/processed_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Create database tables
create_tables()

# Load YOLO model
model = YOLO("yolov8x.pt")

# Mapping original expressions to classroom-specific expressions
expression_mapping = {
    "Sad": "Focused Challenge",

    "Angry": "Classroom Tension",
    "Fear": "Learning Anxiety",
    "Happy": "Active Engagement",
    "Surprise": "Learning Surprise",
    "Neutral": "Calm Attention"
}

# Database mapping for expression counts
db_expression_mapping = {
    "Focused Challenge": "focused_challenge_count",
    "Classroom Tension": "classroom_tension_count",
    "Learning Anxiety": "learning_anxiety_count",
    "Active Engagement": "active_engagement_count",
    "Learning Surprise": "learning_surprise_count",
    "Calm Attention": "calm_attention_count"
}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Generate unique filename to prevent overwriting
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_location = f"{UPLOAD_FOLDER}/{filename}"
        
        # Save the uploaded file
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File saved: {file_location}")

        # Read the image with OpenCV
        image = cv2.imread(file_location)
        if image is None:
            logger.error(f"Failed to read image: {file_location}")
            return {"error": "Failed to process image"}
        
        processed_image = image.copy()

        # Perform detection with YOLO
        results = model(image, conf=0.15, iou=0.4)

        # Initialize variables
        person_count = 0
        expression_counts = {}

        # Function for custom Non-Maximum Suppression (NMS)
        def custom_nms(boxes, scores, iou_threshold=0.4):
            """Perform Non-Maximum Suppression (NMS) on bounding boxes."""
            if len(boxes) == 0:
                return []
            boxes = np.array(boxes)
            scores = np.array(scores)
            areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
            order = scores.argsort()[::-1]  # Sort by scores in descending order

            keep = []  # List of indices of boxes to keep
            while order.size > 0:
                i = order[0]
                keep.append(i)

                xx1 = np.maximum(boxes[i, 0], boxes[order[1:], 0])
                yy1 = np.maximum(boxes[i, 1], boxes[order[1:], 1])
                xx2 = np.minimum(boxes[i, 2], boxes[order[1:], 2])
                yy2 = np.minimum(boxes[i, 3], boxes[order[1:], 3])

                w = np.maximum(0, xx2 - xx1)
                h = np.maximum(0, yy2 - yy1)
                intersection = w * h
                union = areas[i] + areas[order[1:]] - intersection
                iou = intersection / union
                order = order[np.where(iou <= iou_threshold)[0] + 1]

            return keep

        # Collect bounding boxes and confidence scores for "person" class
        boxes = []
        scores = []
        for result in results[0].boxes:
            cls = int(result.cls[0])  # Class ID
            conf = float(result.conf[0])  # Confidence score
            x_min, y_min, x_max, y_max = map(int, result.xyxy[0])
            if cls == 0:  # Class ID 0 corresponds to "person"
                boxes.append([x_min, y_min, x_max, y_max])
                scores.append(conf)

        # Apply custom NMS to filter overlapping boxes
        nms_indices = custom_nms(boxes, scores)

        # Process detected and filtered bounding boxes
        for i in nms_indices:
            x_min, y_min, x_max, y_max = boxes[i]
            face = processed_image[y_min:y_max, x_min:x_max]
            person_count += 1

            try:
                # Perform facial expression analysis using DeepFace
                analysis = DeepFace.analyze(face, actions=["emotion"], enforce_detection=False)
                if isinstance(analysis, list):
                    analysis = analysis[0]

                # Normalize emotion keys to match mapping
                detected_emotion = max(analysis["emotion"], key=analysis["emotion"].get)
                detected_emotion = detected_emotion.capitalize()  # Normalize to match keys in mapping

                # Map to classroom-specific name
                classroom_expression = expression_mapping.get(detected_emotion, detected_emotion)

                # Update expression counts
                expression_counts[classroom_expression] = expression_counts.get(classroom_expression, 0) + 1

                # Draw bounding box and emotion label with classroom-specific name
                label = f"{classroom_expression} {scores[i]:.2f}"
                cv2.rectangle(processed_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                cv2.putText(processed_image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            except Exception as e:
                logger.error(f"Error analyzing face: {e}")

        # Prepare final output summary with classroom-specific names
        summary_text = f"Total People Detected: {person_count}"
        y_offset = 50
        for classroom_expression, count in expression_counts.items():
            summary_text += f"\n{classroom_expression}: {count}"

        # Add the summary text to the image
        y_position = 30
        for line in summary_text.split("\n"):
            cv2.putText(processed_image, line, (30, y_position), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            y_position += y_offset

        # Save the processed image
        processed_filename = f"processed_{filename}"
        output_path = f"{PROCESSED_FOLDER}/{processed_filename}"
        cv2.imwrite(output_path, processed_image)
        
        logger.info(f"Processed image saved: {output_path}")

        # Create a database entry for this analysis
        db_analysis = Analysis(
            image_filename=filename,
            processed_image_filename=processed_filename,
            person_count=person_count,
            summary=summary_text
        )
        
        # Set expression counts in database model
        for expr, count in expression_counts.items():
            db_field = db_expression_mapping.get(expr)
            if db_field:
                setattr(db_analysis, db_field, count)
        
        # Save to database
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        logger.info(f"Analysis saved to database with ID: {db_analysis.id}")

        # Return the processed image URL and analysis ID
        return {"success": True, "analysis_id": db_analysis.id}
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return {"error": str(e)}

@app.get("/result/{analysis_id}", response_class=HTMLResponse)
async def get_result(request: Request, analysis_id: int, db: Session = Depends(get_db)):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not analysis:
        return RedirectResponse(url="/")
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": analysis.summary,
        "processed_image_url": f"/static/processed_images/{analysis.processed_image_filename}",
        "analysis": analysis
    })

@app.get("/history", response_class=HTMLResponse)
async def get_history(
    request: Request, 
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    # Get total count of analyses
    total = db.query(Analysis).count()
    
    # Calculate offset and get analyses for the current page
    offset = (page - 1) * limit
    analyses = db.query(Analysis).order_by(Analysis.timestamp.desc()).offset(offset).limit(limit).all()
    
    # Calculate total pages
    total_pages = (total + limit - 1) // limit
    
    return templates.TemplateResponse("history.html", {
        "request": request,
        "analyses": analyses,
        "page": page,
        "limit": limit,
        "total_pages": total_pages
    })

@app.get("/static/processed_images/{filename}", response_class=FileResponse)
async def get_processed_image(filename: str):
    return FileResponse(f"{PROCESSED_FOLDER}/{filename}")