from django.apps import AppConfig


class web_appConfig(AppConfig): # 주의 뭔가 문제면 얘때문임
    default_auto_field = "django.db.models.BigAutoField"
    name = "web_app"
