from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.db.models import InstalledTile
from app.schemas.tile import TileBase, InstalledTileCreate
from typing import List
import json
import os

router = APIRouter()

TILES_JSON_PATH = os.path.join(os.path.dirname(__file__), '../static/tiles.json')

def load_tiles():
    with open(TILES_JSON_PATH, 'r') as f:
        return json.load(f)

@router.get("/tiles", response_model=List[TileBase])
async def get_tiles(db: AsyncSession = Depends(get_db)):
    tiles = load_tiles()
    result = await db.execute(select(InstalledTile.tile_id).where(InstalledTile.installed == True))
    installed_ids = {row[0] for row in result.fetchall()}
    for tile in tiles:
        tile["installed"] = tile["_id"] in installed_ids
    return tiles

@router.post("/tiles/install")
async def install_tile(tile: InstalledTileCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InstalledTile).where(InstalledTile.tile_id == tile.tile_id))
    db_tile = result.scalar_one_or_none()
    if db_tile:
        return {
            "_id": db_tile.tile_id,
            "installed": True
        }
    db_tile = InstalledTile(tile_id=tile.tile_id, name=tile.name, installed=True, tile_metadata=tile.tile_metadata)
    db.add(db_tile)
    await db.commit()
    await db.refresh(db_tile)
    return {
        "_id": db_tile.tile_id,
        "installed": True
    }

@router.delete("/tiles/{tile_id}", status_code=200)
async def uninstall_tile(tile_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InstalledTile).where(InstalledTile.tile_id == tile_id))
    db_tile = result.scalar_one_or_none()
    if not db_tile:
        raise HTTPException(status_code=404, detail="Tile not found")
    await db.delete(db_tile)
    await db.commit()
    return {
        "_id": tile_id,
        "installed": False
    }
