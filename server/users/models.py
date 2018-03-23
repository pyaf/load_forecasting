from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    college = models.TextField(null = True, blank=True)

    def __str__(self):
        return '%s-%s' % (self.user.first_name, self.college)
