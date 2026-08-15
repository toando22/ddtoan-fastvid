from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt
from datetime import datetime
from db.database import get_db
from db.models import BulkAccessCode, AdminUser

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

# ==========================================
# 2. PHẦN ĐĂNG NHẬP QUẢN TRỊ ADMIN (Bổ sung mới)
# ==========================================
class AdminLoginRequest(BaseModel):
    username: str
    password: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@router.post("/admin-login")
def admin_login(form: AdminLoginRequest, db: Session = Depends(get_db)):
    # Tìm kiếm admin theo username và chưa bị xóa (deleted_at IS NULL)
    admin = db.query(AdminUser).filter(
        AdminUser.username == form.username,
        AdminUser.deleted_at.is_(None)
    ).first()
    
    if not admin or not verify_password(form.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu quản trị không chính xác!"
        )
    
    # Cập nhật thời gian đăng nhập gần nhất
    admin.last_login = datetime.utcnow()
    db.commit()
    
    return {
        "success": True,
        "message": "Đăng nhập quản trị thành công!",
        "username": admin.username,
        "role": admin.role
    }