from django.db import models


class YANG_Models(models.Model):
    yang_id = models.CharField(primary_key=True, unique=True, max_length=100)
    yang_model = models.TextField()

# All 'Model' has to be added to __init__.py file. Check such file fore further information
