from models import VNF
import base64



def getVNFTemplate(vnf_id):
	vnf = VNF.objects.get(vnf_id=str(vnf_id))
	if vnf is not None:
		return base64.decode(vnf.template)
	return None
