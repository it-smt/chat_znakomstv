from datetime import datetime
from typing import List

from ninja import ModelSchema, Schema

from ...models import User, Complaint


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


class CreateComplaint(ModelSchema):
    """Схема для создания жалобы."""
    user: int
    accused_user: int
    description: str | None

    class Meta:
        model = Complaint
        fields = ['user', 'accused_user', 'description']


class CreateComplaintSuccess(Schema):
    """Схема успешного создания жалобы."""
    msg: str


class CreateComplaintFailed(CreateComplaintSuccess):
    """Схема неудачного создания жалобы."""
    pass


class ComplaintSchema(Schema):
    """Схема жалобы."""
    user__username: str
    accused_user__username: str
    description: str | None
    date_created: datetime


class FailedComplaints(Schema):
    msg: str
