from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from dependecy import get_auth_service
from schema.user import UserLoginSchema, UserCreateSchema
from service.auth import AuthService
from exception import UserNotFoundException, UserNotCorrectPasswordException

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
        return auth_service.login(body.username, body.password)
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