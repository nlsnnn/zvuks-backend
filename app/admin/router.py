from fastapi import APIRouter

from app.admin.service import AdminService
from app.users.dependencies import CurrentAdminDep

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/block/{user_id}")
async def block_user(user_id: int, user: CurrentAdminDep):
    await AdminService.block_user(user_id, user)
    return {"message": "Пользователь заблокирован"}


@router.post("/unblock/{user_id}")
async def unblock_user(user_id: int, user: CurrentAdminDep):
    await AdminService.unblock_user(user_id, user)
    return {"message": "Пользователь разблокирован"}
