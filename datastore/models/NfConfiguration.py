from django.db import models


class NF_Configuration(models.Model):
    configuration_id = models.CharField(primary_key=True, unique=True, max_length=100)
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=False)
    configuration = models.TextField(max_length=80000, blank=False)
    yang = models.ForeignKey('YANG_Models', on_delete=models.CASCADE, blank=False)

    class Meta:
        unique_together = ("configuration_id", "user")

# All 'Model' has to be added to __init__.py file. Check such file fore further information
