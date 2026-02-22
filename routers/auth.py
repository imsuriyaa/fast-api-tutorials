from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get('/')
def read_root():
    return {"message": "Hello World"}