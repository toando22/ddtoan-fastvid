# API endpoint definitions for download routes
from fastapi import APIRouter
from pydantic import BaseModel
from core.extractor import extract_video_info
from fastapi.responses import StreamingResponse
import urllib.parse
import requests

router = APIRouter()

# Schema nhận dữ liệu từ Frontend
class URLRequest(BaseModel):
    url: str

@router.post("/extract")
def extract_video(request: URLRequest):
    result = extract_video_info(request.url)
    return result

@router.get("/force-download")
def force_download(url: str, filename: str = "FastVid_Video.mp4"):
    """
    API Proxy lấy video từ link gốc và stream về cho Client
    kèm Header ép trình duyệt lưu file thay vì phát video.
    """
    # Xử lý giải mã URL (đề phòng URL chứa ký tự đặc biệt)
    decoded_url = urllib.parse.unquote(url)

    def iterfile():
        # Gọi request tới server chứa video gốc
        with requests.get(decoded_url, stream=True) as r:
            # Chia nhỏ file thành từng cục (chunk) 8KB để không làm tràn RAM server
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    yield chunk

    # Header quan trọng nhất: Ép trình duyệt tải xuống (attachment)
    headers = {
        "Content-Disposition": f'attachment; filename="{filename}"'
    }
    
    return StreamingResponse(iterfile(), media_type="video/mp4", headers=headers)