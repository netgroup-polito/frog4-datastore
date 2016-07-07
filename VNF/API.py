from models import VNF,NFFG
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





def addNFFG(nffg_id, template):
	nffg = NFFG(nffg_id = str(nffg_id), template = base64.b64encode(template))
	nffg.save()




def getNFFG(nffg_id=None):
	if nffg_id is not None:
		nffg_id = NFFG.objects.filter(nffg_id=str(nffg_id))
	else:
		nffg = NFFG.objects.all()
		nffgList = []
		for foundNFFG in nffg:
			newNFFG = {}
			newNFFG['id'] = foundNFFG.nffg_id
			newNFFG['template'] = json.loads(base64.b64decode(foundNFFG.template))
			nffgList.append(newNFFG)
		return {'list':nffgList}
	return None
