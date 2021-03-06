from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = _('users')

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass