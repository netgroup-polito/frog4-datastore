import base64
import json
from django.db import transaction
from datastore.models.NfTemplate import NF_Template
from datastore.models.NfCapability import NF_Capability
from datastore.services import YangService


'''
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
'''
def getTemplatesFromCapability(capability_id):
    capability = NF_Capability.objects.filter(capability_id=capability_id)
    if len(capability) == 0:
        return None

    template = NF_Template.objects.filter(capability=str(capability_id))
    if len(template) == 0:
        return None
    templateList = []
    for foundTemplate in template:
        newTemplate = {}
        newTemplate['id'] = foundTemplate.template_id
        newTemplate['template'] = json.loads(base64.b64decode(foundTemplate.template))
        newTemplate['capability-id'] = foundTemplate.capability.capability_id
        templateList.append(newTemplate)
    return {'list': templateList}


def getAllCapabilities():
    capabilities = NF_Capability.objects.all()
    if len(capabilities) == 0:
        return {'list': []}

    capability_list = []
    for found_capability in capabilities:
        new_capability = {}
        yang_id = ""
        if found_capability.yang is not None:
            yang_id = found_capability.yang.yang_id
        new_capability['name'] = found_capability.capability_id
        new_capability['yang_model_id'] = yang_id
        capability_list.append(new_capability)
    return {'list': capability_list}


@transaction.atomic
def addCapability(capability_id, yang_id=None):
    capability = NF_Capability.objects.filter(capability_id=capability_id)
    if len(capability) != 0:
        return capability[0]

    yang_model = YangService.getYangModelObj(yang_id)
    capability = NF_Capability(capability_id=capability_id, yang=yang_model)
    capability.save()
    return capability

@transaction.atomic
def deleteCapability(capability_id):
    capability = NF_Capability.objects.filter(capability_id=capability_id)
    if len(capability) != 0:
        capability[0].delete()
        return True
    return False