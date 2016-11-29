from models import VNF,NF_FGraphs
import base64
import json

def getVNFTemplate(vnf_id=None):
	if vnf_id is not None:
		vnf = VNF.objects.filter(vnf_id=str(vnf_id))
	else:
		vnf = VNF.objects.all()
		vnfList = []
		for foundVNF in vnf:
			newVNF = {}
			newVNF['id'] = foundVNF.vnf_id
			newVNF['template'] = json.loads(base64.b64decode(foundVNF.template))
			vnfList.append(newVNF)
		return {'list':vnfList}
	
	if len(vnf) != 0:
		return json.loads(base64.b64decode(vnf[0].template))
	return None

def getTemplatesFromCapability(vnfCapability):
	vnf = VNF.objects.filter(capability=str(vnfCapability))
	vnfList = []
	for foundVNF in vnf:
		newVNF = {}
		newVNF['id'] = foundVNF.vnf_if
		newVNF['template'] = json.loads(base64.b64decode(foundVNF.template))
		vnfList.append(newVNF)
	return {'list': vnfList}

def deleteVNFTemplate(vnf_id):
	vnf = VNF.objects.filter(vnf_id=str(vnf_id))
	if len(vnf) != 0:
		vnf[0].delete()
		return True
	return False

def addVNFTemplate(vnf_id, template):
	vnf = VNF(vnf_id = str(vnf_id), template = base64.b64encode(template))
	vnf.save()

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
