import logging

from django.http import JsonResponse
from ninja import Router

from .schemas import UserLogin, UserSuccessLogin, UserFailedLogin, UserRegister, UserSuccessRegister, UserFailedRegister
from users.models import User

router = Router()

logger = logging.getLogger('main')


@router.post('login/', response={200: UserSuccessLogin, 401: UserFailedLogin})
def login_user(request, user_id: int):
    """Функция авторизации пользователя в телеграмме."""
    try:
        user = User.objects.get(user_id=user_id)
        return JsonResponse({'msg': 'Вы успешно авторизовались.', 'auth_token': user.auth_token}, safe=False,
                            status=200)
    except User.DoesNotExist:
        return JsonResponse({'msg': 'Нет пользователя с таким user_id'}, safe=False, status=404)


@router.post('register/', response={201: UserSuccessRegister, 400: UserFailedRegister})
def register_user(request, body: UserRegister):
    """Функция регистрации пользователя."""
    user = User()
    user.user_id = body.user_id
    user.username = body.username
    user.first_name = body.name
    user.age = body.age
    user.description = body.description
    user.city = body.city
    user.set_password(f'{body.user_id}_{body.username}')
    user.save()
    return JsonResponse({'msg': 'Вы успешно зарегистрировались.', 'auth_token': user.auth_token}, safe=False,
                        status=201)
