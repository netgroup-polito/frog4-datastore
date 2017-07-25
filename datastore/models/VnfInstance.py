from django.db import models


class VNF_Instance(models.Model):
    vnf_instance_id = models.CharField(primary_key=True, unique=True, max_length=100)
    bootstrap_configuration = models.ForeignKey('NF_Configuration', blank=False, null=True)
    restEndpoint = models.CharField(max_length=1000, blank=True)

# All 'Model' has to be added to __init__.py file. Check such file fore further information
