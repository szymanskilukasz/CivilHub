from django.apps import AppConfig
from actstream import registry

class ProjectStreamConfig(AppConfig):
    name = 'projects'

    def ready(self):
        registry.register(self.get_model('SocialProject'))
