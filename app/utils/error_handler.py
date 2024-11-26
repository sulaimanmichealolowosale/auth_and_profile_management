from fastapi import HTTPException


def server_error(status_code, e) -> dict:
    raise HTTPException(
        status_code=status_code, detail=str(e))