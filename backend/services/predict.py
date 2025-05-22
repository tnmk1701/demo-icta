from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from datetime import datetime
import pickle
from pathlib import Path

router = APIRouter()
model_path = Path(__file__).parent.parent / "ml_models" / "arimax_model1.pkl"
model_fit = pickle.load(open(model_path, "rb"))

@router.post("/")
async def predict(thoi_gian: str = Form(...)):
    try:
        target_date = datetime.strptime(thoi_gian.strip(), "%Y-%m-%d")
        last_train_date = datetime(2022, 12, 31)
        steps = (target_date - last_train_date).days

        if steps <= 0:
            return JSONResponse(content={"error": "Ngày dự đoán phải sau 2022-12-31"}, status_code=400)

        forecast = model_fit.get_forecast(steps=steps)
        prediction = forecast.predicted_mean.iloc[-1]
        return {"prediction": round(prediction, 2)}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
