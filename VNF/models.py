from django.db import models
class VNF(models.Model):
	vnf_id = models.CharField(primary_key=True, unique=True,max_length=100)
	template = models.CharField(max_length=60000,blank=False)
