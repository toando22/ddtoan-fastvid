from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import AccessLog
from db.schemas import LogCreate

# ĐÂY CHÍNH LÀ BIẾN 'router' MÀ BẠN ĐANG THIẾU
router = APIRouter()

@router.post("/record")
def record_user_log(request_data: LogCreate, request: Request, db: Session = Depends(get_db)):
    # Trích xuất IP và User-Agent từ Request
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")
    
    new_log = AccessLog(
        ip_address=client_ip,
        user_agent=user_agent,
        action_type=request_data.action_type,
        device_type=request_data.device_type,
        reference_id=request_data.reference_id,
        status_code=request_data.status_code
    )
    
    db.add(new_log)
    db.commit()
    return {"success": True, "message": "Log recorded"}