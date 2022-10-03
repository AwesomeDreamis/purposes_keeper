from .models import Profile

def create_profile(backend, user, response, *args, **kwargs):
    try:
        Profile.objects.create(
            user=user,
        )
    except:
        pass
