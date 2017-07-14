import base64
import json
from datastore.models import VNF_Image, VNF


def getTemplatesFromCapability(vnfCapability):
    vnf = VNF_Image.objects.filter(capability=str(vnfCapability))
    # Filter out templates with uncompleted images
    vnf = vnf.exclude(image_upload_status=VNF_Image.IN_PROGRESS)
    if len(vnf) == 0:
        return None
    vnfList = []
    for foundVNF in vnf:
        newVNF = {}
        newVNF['id'] = foundVNF.vnf_id
        newVNF['template'] = json.loads(base64.b64decode(foundVNF.template))
        newVNF['image-upload-status'] = foundVNF.image_upload_status
        vnfList.append(newVNF)
    return {'list': vnfList}

