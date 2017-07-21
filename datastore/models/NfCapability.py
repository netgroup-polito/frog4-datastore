from django.db import models


class NF_Capability(models.Model):
    capability_id = models.CharField(primary_key=True, unique=True, max_length=100)
    yang = models.ForeignKey('YANG_Models', on_delete=models.CASCADE, null=True)

# All 'Model' has to be added to __init__.py file. Check such file fore further information
