from typing import Annotated

from fastapi import Header, HTTPException


def verify_access_token(x_token: Annotated[str | None, Header()] = None):
    if not x_token:
        raise HTTPException(status_code=403, detail="Insufficient security clearance")
    if x_token != 'siriyetu':
        raise HTTPException(status_code=403, detail="Invalid access token")