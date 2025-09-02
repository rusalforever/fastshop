from fastapi import APIRouter

from .user import router as _user_router
from .user_address import router as _address_router

router = APIRouter()
router.include_router(_user_router)
router.include_router(_address_router)

user_router = router
