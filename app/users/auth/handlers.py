from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from typing import Annotated

from app.dependency import get_auth_service
from app.users.user_profile.schema import UserLoginSchema, UserCreateSchema
from app.users.auth.service import AuthService
from app.exception import UserNotFoundException, UserNotCorrectPasswordException

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post(
    '/login',
    response_model=UserLoginSchema,
    responses={
        401: {"description": "Invalid credentials"},
        404: {"description": "User not found"}
    }
)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        return await auth_service.login(body.username, body.password)
    except UserNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    except UserNotCorrectPasswordException:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )
    

@router.get(
    '/login/google',
    response_class=RedirectResponse
)

async def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_google_redirect_url()
    return RedirectResponse(redirect_url)


@router.get(
    '/google',
)

async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    return await auth_service.google_auth(code=code)


@router.get(
    '/login/yandex',
    response_class=RedirectResponse
)

async def yandex_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_yandex_redirect_url()
    return RedirectResponse(redirect_url)


@router.get(
    '/yandex'
)

async def yandex_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    return await auth_service.yandex_auth(code=code)
    
