from models import VNF
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
		return base64.b64decode(vnf[0].template)
	return None


def deleteVNFTemplate(vnf_id):
	vnf = VNF.objects.filter(vnf_id=str(vnf_id))
	if len(vnf) != 0:
		vnf[0].delete()
		return True
	return False

def addVNFTemplate(vnf_id, template):
	vnf = VNF(vnf_id = str(vnf_id), template = base64.b64encode(template))
	vnf.save()
