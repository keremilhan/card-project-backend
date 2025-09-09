from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class SubscriptionType(BaseModel):
    type: str
    cost: str

class TileBase(BaseModel):
    id: str = Field(..., alias="_id")
    name: str = Field(..., max_length=32)
    short_description: str
    complete_description: str
    version: str
    image_path: str
    category: str
    subscription_type: SubscriptionType
    metadata: Optional[Dict[str, Any]] = None
    installed: bool = False

class InstalledTileCreate(BaseModel):
    tile_id: str
    name: str
    tile_metadata: Optional[Dict[str, Any]] = None
