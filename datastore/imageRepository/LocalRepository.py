import os
from wsgiref.util import FileWrapper

class LocalRepository(object):
	
	def __init__(self, imagesDir):
		self.imagesDir = imagesDir

	def storeImage(self, vnf_id, imageFile):
		if not os.path.exists(self.imagesDir):
			os.makedirs(self.imagesDir)
		with open(self.imagesDir + str(vnf_id), 'wb')as f:
                	for chunk in imageFile.chunks():
                        	f.write(chunk)

	def getImage(self, vnf_id):
		filename = self.imagesDir + str(vnf_id)

		wrapper = FileWrapper(file(filename))
		fileLen = os.path.getsize(filename)
		return (wrapper, fileLen)
