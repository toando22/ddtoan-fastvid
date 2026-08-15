from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.database import get_db
from db.models import BulkAccessCode

router = APIRouter()

class PasscodeRequest(BaseModel):
    passcode: str

@router.post("/verify")
def verify_passcode(request: PasscodeRequest, db: Session = Depends(get_db)):
    # Tìm mã trong Database
    code = db.query(BulkAccessCode).filter(
        BulkAccessCode.passcode == request.passcode,
        BulkAccessCode.is_active == True
    ).first()

    if not code:
        return {"success": False, "message": "Mã truy cập không hợp lệ hoặc đã bị khóa!"}

    # Kiểm tra giới hạn lượt dùng (nếu max_uses khác -1)
    if code.max_uses != -1 and code.used_count >= code.max_uses:
        return {"success": False, "message": "Mã này đã hết lượt sử dụng!"}

    # Tăng biến đếm số lần sử dụng lên 1
    code.used_count += 1
    db.commit()

    return {"success": True, "message": "Xác thực thành công!"}