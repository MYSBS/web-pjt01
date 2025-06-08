from django.apps import AppConfig
import os
import shutil


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        static_default = os.path.join('static', 'img', 'user_profile', 'default.png')
        media_default_dir = os.path.join('media', 'user_profile_img')
        media_default_file = os.path.join(media_default_dir, 'default.png')

        if not os.path.exists(media_default_file):
            os.makedirs(media_default_dir, exist_ok=True)
            shutil.copy(static_default, media_default_file)