from requests import get, put, delete, patch
import urllib
'''
Client for the VNF Repository API. All methods return a Response object.
'''
class Client:
	def __init__(self,base_URL):
		self.base_URL=base_URL+'/v2/'
		self.headers={"Accept":'application/json','Content-type':'application/json'}

	def get_template(self, vnf_id):
		url = self.base_URL+'nf_template/'+image_id
		return get(url)

	def delete_template(self,image_id):
		url = self.base_URL+'nf_template/'+image_id+'/'
		return delete(url)

	def delete_image(self, image_id):
		url = self.base_URL+'nf_image/'+image_id+'/'
		return delete(url)

	def put_template(self,image_id,manifestJSON):
		url=self.base_URL+'nf_template/'+image_id+'/'
		return put(url,data=manifestJSON, headers=self.headers)
