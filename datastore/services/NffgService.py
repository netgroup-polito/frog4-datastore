import base64
import json
import uuid
from django.db import transaction
from datastore.models.Nffg import NF_FGraphs
from datastore.services import UserService


@transaction.atomic
def addNF_FGraphs(user_id, nffg):
    found_user = UserService.getUserObject(user_id)
    if found_user is None:
        return found_user
    while True:
        new_nffg_uuid = uuid.uuid4()
        graph = NF_FGraphs.objects.filter(nf_fgraph_id=str(new_nffg_uuid))
        #Check if the uuid is already used
        if len(graph) == 0:
            nf_fgraph_id = str(new_nffg_uuid)
            break
    graphs = NF_FGraphs(user=found_user, nf_fgraph_id=str(nf_fgraph_id), nffg =base64.b64encode(nffg))
    graphs.save()
    return nf_fgraph_id


@transaction.atomic
def updateNF_FGraphs(user_id, nf_fgraph_id, nffg):
    foundNffg = NF_FGraphs.objects.filter(user =user_id).filter(nf_fgraph_id=nf_fgraph_id)
    if len(foundNffg) == 0 or foundNffg[0].nffg == "":
        return False
    foundNffg.update(nffg = base64.b64encode(nffg))
    return True


def getNF_FGraphs(user_id=None, nf_fgraph_id=None):
    if nf_fgraph_id is not None and user_id is not None:
        nf_fgraphs = NF_FGraphs.objects.filter(user=str(user_id)).filter(nf_fgraph_id=str(nf_fgraph_id))
        if len(nf_fgraphs) == 0:
            return None
        return json.loads(base64.b64decode(nf_fgraphs[0].nffg))

    else:
        nf_fgraphs = NF_FGraphs.objects.all()
        if len(nf_fgraphs) == 0:
            return {'list': []}
        graphs = []
        for foundnf_fgraphs in nf_fgraphs:
            graph = {}
            graph['user id'] = foundnf_fgraphs.user.user_id
            graph['nffg-uuid'] = foundnf_fgraphs.nf_fgraph_id
            graph['forwarding-graph'] = json.loads(base64.b64decode(foundnf_fgraphs.nffg))['forwarding-graph']
            graphs.append(graph)
        return {'list': graphs}


@transaction.atomic
def deleteNF_FGraphs(user_id, nf_fgraph_id):
    graph = NF_FGraphs.objects.filter(user=str(user_id), nf_fgraph_id=str(nf_fgraph_id))
    if len(graph) != 0:
        graph[0].delete()
        return True
    return False


def getNffgDigest():
    nf_fgraphs = NF_FGraphs.objects.all()
    nf_fgraphsList = []
    for foundnf_fgraph in nf_fgraphs:
        nf_fgraphs_digest = {}
        newnf_fgraphs = json.loads(base64.b64decode(foundnf_fgraph.nffg))['forwarding-graph']
        print("name: " + newnf_fgraphs['name'])
        if 'name' in newnf_fgraphs.keys():
            nf_fgraphs_digest['name'] = newnf_fgraphs['name']
        nf_fgraphs_digest['nffg-uuid'] = foundnf_fgraph.nf_fgraph_id
        nf_fgraphs_digest['user'] = foundnf_fgraph.user.user_id
        nf_fgraphsList.append(nf_fgraphs_digest)
    if len(nf_fgraphs) != 0:
        return {'list': nf_fgraphsList}
    return {'list': []}


def getNFFGByUser(user_id):
    if UserService.getUserObject(user_id) is None:
        return None
    nffgs = NF_FGraphs.objects.filter(user=user_id)

    nffgsList = []
    for foundNffg in nffgs:
        newNffg = {}
        nffg = base64.b64decode(foundNffg.nffg).decode('utf-8')
        newNffg['user id'] = foundNffg.user.user_id
        newNffg['nffg-uuid'] = foundNffg.nf_fgraph_id
        newNffg['forwarding-graph'] = json.loads(nffg)
        nffgsList.append(newNffg)
    if len(nffgsList) != 0:
        return {'list': nffgsList}
    return {'list': []}