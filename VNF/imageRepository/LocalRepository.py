import os
from wsgiref.util import FileWrapper

class LocalRepository(object):
	
	def __init__(self, imageDir):
		self.imageDir = imageDir

	def storeImage(self, vnf_id, imageFile):
		if not os.path.exists(self.imageDir):
			os.makedirs(self.imageDir)
		with open(self.imageDir + str(vnf_id), 'wb')as f:
                	for chunk in imageFile.chunks():
                        	f.write(chunk)

	def getImage(self, vnf_id):
		filename = self.imageDir + str(vnf_id)

		wrapper = FileWrapper(file(filename))
		fileLen = os.path.getsize(filename)
		return (wrapper, fileLen)
