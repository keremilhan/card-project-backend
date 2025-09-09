from sqlalchemy import Column, Integer, String, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class InstalledTile(Base):
    __tablename__ = "installed_tiles"
    id = Column(Integer, primary_key=True, index=True)
    tile_id = Column(String, unique=True, index=True)
    name = Column(String)
    installed = Column(Boolean, default=True)
    tile_metadata = Column(JSON)
