from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime
from db.database import Base
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class AffiliateConfig(Base):
    __tablename__ = "affiliate_configs"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    campaign_name = Column(String(255), nullable=False)
    link_url = Column(Text, nullable=False)
    priority = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # BỔ SUNG CỘT NÀY ĐỂ FIX LỖI
    deleted_at = Column(DateTime, nullable=True) 
    required_clicks = Column(Integer, default=1)

class AccessLog(Base):
    __tablename__ = "access_logs"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    ip_address = Column(String(50))
    device_type = Column(String(50))
    user_agent = Column(Text)
    action_type = Column(String(50))
    reference_id = Column(String(36), nullable=True)
    status_code = Column(Integer, default=200)
    created_at = Column(DateTime, default=datetime.now)
    required_clicks = Column(Integer, default=1)

class BulkAccessCode(Base):
    __tablename__ = "bulk_access_codes"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    passcode = Column(String(100), nullable=False, unique=True)
    max_uses = Column(Integer, default=-1)
    used_count = Column(Integer, default=0)
    note = Column(Text, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # BỔ SUNG CỘT NÀY CHO ĐỒNG BỘ
    deleted_at = Column(DateTime, nullable=True)
    
class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="SUPER_ADMIN")
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)    