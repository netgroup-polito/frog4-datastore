import os
import glob
from wsgiref.util import FileWrapper


class LocalRepository(object):
    def __init__(self, imagesDir):
        self.imagesDir = imagesDir

    def storeImage(self, vnf_id, imageFile):
        # Getting original file extension
        ext = os.extsep + imageFile.name.split(os.extsep, 1)[1] if len(imageFile.name.split(os.extsep, 1)) == 2 else ""
        # Create the images folder if it doesn't exists
        if not os.path.exists(self.imagesDir):
            os.makedirs(self.imagesDir)
        # Remove the old image if it exists. This is necessary because in case of an update, if the new image has a
        # different extension, the old file will not be overwritten.
        try:
            self.deleteImage(vnf_id)
        except OSError:
            pass
        # Store the new uploaded image file
        with open(os.path.join(self.imagesDir, str(vnf_id) + ext), 'wb') as f:
            for chunk in imageFile.chunks():
                f.write(chunk)

    def getImage(self, vnf_id):
        filename = glob.glob(os.path.join(self.imagesDir, str(vnf_id) + '.*'))[0]
        wrapper = FileWrapper(file(filename))
        fileLen = os.path.getsize(filename)
        return (wrapper, fileLen)

    def deleteImage(self, vnf_id):
        filename = glob.glob(os.path.join(self.imagesDir, str(vnf_id) + '.*'))[0] if len(
            glob.glob(os.path.join(self.imagesDir, str(vnf_id) + '.*'))) != 0 else os.path.join(self.imagesDir,
                                                                                                str(vnf_id))
        os.remove(filename)
