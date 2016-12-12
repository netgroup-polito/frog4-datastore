from django.db import models
from chunked_upload.models import ChunkedUpload

class MyChunkedUpload(ChunkedUpload):
    pass
# Override the default ChunkedUpload to make the `user` field nullable
MyChunkedUpload._meta.get_field('user').null = True

class VNF(models.Model):
	vnf_id = models.CharField(primary_key=True, unique=True,max_length=100)
	template = models.CharField(max_length=60000,blank=False)
	capability = models.CharField(max_length=600)

class NF_FGraphs(models.Model):
	nf_fgraphs_id = models.CharField(primary_key=True, unique=True,max_length=100)
	nf_fgraphs_template = models.TextField()
