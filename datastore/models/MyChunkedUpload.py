from django.db import models
from chunked_upload.models import ChunkedUpload


class My_ChunkedUpload(ChunkedUpload):
    vnf_id = models.CharField(unique=True, max_length=100)

# Override the default ChunkedUpload to make the `user` field nullable
My_ChunkedUpload._meta.get_field('user').null = True

# All 'Model' has to be added to __init__.py file. Check such file fore further information
