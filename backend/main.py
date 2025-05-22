# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.responses import JSONResponse, FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from pathlib import Path
# from datetime import datetime
# import pandas as pd
# import shutil
# import pickle
# import os

# app = FastAPI()

# # Cho phép frontend kết nối
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Tải mô hình ARIMAX
# with open("arimax_model1.pkl", "rb") as f:
#     model_fit = pickle.load(f)

# # Tải dữ liệu biến ngoại sinh đã chuẩn bị
# exog_future_df = pd.read_csv("future_exog1.csv", parse_dates=["thoi_gian"])
# exog_future_df.set_index("thoi_gian", inplace=True)

# # Cấu hình thư mục uploads
# UPLOAD_DIR = Path(__file__).parent / "uploads"
# UPLOAD_DIR.mkdir(exist_ok=True)

# @app.post("/upload")
# async def upload_image(file: UploadFile = File(...)):
#     save_path = UPLOAD_DIR / file.filename
#     with open(save_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return JSONResponse(content={"url": f"/uploads/{file.filename}"})

# @app.get("/uploads/{filename}")
# async def get_uploaded_image(filename: str):
#     file_path = UPLOAD_DIR / filename
#     if file_path.exists():
#         return FileResponse(file_path)
#     return JSONResponse(status_code=404, content={"message": "File not found"})

# @app.post("/predict")
# async def predict(thoi_gian: str = Form(...)):
#     try:
#         # Chuyển đổi định dạng thời gian
#         target_date = datetime.strptime(thoi_gian.strip(), "%Y-%m-%d")
#         last_train_date = datetime(2021, 12, 31)

#         # Kiểm tra điều kiện hợp lệ
#         if target_date <= last_train_date:
#             return JSONResponse(content={"error": "Ngày dự đoán phải sau 2021-12-31"}, status_code=400)

#         steps = (target_date - last_train_date).days

#         # Lấy dữ liệu biến ngoại sinh tương ứng
#         future_exog = exog_future_df.loc[exog_future_df.index > last_train_date]
#         if len(future_exog) < steps:
#             return JSONResponse(content={"error": "Không đủ dữ liệu biến ngoại sinh để dự đoán đến ngày này."}, status_code=400)

#         future_exog_for_pred = future_exog.iloc[:steps]

#         # Dự đoán với ARIMAX
#         forecast = model_fit.get_forecast(steps=steps, exog=future_exog_for_pred)
#         prediction = forecast.predicted_mean.iloc[-1]

#         return {"prediction": round(prediction, 2)}

#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)





from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pathlib import Path
import shutil
import pickle

app = FastAPI()

# Cho phép frontend truy cập từ mọi domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load mô hình SARIMA từ file
with open("sarima_model1.pkl", "rb") as f:
    model_fit = pickle.load(f)

# Thư mục lưu ảnh upload
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    save_path = UPLOAD_DIR / file.filename
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Trả về đường dẫn truy cập ảnh
    return JSONResponse(content={"url": f"/uploads/{file.filename}"})


@app.get("/uploads/{filename}")
async def get_uploaded_image(filename: str):
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        return FileResponse(file_path)
    return JSONResponse(status_code=404, content={"message": "File not found"})


@app.post("/predict")
async def predict(thoi_gian: str = Form(...)):
    try:
        # Định dạng thời gian từ frontend: YYYY-MM-DD
        target_date = datetime.strptime(thoi_gian.strip(), "%Y-%m-%d")

        # Ngày cuối dữ liệu huấn luyện
        last_train_date = datetime(2022, 12, 31)
        steps = (target_date - last_train_date).days

        if steps <= 0:
            return JSONResponse(content={"error": "Ngày dự đoán phải sau 2022-12-31"}, status_code=400)

        # Dự đoán SARIMA
        forecast = model_fit.get_forecast(steps=steps)
        prediction = forecast.predicted_mean.iloc[-1]

        return {"prediction": round(prediction, 2)}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from backend.auth.auth import router as auth_router
# from backend.services.predict import router as predict_router
# from backend.services.image import router as image_router

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(auth_router, prefix="/auth")
# app.include_router(image_router, prefix="/upload")
# app.include_router(predict_router, prefix="/predict")
