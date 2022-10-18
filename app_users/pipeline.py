from .models import Profile


def create_profile(backend, user, response, *args, **kwargs):
    """Создаёт профиль пользователя при создании аккаунта через Google"""
    try:
        Profile.objects.create(
            user=user,
        )
    except:
        pass
