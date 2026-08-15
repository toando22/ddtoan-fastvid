from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import AffiliateConfig
from db.schemas import AffiliateResponse, AffiliateCreate, AffiliateUpdate

router = APIRouter()

# 1. DÀNH CHO USER: Lấy link ưu tiên nhất đang bật
@router.get("/active", response_model=AffiliateResponse)
def get_active_affiliate(db: Session = Depends(get_db)):
    config = db.query(AffiliateConfig).filter(
        AffiliateConfig.is_active == True,
        AffiliateConfig.deleted_at == None
    ).order_by(AffiliateConfig.priority.desc()).first()
    
    if not config:
      return {"id": "default", "link_url": "https://shopee.vn/", "campaign_name": "Default", "required_clicks": 1}
    return config

# 2. DÀNH CHO ADMIN: Lấy tất cả danh sách chiến dịch
@router.get("/all")
def get_all_affiliates(db: Session = Depends(get_db)):
    configs = db.query(AffiliateConfig).filter(
        AffiliateConfig.deleted_at == None
    ).order_by(AffiliateConfig.priority.desc()).all()
    return configs

# 3. DÀNH CHO ADMIN: Thêm link Affiliate mới
@router.post("/add")
def add_affiliate(data: AffiliateCreate, db: Session = Depends(get_db)):
    new_config = AffiliateConfig(
        campaign_name=data.campaign_name,
        link_url=data.link_url,
        priority=data.priority,
        is_active=data.is_active,
        required_clicks=data.required_clicks
    )
    db.add(new_config)
    db.commit()
    return {"success": True, "message": "Thêm chiến dịch thành công!"}

# 4. DÀNH CHO ADMIN: Bật/Tắt trạng thái chiến dịch
@router.put("/toggle/{config_id}")
def toggle_affiliate(config_id: str, db: Session = Depends(get_db)):
    config = db.query(AffiliateConfig).filter(AffiliateConfig.id == config_id).first()
    if not config:
        return {"success": False, "message": "Không tìm thấy chiến dịch"}
    
    config.is_active = not config.is_active
    db.commit()
    return {"success": True, "message": "Cập nhật trạng thái thành công!", "new_status": config.is_active}

# --- CHÈN THÊM 2 API NÀY VÀO CUỐI FILE ---

# 5. DÀNH CHO USER: Tracking mỗi khi bị nhảy tab bẫy
@router.post("/track-click/{config_id}")
def track_click(config_id: str, db: Session = Depends(get_db)):
    config = db.query(AffiliateConfig).filter(AffiliateConfig.id == config_id).first()
    if config:
        config.click_count += 1
        db.commit()
        return {"success": True}
    return {"success": False}

# 6. DÀNH CHO ADMIN: Sửa trực tiếp toàn bộ thông tin chiến dịch
@router.put("/edit/{config_id}")
def edit_affiliate(config_id: str, data: AffiliateUpdate, db: Session = Depends(get_db)):
    config = db.query(AffiliateConfig).filter(AffiliateConfig.id == config_id).first()
    if not config:
        return {"success": False, "message": "Không tìm thấy chiến dịch"}
    
    # Ghi đè dữ liệu mới
    config.campaign_name = data.campaign_name
    config.link_url = data.link_url
    config.priority = data.priority
    config.required_clicks = data.required_clicks
    config.click_count = data.click_count
    config.is_active = data.is_active
    
    db.commit()
    return {"success": True, "message": "Cập nhật thành công!"}