import base64
import json
from django.db import transaction
from rest_framework.parsers import ParseError
from datastore.models import VNF


def getAllVNFs():
    vnf = VNF.objects.all()
    vnfList = []
    for foundVnf in vnf:
        newVnf = {}
        config = base64.b64decode(foundVnf.bootstrap_configuration).decode('utf-8')
        if config != "":
            config = json.loads(config)
        newVnf['configuration id'] = foundVnf.configuration_id
        newVnf['boot configuration'] = config
        newVnf['rest endpoint'] = foundVnf.restEndpoint
        vnfList.append(newVnf)
    if len(vnfList) != 0:
        return {'list': vnfList}
    return None


def getVNF(configuration_id):
    foundVNF = VNF.objects.filter(configuration_id=configuration_id)
    if len(foundVNF) == 0:
        return None
    newVnf = {}
    config = base64.b64decode(foundVNF[0].bootstrap_configuration).decode('utf-8')
    if config != "":
        config = json.loads(config)
    newVnf['configuration id'] = foundVNF[0].configuration_id
    newVnf['boot configuration'] = config
    newVnf['rest endpoint'] = foundVNF[0].restEndpoint
    return newVnf


@transaction.atomic
def addVNF(configuration_id):
    vnf= VNF.objects.filter(configuration_id=configuration_id)
    if len(vnf) > 0:
        return False
    vnf = VNF(configuration_id=configuration_id)
    vnf.save()
    return True


@transaction.atomic
def deleteVNF(configuration_id):
    vnf = VNF.objects.filter(configuration_id=configuration_id)
    if len(vnf) != 0:
        vnf[0].delete()
        return True
    return False


# VNF Booting configuration API
def getBootConfig(configuration_id):
    foundVNF = VNF.objects.filter(configuration_id=configuration_id)
    if len(foundVNF) == 0:
        return None
    config = base64.b64decode(foundVNF[0].bootstrap_configuration).decode('utf-8')
    return config


@transaction.atomic
def deleteBootConfig(configuration_id):
    vnf = VNF.objects.filter(configuration_id=configuration_id)
    if len(vnf) != 0 and vnf[0].bootstrap_configuration != "":
        vnf.update(bootstrap_configuration="")
        return True
    return False


@transaction.atomic
def updateBootConfig(configuration_id, configuration):
    if configuration is None:
        raise ParseError(detail="No configuration was provided")
    vnf = VNF.objects.filter(configuration_id=configuration_id)
    if len(vnf) == 0:
        return False
    vnf.update(bootstrap_configuration=base64.b64encode(configuration))
    return True



#VNF REST endpoint
def getRESTEndpoint(configuration_id):
    foundVNF = VNF.objects.filter(configuration_id=configuration_id)
    if len(foundVNF) == 0:
        return None
    rest_endpoint = foundVNF[0].restEndpoint
    return rest_endpoint


def putRESTEndpoint(configuration_id, rest_endpoint):
    foundVNF= VNF.objects.filter(configuration_id=configuration_id)
    if len(foundVNF) == 0:
        return False
    foundVNF.update(restEndpoint=rest_endpoint)
    return True


def deleteRESTEndpoint(configuration_id):
    vnf = VNF.objects.filter(configuration_id=configuration_id)
    if len(vnf) != 0:
        if vnf[0].restEndpoint != "":
            vnf.update(restEndpoint="")
            return True
    return False
