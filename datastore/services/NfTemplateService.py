import base64
import json
import random
import string
from django.db import transaction
from datastore.models import VNF_Image


def getVNFTemplate(vnf_id=None):
    if vnf_id is not None:
        vnf = VNF_Image.objects.filter(vnf_id=str(vnf_id))
    else:
        vnf = VNF_Image.objects.all()
        # Filter out templates with uncompleted images
        vnf = vnf.exclude(image_upload_status=VNF_Image.IN_PROGRESS)
        vnfList = []
        for foundVNF in vnf:
            newVNF = {}
            newVNF['id'] = foundVNF.vnf_id
            newVNF['template'] = json.loads(base64.b64decode(foundVNF.template))
            newVNF['image-upload-status'] = foundVNF.image_upload_status
            vnfList.append(newVNF)
        return {'list':vnfList}

    if len(vnf) != 0:
        return json.loads(base64.b64decode(vnf[0].template))
    return None


@transaction.atomic
def deleteVNFTemplate(vnf_id):
    vnf = VNF_Image.objects.filter(vnf_id=str(vnf_id))
    if len(vnf) != 0:
        vnf[0].delete()
        return True
    return False


def addVNFTemplate(vnf_id, template, capability):
    vnf = VNF_Image(vnf_id = str(vnf_id), template = base64.b64encode(template), capability=capability)
    vnf.save()


def addVNFTemplateV2(template, capability, image_upload_status):
    # Generate 6 chars alphanumeric nonce and verify its uniqueness
    while True:
        vnf_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
        vnf = VNF_Image.objects.filter(vnf_id=vnf_id)
        if len(vnf) == 0:
            break
    # Store the template
    vnf = VNF_Image(vnf_id = vnf_id, template = base64.b64encode(template), capability=capability, image_upload_status=image_upload_status)
    vnf.save()
    # Return the generated NF ID
    return vnf_id


@transaction.atomic
def updateVNFTemplate(vnf_id, template, capability):
    old_template = VNF_Image.objects.filter(vnf_id=vnf_id)
    if len(old_template) == 0:
        return False
    VNF_Image.objects.filter(vnf_id=str(vnf_id)).update(template=base64.b64encode(template), capability=capability)
    return True
