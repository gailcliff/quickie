
from fastapi import APIRouter

router = APIRouter(
    prefix='/woke',
    tags=['woke'],
    responses={
        404: {
            "model": None,
            "media_type": "application/json",
            "headers": {"Content-Type": "application/json"},
            "status_code": 404,
            "description": "Nun nigga"
            },
        }
)


@router.get('/')
def get_woke_users():
    return ['g', 'q', 't', 'b', 'l']
    # raise HTTPException(status_code=404)
