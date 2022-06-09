from fastapi import HTTPException, Header
from uuid import UUID, uuid4
from models import Settings


settings = Settings()

async def verify_etag(etagH: UUID = Header("etag")):
    if settings.etag != etagH: 
        raise HTTPException(status_code=400, detail="Update your etag", headers= {"Etag" : str(settings.etag)})
    settings.etag = uuid4()

