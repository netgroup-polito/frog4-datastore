from django.db import models
from chunked_upload.models import ChunkedUpload


class MyChunkedUpload(ChunkedUpload):
    vnf_id = models.CharField(unique=True, max_length=100)


# Override the default ChunkedUpload to make the `user` field nullable
MyChunkedUpload._meta.get_field('user').null = True


class VNF_Image(models.Model):
    IN_PROGRESS = 'IP'
    COMPLETED = 'CO'
    REMOTE = 'RE'
    IMAGE_UPLOAD_STATUS = (
        (IN_PROGRESS, 'In progress'),
        (COMPLETED, 'Completed'),
        (REMOTE, 'Remote')
    )
    vnf_id = models.CharField(primary_key=True, unique=True, max_length=100)
    template = models.CharField(max_length=60000, blank=False)
    capability = models.CharField(max_length=600)
    image_upload_status = models.CharField(
        max_length=2,
        choices=IMAGE_UPLOAD_STATUS,
        default=COMPLETED
    )


class User(models.Model):
    user_id = models.CharField(primary_key=True, unique=True, max_length=100)
    broker_key = models.CharField(max_length=20000, blank=False)


class NF_FGraphs(models.Model):
#    VOLATILITYCHOICE = (
#        ('t', 'Temporary'),
#        ('p', 'Permanent')
#    )

    user_id = models.CharField(max_length=100)
    nf_fgraph_id = models.CharField(primary_key=True, unique=True, max_length=100)
    nffg = models.TextField()
#    volatility = models.CharField(max_length=1, choices=VOLATILITYCHOICE)

    class Meta:
        unique_together = ("user_id", "nf_fgraph_id")


class VNF(models.Model):
    configuration_id = models.CharField(primary_key=True, unique=True, max_length=100)
    bootstrap_configuration = models.CharField(max_length=20000, blank=True)
    restEndpoint = models.CharField(max_length=1000, blank=True)


class YANG_Models(models.Model):
    yang_id = models.CharField(primary_key=True, unique=True, max_length=100)
    yang_model = models.TextField()
