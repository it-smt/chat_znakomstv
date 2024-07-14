import json
import logging
import random
from typing import List

from django.http import JsonResponse
from ninja import Router

from .bearers import AuthTokenBearer
from .schemas import UserSuccessLogin, UserFailedLogin, UserRegister, UserSuccessRegister, UserFailedRegister, \
    QuestionnaireSuccess, QuestionnaireFailed, CreateComplaint, CreateComplaintSuccess, CreateComplaintFailed, \
    FailedComplaints, ComplaintSchema
from ...models import User, Complaint

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
    user.gender = body.gender
    user.who_looking = body.who_looking
    user.set_password(f'{body.user_id}_{body.username}')
    user.save()
    return JsonResponse({'msg': 'Вы успешно зарегистрировались.', 'auth_token': user.auth_token}, safe=False,
                        status=201)


@router.get('random_questionnaire/', auth=AuthTokenBearer(),
            response={200: QuestionnaireSuccess, 404: QuestionnaireFailed})
def get_random_questionnaire(request):
    """Функция для получения случайной анкеты."""
    request_user = request.auth
    gender = User.Gender.MALE if request_user.who_looking == User.WhoLooking.MALE else User.Gender.FEMALE
    if request_user.who_looking == User.WhoLooking.ALL:
        gender = User.WhoLooking.ALL
    logger.debug(f'Мы ищем людей с гендером: {gender}')
    valid_age = [request_user.age - 1, request_user.age, request_user.age + 1]
    if gender != User.WhoLooking.ALL:
        users = User.objects.filter(age__in=valid_age, gender=gender, city=request_user.city).exclude(
            user_id=request_user.user_id)
    else:
        users = User.objects.filter(age__in=valid_age, city=request_user.city).exclude(
            user_id=request_user.user_id)
    if users:
        user = random.choices(users)[0]
        logger.debug(f'Вот пользователь, которой подходит под ваш запрос: {user}')
        return JsonResponse(dict(QuestionnaireSuccess.from_orm(user)), safe=False, status=200)


@router.post('create_complaint/', auth=AuthTokenBearer(),
             response={201: CreateComplaintSuccess, 400: CreateComplaintFailed})
def create_complaint(request, body: CreateComplaint):
    """Функция для создания жалобы на пользователя."""
    try:
        complaint = Complaint()
        complaint.user = User.objects.get(id=body.user)
        complaint.accused_user = User.objects.get(id=body.accused_user)
        complaint.description = body.description
        complaint.save()
    except Exception as e:
        return JsonResponse({'msg': e}, safe=False, status=400)
    return JsonResponse({'msg': f'Жалоба на пользователя {complaint.accused_user.first_name} успешно отправлена.'})


@router.get('get_complaints/', auth=AuthTokenBearer(), response={200: List[ComplaintSchema], 400: FailedComplaints})
def get_complaints(request):
    """Получает все жалобы."""
    try:
        complaints = list(
            Complaint.objects.all().values('user__username', 'accused_user__username', 'description', 'date_created'))
        print(complaints)
    except Exception as e:
        return JsonResponse({'msg': f'{type(e)}: {e}'}, safe=False, status=400)
    return JsonResponse(complaints, safe=False, status=200)
