from django.contrib import admin
from django.urls import path

from ninja import NinjaAPI

from users.api.v1.routes import router as users_router

api_v1 = NinjaAPI()
api_v1.add_router(router=users_router, prefix='accounts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', api_v1.urls)
]
