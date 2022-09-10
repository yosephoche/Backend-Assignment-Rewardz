from django.db import models
from authentication.models import User


class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserAwareModel(Timestampable, models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True
