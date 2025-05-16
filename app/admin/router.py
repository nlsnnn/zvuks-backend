from fastapi import APIRouter, HTTPException

from app.admin.exceptions import AdminException
from app.admin.service import AdminService
from app.users.dependencies import CurrentAdminDep

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/block/{user_id}")
async def block_user(user_id: int, user: CurrentAdminDep):
    try:
        await AdminService.block_user(user_id, user)
        return {"message": "Пользователь заблокирован"}
    except AdminException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/unblock/{user_id}")
async def unblock_user(user_id: int, user: CurrentAdminDep):
    try:
        await AdminService.unblock_user(user_id, user)
    except AdminException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
