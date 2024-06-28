from datetime import timedelta
from typing import (
    Annotated,
    Any,
)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.security import OAuth2PasswordRequestForm

from src.authentication import security
from src.authentication.models import (
    Token, PasswordModel,
)
from src.authentication.routes import (
    AuthRoutesPrefixes,
)
from src.authentication.security import get_password_hash
from src.base_settings import base_settings
from src.users.services import (
    get_user_service,
)

router = APIRouter()


@router.post(AuthRoutesPrefixes.token, response_model=Token)
async def get_token(
        service: Annotated[get_user_service, Depends()],
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await service.authenticate(email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=base_settings.auth.access_token_expire_minutes)

    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires,
        ),
        "token_type": "bearer",
    }


@router.post("/hash-password/")
async def hash_password(password_model: PasswordModel):
    password = password_model.password
    hashed_password = get_password_hash(password)
    return {"hashed_password": hashed_password}
