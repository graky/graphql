from django.contrib.auth.admin import UserAdmin
from work.models import User, Vacancy, Candidate, Recruiter, Employer
from django.contrib import admin
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


class SettingsBackend(BaseBackend):
    """Данная реализация решает вопрос jwt токена."""

    """Переопределяем метод. Описываем авторизацию."""
    """Отсееваем юзеров с мобилы, у мобильных узеров пароля нет"""
    """В случае каких то исключений или применения сплоитов при авторизации отсееваем """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.get(username=username)
        if user.password == password:
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


admin.site.register(Vacancy)
admin.site.register(Candidate)
admin.site.register(Recruiter)
admin.site.register(Employer)
# Register your models here.
