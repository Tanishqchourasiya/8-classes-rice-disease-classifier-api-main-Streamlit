import io
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from .schemas import PredictionResponse
from .services import predict_image
from .config import config

app = FastAPI(title="Crop Disease Detection API")

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    image_data = await file.read()
    image = io.BytesIO(image_data)

    predicted_class, confidence = predict_image(image)

    return PredictionResponse(
        predicted_class=predicted_class,
        confidence=confidence,
        remedy=config["remedies"].get(predicted_class, "No specific remedy available")
    )
