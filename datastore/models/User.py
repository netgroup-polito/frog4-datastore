from django.db import models


class User(models.Model):
    user_id = models.CharField(primary_key=True, unique=True, max_length=100)
    broker_key = models.CharField(max_length=20000, blank=True)
    password = models.CharField(max_length=50, blank=False)
    token = models.CharField(max_length=200, blank=True, unique=True)

# All 'Model' has to be added to __init__.py file. Check such file fore further information
