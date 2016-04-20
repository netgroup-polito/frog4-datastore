from models import VNF
import base64



def getVNFTemplate(vnf_id):
	vnf = VNF.objects.filter(vnf_id=str(vnf_id))
	
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
