import base64
import json
import random
import string
from django.db import transaction
from datastore.models.NfTemplate import NF_Template
import datastore.services.NfCapabilityService as CapabilityApi


def getVNFTemplate(template_id=None):
    if template_id is not None:
        template = NF_Template.objects.filter(template_id=str(template_id))
    else:
        template = NF_Template.objects.all()
        templateList = []
        for foundTemplate in template:
            newTemplate = {}
            newTemplate['id'] = foundTemplate.template_id
            newTemplate['template'] = json.loads(base64.b64decode(foundTemplate.template))
            newTemplate['capability'] = foundTemplate.capability.capability_id
            templateList.append(newTemplate)
        return {'list':templateList}

    if len(template) != 0:
        return json.loads(base64.b64decode(template[0].template))
    return None


@transaction.atomic
def deleteVNFTemplate(template_id):
    template = NF_Template.objects.filter(template_id=str(template_id))
    if len(template) != 0:
        capability = template.capability.capability_id
        template[0].delete()
        template = NF_Template.objects.filter(capability=capability)
        if len(template) == 0:
            CapabilityApi.deleteCapability(capability)
        return True
    return False


def addVNFTemplate(template_id, template, capability):
    template = NF_Template(template_id = str(template_id), template = base64.b64encode(template), capability=capability)
    template.save()


@transaction.atomic
def addVNFTemplateV2(template):
    """
    This method add a template into the database. It supposes the template to contains the 'functional-capability' key
    If the capability does not already exists into the DB, it is created
    :param template:
    :return:
    """
    yang_id = None
    if 'uri-yang' in template:
        yang_uri = template['uri-yang']
        #I can find the yang_id at the end of the uri-yang string. (e.g. http://127.0.0.1:8080/yang/5)
        yang_id = yang_uri[yang_uri.rfind('/') + 1:len(yang_uri)]
    capability = template['functional-capability']
    capability_obj = CapabilityApi.addCapability(capability, yang_id)
    if capability_obj is None:
        raise Exception("Error during capability creation (" + capability + ")")

    # Generate 6 chars alphanumeric nonce and verify its uniqueness
    while True:
        template_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
        templateFound = NF_Template.objects.filter(template_id=template_id)
        if len(templateFound) == 0:
            break
    # Store the template
    template = NF_Template(template_id=template_id, template=base64.b64encode(json.dumps(template)), capability=capability_obj)
    template.save()

    # Return the generated NF ID
    return template_id


@transaction.atomic
def updateVNFTemplate(template_id, template, capability):
    old_template = NF_Template.objects.filter(template_id=template_id)
    if len(old_template) == 0:
        return False
    NF_Template.objects.filter(template_id=str(template_id)).update(template=base64.b64encode(template), capability=capability)
    return True


def getTemplateObject(template_id):
    template = NF_Template.objects.filter(template_id=template_id)
    if len(template) == 0:
        return None
    return template[0]
