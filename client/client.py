
from requests import get, put, delete, patch
import urllib
'''
Client for the VNF Repository API. All methods return a Response object.

'''
class Client:
	def __init__(self,base_URL):
		self.base_URL=base_URL+'/v1/'
		self.headers={"Accept":'application/json','Content-type':'application/json'}
	
	
	def get_manifest(self, vnf_id):
		url = self.base_URL+'VNF/manifest/'+image_id
		return get(url)
	
	def get_image_file(self,image_id, path):
		url =self.base_URL+'VNF/image/'+image_id+'/'
		r=get(url)
		if r.status_code == 200:
			with open(path, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024):
					f.write(chunk)
		return r

	def delete_manifest (self,image_id):
		url = self.base_URL+'VNF/'+image_id+'/'
		return delete(url)
		
	def delete_image(self, image_id):
		url = self.base_URL+'VNF/images/'+image_id+'/'
		return delete(url)
	
	def put_image(self, image_id, path):
		url=self.base_URL+'VNF/image/'+image_id+'/'
		with open (path, 'rb') as f:
			files={'image':f}
			return put(url,files=files)
	
	def put_manifest(self,image_id,manifestJSON):
		url=self.base_URL+'VNF/'+image_id+'/'
		return put(url,data=manifestJSON, header=self.headers)
