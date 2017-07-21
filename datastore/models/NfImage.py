from django.db import models


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
    template = models.ForeignKey('NF_Template', on_delete=models.CASCADE, blank=False)
    image_upload_status = models.CharField(
        max_length=2,
        choices=IMAGE_UPLOAD_STATUS,
        default=COMPLETED
    )

# All 'Model' has to be added to __init__.py file. Check such file fore further information
