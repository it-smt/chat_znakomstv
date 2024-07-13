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
    who_looking: str
    gender: str


class UserSuccessRegister(UserSuccessLogin):
    """Схема успешной регистрации пользователя."""
    pass


class UserFailedRegister(UserFailedLogin):
    """Схема ошибки при регистрации пользователя."""
    pass


class QuestionnaireSuccess(ModelSchema):
    """Схема успешного получения анкеты."""
    id: int
    user_id: int
    username: str
    first_name: str
    age: int
    description: str
    city: str

    class Meta:
        model = User
        fields = ['id', 'user_id', 'username', 'first_name', 'age', 'description', 'city']


class QuestionnaireFailed(Schema):
    """Схема неудачного получения анкеты."""
    msg: str
