import logging
import os
from ConfigParser import SafeConfigParser
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from datastore.imageRepository.LocalRepository import LocalRepository
from datastore.models import MyChunkedUpload, VNF_Image
import datastore.services.NfImageService as API

parser = SafeConfigParser()
parser.read(os.environ["DATASTORE_CONFIG_FILE"])
logging.basicConfig(filename=parser.get('logging', 'filename'), format='%(asctime)s %(levelname)s:%(message)s',
                    level=parser.get('logging', 'level'))
repository = parser.get('repository', 'repository')
if repository == "LOCAL_FILES":
    imagesDir = parser.get('General', 'IMAGE_DIR')
    imageRepo = LocalRepository(imagesDir)


class VNF_Image(APIView):
    """
    """

    def get(self, request, vnf_id):
        """
        Get the disk image of a VNF
        """
        return self.getImage(request, vnf_id)

    def delete(self, request, vnf_id):
        """
        Remove a disk image for a VNF
        """
        return self.deleteImage(request, vnf_id)

    def getImage(self, request, vnf_id):
        """
        Get the disk image of a VNF
        """
        try:
            (wrapper, fileLen) = imageRepo.getImage(vnf_id)
            response = HttpResponse(wrapper, content_type='text/plain', status=status.HTTP_200_OK)
            response['Content-Length'] = fileLen
            return response
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, vnf_id):
        """
        Insert/update a disk image for a VNF.
        """
        try:
            imageRepo.storeImage(vnf_id, request.data['file'])
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=400)

    def deleteImage(self, request, vnf_id):
        """
        Remove a disk image for a VNF
        """
        try:
            state = VNF_Image.objects.get(vnf_id=str(vnf_id)).image_upload_status
            if state == VNF_Image.COMPLETED:
                imageRepo.deleteImage(vnf_id)
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=400)


class MyChunkedUploadView(ChunkedUploadView, APIView):
    """
    """
    field_name = 'the_file'
    model = MyChunkedUpload

    def get_extra_attrs(self, request):
        attrs = {}
        for attr in request.POST.keys():
            attrs.update({attr: request.POST.get(attr)})
        return attrs

    def post(self, request, *args, **kwargs):
        """
        Insert/update a disk image for a VNF.

        Subsequent POST requests with chunks of the image file have to be sent.

        For further details see the note about NF Image upload API in the README_developer.
        """
        return super(MyChunkedUploadView, self).post(request, *args, **kwargs)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(MyChunkedUploadView, self).dispatch(*args, **kwargs)

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView, APIView):
    """
    """
    model = MyChunkedUpload

    def post(self, request, *args, **kwargs):
        """
        Insert/update a disk image for a VNF.

        Final POST request has to be sent when an image upload is completed.

        For further details see the note about NF Image upload API in the README_developer.
        """
        return super(MyChunkedUploadCompleteView, self).post(request, *args, **kwargs)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(MyChunkedUploadCompleteView, self).dispatch(*args, **kwargs)

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass

    def on_completion(self, uploaded_file, request):
        # Store the uploaded NF image file
        imageRepo.storeImage(request.POST['vnf_id'], uploaded_file)
        # Set the NF template to completed (in order to show in the available NFs list)
        VNF_Image.objects.filter(vnf_id=str(request.POST['vnf_id'])).update(image_upload_status=VNF.COMPLETED)

    def get_response_data(self, chunked_upload, request):
        filename = chunked_upload.filename
        offset = chunked_upload.offset
        vnf_id = chunked_upload.vnf_id
        # Delete the temp upload both from DB and from disk
        chunked_upload.delete()
        return {'message': ("You successfully uploaded '%s' (%s bytes) for VNF with ID: %s" % (filename, offset, vnf_id)),
                'vnf_id': vnf_id}
