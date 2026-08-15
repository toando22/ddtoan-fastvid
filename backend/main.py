# FastAPI app entrypoint and CORS configuration
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import download
from api import download, affiliate, log, auth

app = FastAPI(title="Video Downloader API")

# Cấu hình CORS cho phép Vue.js gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Trong thực tế khi deploy sẽ thay bằng domain của bạn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Nhúng các API Router vào hệ thống (CHÚ Ý DÒNG affiliate VÀ auth)
app.include_router(download.router, prefix="/api/v1/download", tags=["Download"])
app.include_router(affiliate.router, prefix="/api/v1/affiliate", tags=["Affiliate"]) # Dòng này gọi các API của Admin
app.include_router(log.router, prefix="/api/v1/logs", tags=["Logs"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"]) # Dòng này gọi API nhập mã tải hàng loạt
# Nhúng API router
app.include_router(download.router, prefix="/api/v1")

# Thêm dòng này ở khu vực app.include_router
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

@app.get("/")
def read_root():
    return {"message": "Backend API is running!"}