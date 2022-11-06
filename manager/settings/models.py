from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Settings(models.Model):
    currency = models.CharField(max_length=30, blank=True, null=True, default="$")
    limit = models.FloatField(default=0, blank=True)
    user = models.ForeignKey(User, related_name='settings', on_delete=models.SET_NULL, null=True)
