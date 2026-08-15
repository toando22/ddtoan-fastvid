from pydantic import BaseModel
from typing import Optional

class AffiliateResponse(BaseModel):
    id: str
    link_url: str
    campaign_name: str

    class Config:
        from_attributes = True

class LogCreate(BaseModel):
    action_type: str
    device_type: Optional[str] = "Desktop"
    reference_id: Optional[str] = None
    status_code: Optional[int] = 200
    
class AffiliateCreate(BaseModel):
    campaign_name: str
    link_url: str
    priority: Optional[int] = 0
    is_active: Optional[bool] = True
    required_clicks: Optional[int] = 1

class AffiliateUpdate(BaseModel):
    campaign_name: str
    link_url: str
    priority: int
    required_clicks: int
    click_count: int  # Cho phép Admin "phù phép" lại số lượt click
    is_active: bool    