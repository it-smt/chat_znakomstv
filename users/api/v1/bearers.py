from typing import Optional, Any

from ninja.security import HttpBearer

from users.models import User


class AuthTokenBearer(HttpBearer):
    """Класс для проверки токена пользователя."""
    def authenticate(self, request, token: str) -> Optional[Any]:
        user = User.objects.filter(auth_token=token).first()
        if user is not None and token != '':
            return user
        return None
