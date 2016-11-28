from django.db import models
class VNF(models.Model):
	vnf_id = models.CharField(primary_key=True, unique=True,max_length=100)
	template = models.CharField(max_length=60000,blank=False)
"""
class NFFG(models.Model):
	nffg_id = models.CharField(primary_key=True, unique=True,max_length=100)
	template = models.CharField(max_length=60000,blank=False)
"""
class NF_FGraphs(models.Model):
	nf_fgraphs_id = models.CharField(primary_key=True, unique=True,max_length=100)
	nf_fgraphs_template = models.TextField()