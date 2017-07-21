from django.db import models


class NF_Template(models.Model):
    template_id = models.CharField(primary_key=True, unique=True, max_length=100)
    template = models.TextField(blank=False)
    capability = models.ForeignKey('NF_Capability', on_delete=models.CASCADE, blank=False)

# All 'Model' has to be added to __init__.py file. Check such file fore further information
