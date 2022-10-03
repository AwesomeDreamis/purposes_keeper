from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppGoalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_goals'
    verbose_name = _('goals')
