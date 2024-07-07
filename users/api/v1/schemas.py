from ninja import ModelSchema, Schema

from users.models import User


class UserLogin(ModelSchema):
    """Схема для авторизации пользователя."""

    class Meta:
        model = User
        fields = ('username', 'password')


class UserFailedLogin(Schema):
    """Схема ошибки при авторизации пользователя."""
    msg: str


class UserSuccessLogin(UserFailedLogin):
    """Схема успешной авторизации пользователя."""
    token: str


class UserRegister(Schema):
    """Схема для регистрации пользователя."""
    user_id: int
    username: str
    name: str
    age: int
    description: str | None
    city: str


class UserSuccessRegister(UserSuccessLogin):
    """Схема успешной регистрации пользователя."""
    pass


class UserFailedRegister(UserFailedLogin):
    """Схема ошибки при регистрации пользователя."""
    pass
