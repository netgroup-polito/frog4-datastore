import os
import glob
from wsgiref.util import FileWrapper


class LocalRepository(object):
    def __init__(self, imagesDir):
        self.imagesDir = imagesDir

    def storeImage(self, vnf_id, imageFile):
        ext = os.path.splitext(imageFile.name)[1]
        if not os.path.exists(self.imagesDir):
            os.makedirs(self.imagesDir)
        with open(os.path.join(self.imagesDir, str(vnf_id) + ext), 'wb') as f:
            for chunk in imageFile.chunks():
                f.write(chunk)

    def getImage(self, vnf_id):
        filename = glob.glob(os.path.join(self.imagesDir, str(vnf_id) + '.*'))[0]
        wrapper = FileWrapper(file(filename))
        fileLen = os.path.getsize(filename)
        return (wrapper, fileLen)

    def deleteImage(self, vnf_id):
        filename = glob.glob(os.path.join(self.imagesDir, str(vnf_id) + '.*'))[0]
        os.remove(filename)
