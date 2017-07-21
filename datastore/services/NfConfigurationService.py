import base64
import json
from django.db import transaction
from datastore.models.NfConfiguration import NF_Configuration
from datastore.models.Yang import YANG_Models
from datastore.models.User import User


def getConfigurationsByUser(user_id):
    configurations = NF_Configuration.objects.filter(user=user_id)
    configuration_list = []
    for found_configuration in configurations:
        new_configuration = {}
        configuration = base64.b64decode(found_configuration.configuration).decode('utf-8')
        new_configuration['configuration id'] = found_configuration.configuration_id
        new_configuration['user'] = found_configuration.user.user_id
        new_configuration['configuration'] = json.loads(configuration)
        new_configuration['yang id'] = found_configuration.yang.yang_id
        configuration_list.append(new_configuration)
    if len(configuration_list) != 0:
        return {'list': configuration_list}
    return {'list': []}


def getConfiguration(user_id, configuration_id):
    found_configuration= NF_Configuration.objects.filter(user=user_id, configuration_id=configuration_id)
    if len(found_configuration) == 0:
        return None
    new_configuration = {}
    configuration = base64.b64decode(found_configuration[0].configuration).decode('utf-8')
    new_configuration['configuration id'] = found_configuration[0].configuration_id
    new_configuration['user'] = found_configuration[0].user.user_id
    new_configuration['configuration'] = json.loads(configuration)
    new_configuration['yang id'] = found_configuration[0].yang.yang_id

    return new_configuration


@transaction.atomic
def addConfiguration(user_id, configuration_id, configuration, yang_id):
    user = User.objects.filter(user_id=user_id)
    if len(user) == 0:
        raise Exception("User " + user_id + " does not exist")
    yang = YANG_Models.objects.filter(yang_id=yang_id)
    if len(yang) == 0:
        raise Exception("Yang models " + yang_id + " does not exist")

    conf = NF_Configuration.objects.filter(user=user_id)
    if len(conf) > 0:
        return False

    conf = NF_Configuration(user=user[0], configuration_id=configuration_id, configuration= base64.b64encode(configuration), yang=yang[0])
    conf.save()
    return True


@transaction.atomic
def updateConfiguration(user_id, configuration_id, configuration):
    conf = NF_Configuration.objects.filter(user=user_id, configuration_id=configuration_id)
    if len(conf) == 0:
        return False
    NF_Configuration.objects.filter(user=user_id).filter(configuration_id=configuration_id).update(configuration=base64.b64encode(configuration))
    return True


@transaction.atomic
def deleteConfiguration(user_id, configuration_id):
    print("delete: user - conf_id " + user_id + " " + configuration_id)
    configuration = NF_Configuration.objects.filter(user=user_id, configuration_id=configuration_id)
    if len(configuration) != 0:
        configuration[0].delete()
        return True
    return False


def getConfigurationObject(user_id, configuration_id):
    """
        Returns the configuration object of the configuration of the given user_id and configuration_id
        :param user_id:
        :param configuration_id:
        :return: None if no configuration is found
    """
    found_configuration = NF_Configuration.objects.filter(user=user_id, configuration_id=configuration_id)
    if len(found_configuration) == 0:
        return None
    return found_configuration[0]