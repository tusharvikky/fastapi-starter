from fastapi import Request, Header, HTTPException
from core.db import session
from app.models import Team


class AppOrigin:
    def __init__(self, app_origin: int = Header(None)):

        if not app_origin:
            raise HTTPException(status_code=422, detail="App-Origin header invalid")

        tenant = session.query(Team).filter(Team.id==app_origin).first()
        session.info['tenant'] = tenant
        
