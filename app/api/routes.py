import os
from fastapi import APIRouter, UploadFile, Depends, File, HTTPException
from sqlalchemy.orm import Session
from app.database import crud
from app.database.database import get_db
from app.services.image_service import process_upload_file
from app.services.model_service import predict_image

router = APIRouter()


@router.post("/upload")
async def upload_scan(
    file: UploadFile = File(...),
    user_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Endpoint to upload an MRI scan.
    """
    # 1. Ensure file type is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    # 2. Save file
    file_path = await process_upload_file(file)

    # 3. Save DB record
    db_scan = crud.create_scan(db=db, file_path=file_path, user_id=user_id)

    return {"message": "File uploaded successfully", "scan_id": db_scan.id, "file_path": file_path}


@router.post("/predict")
async def predict_scan(
    scan_id: int,
    db: Session = Depends(get_db)
):
    """
    Endpoint to trigger a prediction on an already uploaded MRI scan.
    Returns: {"prediction": "Tumor", "confidence": 0.94}
    """
    # 1. Fetch scan
    db_scan = crud.get_scan(db=db, scan_id=scan_id)
    if not db_scan:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    if not os.path.exists(db_scan.file_path):
        raise HTTPException(status_code=500, detail="Image file not found on server")

    # 2. Predict using Model Service
    try:
        prediction_label, confidence = predict_image(db_scan.file_path)
    except Exception as e:
         raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    # 3. Save prediction
    db_prediction = crud.create_prediction(
        db=db, 
        scan_id=scan_id, 
        prediction=prediction_label, 
        confidence=confidence
    )

    return {
        "prediction_id": db_prediction.id,
        "prediction": db_prediction.prediction,
        "confidence": db_prediction.confidence,
    }

