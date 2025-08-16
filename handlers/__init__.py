from .tasks import router as tasks_router
from .categories import router as categories_router
from .user import router as user_router
from .auth import router as auth_router

routers = [tasks_router, categories_router, user_router, auth_router] 