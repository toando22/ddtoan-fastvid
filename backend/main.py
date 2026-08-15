from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import download, affiliate, log, auth

app = FastAPI(title="Video Downloader API")

# Cấu hình CORS cấp phép chính xác cho tên miền thật và môi trường code nội bộ
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fastvid.click", 
        "https://www.fastvid.click",
        "http://localhost:5173", # Giữ lại để bạn test code trên máy cá nhân
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nhúng các API Router (Đã dọn dẹp các dòng code bị lặp)
app.include_router(download.router, prefix="/api/v1/download", tags=["Download"])
app.include_router(affiliate.router, prefix="/api/v1/affiliate", tags=["Affiliate"])
app.include_router(log.router, prefix="/api/v1/logs", tags=["Logs"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

@app.get("/")
def read_root():
    return {"message": "Backend API is running!"}