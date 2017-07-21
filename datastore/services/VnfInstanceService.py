from django.db import transaction
from datastore.models.VnfInstance import VNF_Instance
from datastore.services import NfConfigurationService


def getAllVNFs():
    vnf = VNF_Instance.objects.all()
    vnf_list = []
    for found_vnf in vnf:
        new_vnf = {}
        bootstrap_configuration_id = ""
        if found_vnf.bootstrap_configuration is not None:
            bootstrap_configuration_id = found_vnf.bootstrap_configuration.configuration_id
        new_vnf['instance id'] = found_vnf.vnf_instance_id
        new_vnf['boot configuration id'] = bootstrap_configuration_id
        new_vnf['rest endpoint'] = found_vnf.restEndpoint
        vnf_list.append(new_vnf)
    if len(vnf_list) != 0:
        return {'list': vnf_list}
    return {'list': []}


def getVNF(instance_id):
    found_vnf = VNF_Instance.objects.filter(vnf_instance_id=instance_id)
    if len(found_vnf) == 0:
        return None
    new_vnf = {}
    bootstrap_configuration_id = ""
    if found_vnf[0].bootstrap_configuration is not None:
        bootstrap_configuration_id = found_vnf[0].bootstrap_configuration.configuration_id
    new_vnf['instance id'] = found_vnf[0].vnf_instance_id
    new_vnf['boot configuration id'] = bootstrap_configuration_id
    new_vnf['rest endpoint'] = found_vnf[0].restEndpoint
    return new_vnf


@transaction.atomic
def addVNF(instance_id):
    vnf= VNF_Instance.objects.filter(vnf_instance_id=instance_id)
    if len(vnf) > 0:
        return False
    vnf = VNF_Instance(vnf_instance_id=instance_id)
    vnf.save()
    return True


@transaction.atomic
def deleteVNF(instance_id):
    vnf = VNF_Instance.objects.filter(vnf_instance_id=instance_id)
    if len(vnf) != 0:
        vnf[0].delete()
        return True
    return False


# VNF Booting configuration API
def getBootConfig(instance_id):
    foundVNF = VNF_Instance.objects.filter(vnf_instance_id=instance_id)
    if len(foundVNF) == 0:
        return None, "The vnf with ID " + instance_id + " does not exist"
    config = foundVNF[0].bootstrap_configuration
    if config is None:
        return None, ""
    config_dict = {}
    config_dict['configuration-id'] = config.configuration_id
    config_dict['username'] = config.user.user_id
    return config_dict, "Ok"


@transaction.atomic
def deleteBootConfig(instance_id):
    vnf = VNF_Instance.objects.filter(vnf_instance_id=instance_id)
    if len(vnf) != 0 and vnf[0].bootstrap_configuration != None:
        vnf.update(bootstrap_configuration=None)
        return True
    return False


@transaction.atomic
def updateBootConfig(instance_id, configuration_id, user_id):
    vnf = VNF_Instance.objects.filter(vnf_instance_id=instance_id)
    if len(vnf) == 0:
        return False, "The vnf with ID " + instance_id + " does not exist"
    configuration = NfConfigurationService.getConfigurationObject(user_id=user_id, configuration_id=configuration_id)
    if configuration is None:
        return False, "The configuration with ID (configuration_id, user_id): (" + configuration_id + "," + user_id + ") does not exist"
    vnf.update(bootstrap_configuration=configuration)
    return True, "Ok"



#VNF REST endpoint
def getRESTEndpoint(instance_id):
    foundVNF = VNF_Instance.objects.filter(vnf_instance_id=instance_id)
    if len(foundVNF) == 0:
        return None
    rest_endpoint = foundVNF[0].restEndpoint
    return rest_endpoint


@transaction.atomic
def putRESTEndpoint(instance_id, rest_endpoint):
    foundVNF= VNF_Instance.objects.filter(vnf_instance_id=instance_id)
    if len(foundVNF) == 0:
        return False
    foundVNF.update(restEndpoint=rest_endpoint)
    return True


@transaction.atomic
def deleteRESTEndpoint(instance_id):
    vnf = VNF_Instance.objects.filter(vnf_instance_id=instance_id)
    if len(vnf) != 0:
        if vnf[0].restEndpoint != "":
            vnf.update(restEndpoint="")
            return True
    return False
