from datastore.models import VNF, NF_FGraphs, YANG_Models
import base64
import json
import random
import string
from datastore.YANGtoYIN import create_yin
from rest_framework.parsers import ParseError

def getVNFTemplate(vnf_id=None):
    if vnf_id is not None:
        vnf = VNF.objects.filter(vnf_id=str(vnf_id))
    else:
        vnf = VNF.objects.all()
        # Filter out templates with uncompleted images
        vnf = vnf.exclude(image_upload_status=VNF.IN_PROGRESS)
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
    vnf = VNF.objects.filter(capability=str(vnfCapability))
    # Filter out templates with uncompleted images
    vnf = vnf.exclude(image_upload_status=VNF.IN_PROGRESS)
    vnfList = []
    for foundVNF in vnf:
        newVNF = {}
        newVNF['id'] = foundVNF.vnf_id
        newVNF['template'] = json.loads(base64.b64decode(foundVNF.template))
        newVNF['image-upload-status'] = foundVNF.image_upload_status
        vnfList.append(newVNF)
    return {'list': vnfList}


def deleteVNFTemplate(vnf_id):
    vnf = VNF.objects.filter(vnf_id=str(vnf_id))
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
        vnf = VNF.objects.filter(vnf_id=vnf_id)
        if len(vnf) == 0:
            break
    # Store the template
    vnf = VNF(vnf_id = vnf_id, template = base64.b64encode(template), capability=capability, image_upload_status=image_upload_status)
    vnf.save()
    # Return the generated NF ID
    return vnf_id


def updateVNFTemplate(vnf_id, template, capability):
    old_template = VNF.objects.filter(vnf_id=vnf_id)
    if len(old_template) == 0:
        return False
    VNF.objects.filter(vnf_id=str(vnf_id)).update(template=base64.b64encode(template), capability=capability)
    return True


def addNF_FGraphs(nf_fgraphs_id, nf_fgraphs_template):
    if nf_fgraphs_id != json.loads(nf_fgraphs_template)['forwarding-graph']['id']:
        return False
    nf_fgraphs= NF_FGraphs(nf_fgraphs_id = str(nf_fgraphs_id), nf_fgraphs_template = base64.b64encode(nf_fgraphs_template))
    nf_fgraphs.save()
    return True


def getNF_FGraphs(nf_fgraphs_id=None):
    if nf_fgraphs_id is not None:
        nf_fgraphs = NF_FGraphs.objects.filter(nf_fgraphs_id=str(nf_fgraphs_id))
    else:
        nf_fgraphs = NF_FGraphs.objects.all()
        nf_fgraphsList = []
        for foundnf_fgraphs in nf_fgraphs:
            newnf_fgraphs = {}
            newnf_fgraphs['nf_fgraph_id'] = foundnf_fgraphs.nf_fgraphs_id
            newnf_fgraphs['forwarding-graph'] = json.loads(base64.b64decode(foundnf_fgraphs.nf_fgraphs_template))['forwarding-graph']
            nf_fgraphsList.append(newnf_fgraphs)
        return {'list': nf_fgraphsList}

    if len(nf_fgraphs) != 0:
        return json.loads(base64.b64decode(nf_fgraphs[0].nf_fgraphs_template))
    return None


def deleteNF_FGraphs(nf_fgraphs_id):
    nf_fgraphs = NF_FGraphs.objects.filter(nf_fgraphs_id=str(nf_fgraphs_id))
    if len(nf_fgraphs) != 0:
        nf_fgraphs[0].delete()
        return True
    return False


def getNF_FGraphsAll_graphs_names():
    nf_fgraphs = NF_FGraphs.objects.all()
    nf_fgraphsList = []
    for foundnf_fgraphs in nf_fgraphs:
        nf_fgraphs_name = {}
        newnf_fgraphs = json.loads(base64.b64decode(foundnf_fgraphs.nf_fgraphs_template))['forwarding-graph']
        if 'name' in newnf_fgraphs.keys():
            nf_fgraphs_name['name'] = newnf_fgraphs['name']
        if 'id' in newnf_fgraphs.keys():
            nf_fgraphs_name['id'] = newnf_fgraphs['id']
        nf_fgraphsList.append(nf_fgraphs_name)
    if len(nf_fgraphs) != 0:
        return {'list': nf_fgraphsList}
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


def addYANG_model(yang_id, yang_model):
    if yang_model == {}:
        raise ParseError(detail="no yang was provided") #the empty case is managed in such a way because django don't pass an empty body to the parser
    yang = YANG_Models(yang_id=yang_id, yang_model=base64.b64encode(yang_model))
    yang.save()


def deleteYANG_model(yang_id):
    yang = YANG_Models.objects.filter(yang_id=yang_id)
    if len(yang) != 0:
        yang[0].delete()
        return True
    return False


def updateYANG_model(yang_id, yang_model):
    yang = YANG_Models.objects.filter(yang_id=yang_id)
    if len(yang) == 0:
        return False
    YANG_Models.objects.filter(yang_id=yang_id).update(yang_model=base64.b64encode(yang_model))
    return True

