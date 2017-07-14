from datastore.models import VNF_Image, User, NF_FGraphs, VNF, YANG_Models
import base64
import uuid
import json
import random
import string
from datastore.YANGtoYIN import create_yin
from rest_framework.parsers import ParseError
from django.db import transaction

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


@transaction.atomic
def deleteVNFTemplate(vnf_id):
    vnf = VNF_Image.objects.filter(vnf_id=str(vnf_id))
    if len(vnf) != 0:
        vnf[0].delete()
        return True
    return False


def addVNFTemplate(vnf_id, template, capability):
    vnf = VNF(vnf_id = str(vnf_id), template = base64.b64encode(template), capability=capability)
    vnf.save()


def addVNFTemplateV2(template, capability, image_upload_status):
    # Generate 6 chars alphanumeric nonce and verify its uniqueness
    while True:
        vnf_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
        vnf = VNF_Image.objects.filter(vnf_id=vnf_id)
        if len(vnf) == 0:
            break
    # Store the template
    vnf = VNF(vnf_id = vnf_id, template = base64.b64encode(template), capability=capability, image_upload_status=image_upload_status)
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


'''
NFFG API
'''
@transaction.atomic
def addNF_FGraphs(user_id, nffg):
    found_user = User.objects.filter(user_id=user_id)
    if len(found_user) == 0:
        return None;
    while True:
        new_nffg_uuid = uuid.uuid4()
        graph = NF_FGraphs.objects.filter(nf_fgraph_id=str(new_nffg_uuid))
        if len(graph) == 0:
            nf_fgraph_id = str(new_nffg_uuid)
            break
    graphs = NF_FGraphs(user_id= str(user_id), nf_fgraph_id = str(nf_fgraph_id), nffg = base64.b64encode(nffg))
    graphs.save()
    return nf_fgraph_id


@transaction.atomic
def updateNF_FGraphs(user_id, nf_fgraph_id, nffg):
    foundNffg = NF_FGraphs.objects.filter(user_id =user_id).filter(nf_fgraph_id=nf_fgraph_id)
    if len(nffg) == 0:
        return False
    foundNffg.update(nffg = base64.b64encode(nffg))
    return True


def getNF_FGraphs(user_id=None, nf_fgraph_id=None):
    if nf_fgraph_id is not None and user_id is not None:
        nf_fgraphs = NF_FGraphs.objects.filter(user_id=str(user_id)).filter(nf_fgraph_id=str(nf_fgraph_id))
        if len(nf_fgraphs) == 0:
            return None
        return json.loads(base64.b64decode(nf_fgraphs[0].nffg))

    else:
        nf_fgraphs = NF_FGraphs.objects.all()
        if len(nf_fgraphs) == 0:
            return None
        graphs = []
        for foundnf_fgraphs in nf_fgraphs:
            graph = {}
            graph['user id'] = foundnf_fgraphs.user_id
            graph['nffg-uuid'] = foundnf_fgraphs.nf_fgraph_id
            graph['forwarding-graph'] = json.loads(base64.b64decode(foundnf_fgraphs.nffg))['forwarding-graph']
            graphs.append(graph)
        return {'NF-FG': graphs }


@transaction.atomic
def deleteNF_FGraphs(user_id, nf_fgraph_id):
    print("delete")
    graph = NF_FGraphs.objects.filter(user_id=str(user_id), nf_fgraph_id=str(nf_fgraph_id))
    if len(graph) != 0:
        graph[0].delete()
        return True
    return False


def getnffg_digest():
    nf_fgraphs = NF_FGraphs.objects.all()
    nf_fgraphsList = []
    for foundnf_fgraph in nf_fgraphs:
        nf_fgraphs_digest = {}
        newnf_fgraphs = json.loads(base64.b64decode(foundnf_fgraph.nffg))['forwarding-graph']
        print("name: " + newnf_fgraphs['name'])
        if 'name' in newnf_fgraphs.keys():
            nf_fgraphs_digest['name'] = newnf_fgraphs['name']
        nf_fgraphs_digest['nffg-uuid'] = foundnf_fgraph.nf_fgraph_id
        nf_fgraphsList.append(nf_fgraphs_digest)
    if len(nf_fgraphs) != 0:
        return {'NF-FG': nf_fgraphsList}
    return None


def getNFFGByUser(user_id):
    nffgs = NF_FGraphs.objects.filter(user_id=user_id)
    nffgsList = []
    for foundNffg in nffgs:
        newNffg = {}
        nffg = base64.b64decode(foundNffg.nffg).decode('utf-8')
        newNffg['user id'] = foundNffg.user_id
        newNffg['nffg-uuid'] = foundNffg.nf_fgraph_id
        newNffg['forwarding-graph'] = json.loads(nffg)
        nffgsList.append(newNffg)
    if len(nffgsList) != 0:
        return {'list': nffgsList}
    return None


'''
YANG models API
'''
def getAllYANG_model():
    yang = YANG_Models.objects.all()
    yangList = []
    for foundYang in yang:
        newYANGModel = {}
        model = base64.b64decode(foundYang.yang_model).decode('utf-8')
        newYANGModel['id'] = foundYang.yang_id
        newYANGModel['model'] = model
        yangList.append(newYANGModel)
    if len(yangList) != 0:
        return {'list': yangList}
    return None


def getYANG_model(yang_id):
    yang = YANG_Models.objects.filter(yang_id=yang_id)
    if len(yang) == 0:
        return None
    model = base64.b64decode(yang[0].yang_model).decode('utf-8')
    return model


def getYINFromYangID(yang_id):
    yang = getYANG_model(yang_id)
    if yang is not None:
        yang = create_yin(str(yang))
    else:
        return None
    return json.loads(yang)


@transaction.atomic
def addYANG_model(yang_id, yang_model):
    if yang_model == {}:
        raise ParseError(detail="no yang was provided") #the empty case is managed in such a way because django don't pass an empty body to the parser
    yang = YANG_Models(yang_id=yang_id, yang_model=base64.b64encode(yang_model))
    yang.save()


@transaction.atomic
def deleteYANG_model(yang_id):
    yang = YANG_Models.objects.filter(yang_id=yang_id)
    if len(yang) != 0:
        yang[0].delete()
        return True
    return False


@transaction.atomic
def updateYANG_model(yang_id, yang_model):
    yang = YANG_Models.objects.filter(yang_id=yang_id)
    if len(yang) == 0:
        return False
    YANG_Models.objects.filter(yang_id=yang_id).update(yang_model=base64.b64encode(yang_model))
    return True

'''''''''''''''''''''''''''''''''''''''
                User API
'''''''''''''''''''''''''''''''''''''''


def getAllUser():
    user = User.objects.all()
    userList = []
    for foundUser in user:
        newUser = {}
        keys = base64.b64decode(foundUser.broker_key).decode('utf-8')
        newUser['id'] = foundUser.user_id
        newUser['key'] = json.loads(keys)
        userList.append(newUser)
    if len(userList) != 0:
        return {'list': userList}
    return None


def getUser(user_id):
    found_user = User.objects.filter(user_id=user_id)
    if len(found_user) == 0:
        return None
    newUser = {}
    keys = base64.b64decode(found_user[0].broker_key).decode('utf-8')
    newUser['id'] = found_user[0].user_id
    newUser['key'] = json.loads(keys)

    return newUser


@transaction.atomic
def addUser(user_id, broker_keys):
    user = User.objects.filter(user_id=user_id)
    if len(user) > 0:
        return False

    user = User(user_id=user_id, broker_key= base64.b64encode(broker_keys))
    user.save()
    return True


@transaction.atomic
def deleteUser(user_id):
    user = User.objects.filter(user_id=user_id)
    if len(user) != 0:
        user[0].delete()
        return True
    return False


'''''''''''''''''''''''''''''''''''''''
                Graph API
'''''''''''''''''''''''''''''''''''''''

'''
def getAllGraph():
    graph = NF_FGraphs.objects.all()
    graphList = []
    for foundGraph in graph:
        newGraph = {}
        newGraph['userId'] = foundGraph.userID
        newGraph['nffGraphID'] = foundGraph.nffGraphID
        newGraph['volatility'] = foundGraph.volatility
        graphList.append(newGraph)
    if len(graphList) != 0:
        return {'list': graphList}
    return None


def getGraph(user_id, graph_id):
    foundGraph = NF_FGraphs.objects.filter(userID=user_id).filter(nffGraphID=graph_id)
    if len(foundGraph) == 0:
        return None
    return foundGraph


def addGraph(user_id, graph_id, volatility):
    graph = NF_FGraphs(userID=user_id, nffGraphID=graph_id, volatility=volatility)
    graph.save()


def deleteGraph(user_id, graph_id):
    graph = NF_FGraphs.objects.filter(userID=user_id).filter(nffGraphID=graph_id)
    if len(graph) != 0:
        graph[0].delete()
        return True
    return False
'''

'''''''''''''''''''''''''''''''''''''''
                VNF API
'''''''''''''''''''''''''''''''''''''''
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


'''
def addBootConfig(configuration_id, configuration):
    if configuration is None:
        raise ParseError(detail="No configuration was provided")
    vnf = VNF(configuration_id=configuration_id)
    if len(vnf) != 0:
        vnf.update(bootstrap_configuration=base64.b64encode(configuration))
        return True
    return False
'''


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


# VNF current status API
'''
def getStatus(user_id, graph_id, vnf_id):
    foundVNF = VNF.objects.filter(userID=user_id).filter(nffGraphID=graph_id).filter(vnfID=vnf_id)
    if len(foundVNF) == 0:
        return None
    config = base64.b64decode(foundVNF[0].last_status_exported).decode('utf-8')
    return config


def addStatus(user_id, graph_id, vnf_id, status):
    if status is None:
        raise ParseError(detail="No status was provided")
    vnf = VNF(userID=user_id, nffGraphID=graph_id, vnfID=vnf_id)
    if len(vnf) != 0:
        vnf.update(last_status_exported=base64.b64encode(status))
        return True
    return False


def deleteStatus(user_id, graph_id, vnf_id):
    vnf = VNF.objects.filter(user_id=user_id).filter(nffGraphID=graph_id).filter(vnfID=vnf_id)
    if len(vnf) != 0:
        vnf.update(last_status_exported=None)
        return True
    return False


def updateStatus(user_id, graph_id, vnf_id, status):
    if status is None:
        raise ParseError(detail="No status was provided")
    vnf = VNF.objects.filter(userID=user_id).filter(nffGraphID=graph_id).filter(vnfID=vnf_id)
    if len(vnf) == 0:
        return False
    vnf.update(last_status_exported=base64.b64encode(status))
    return True
'''
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

'''
def addRESTEndpoint(configuration_id, rest_endpoint):
    if rest_endpoint is None:
        raise ParseError(detail="No status was provided")
    vnf = VNF(configuration_id=configuration_id)
    if len(vnf) != 0:
        print("zero")
        vnf.update(rest_endpoint=rest_endpoint)
        return True
    return False
'''

def deleteRESTEndpoint(configuration_id):
    vnf = VNF.objects.filter(configuration_id=configuration_id)
    if len(vnf) != 0:
        if vnf[0].restEndpoint != "":
            vnf.update(restEndpoint="")
            return True
    return False
