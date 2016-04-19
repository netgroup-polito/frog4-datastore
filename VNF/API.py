from models import VNF
import base64



def getVNFTemplate(vnf_id):
	vnf = VNF.objects.filter(vnf_id=str(vnf_id))
	
	if len(vnf) != 0:
		return base64.decode(vnf[0].template)
	return None


def deleteVNFTemplate(vnf_id):
	vnf = VNF.objects.filter(vnf_id=str(vnf_id))
	if len(vnf) != 0:
		vnf[0].delete()
	return None
