from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import API
from subprocess import call
from django.core.exceptions import ObjectDoesNotExist
from ConfigParser import SafeConfigParser
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.db.models import Q
import os, logging
import xml.etree.ElementTree as ET
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.parsers import FileUploadParser, MultiPartParser
from subprocess import call
from xml.dom import minidom
import json
from datastore.imageRepository.LocalRepository import LocalRepository
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from .models import MyChunkedUpload, VNF
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

parser = SafeConfigParser()
parser.read(os.environ["DATASTORE_CONFIG_FILE"])
logging.basicConfig(filename=parser.get('logging', 'filename'), format='%(asctime)s %(levelname)s:%(message)s',
                    level=parser.get('logging', 'level'))
repository = parser.get('repository', 'repository')
if repository == "LOCAL_FILES":
    imagesDir = parser.get('General', 'IMAGE_DIR')
    imageRepo = LocalRepository(imagesDir)


class VNFTemplateAll(APIView):
    """
    """

    def get(self, request):
        """
        Get the all VNF with the respectively template
        """
        template = API.getVNFTemplate()
        if template is None:
            return HttpResponse(status=404)
        return Response(data=template)


class VNFTemplateAllV2(VNFTemplateAll):
    """
    """

    def put(self, request):
        """
        Create a new VNF template. The 'vnf_id' assigned by the datastore is contained in the response.
        """
        if request.META['CONTENT_TYPE'] != 'application/json':
            return HttpResponse(status=415)
        if 'image-upload-status' not in request.data.keys() or 'template' not in request.data.keys():
            return HttpResponse("Wrong request format", status=400)
        if all(request.data['image-upload-status'] not in state for state in VNF.IMAGE_UPLOAD_STATUS):
            return HttpResponse("Wrong value of image-upload-status field", status=400)
        image_upload_status = request.data['image-upload-status']
        try:
            if 'functional-capability' not in request.data['template'].keys():
                return HttpResponse("Missing functional-capability field", status=400)
            capability = request.data['template']['functional-capability']
            template = json.dumps(request.data['template'])
        except:
            return HttpResponse(status=400)

        vnf_id = API.addVNFTemplateV2(template, capability, image_upload_status)
        return HttpResponse(vnf_id, status=200)


class VNFTemplate(APIView):
    """
    """

    def get(self, request, vnf_id):
        """
        Get the VNF template of a VNF
        """
        template = API.getVNFTemplate(vnf_id)
        if template is None:
            return HttpResponse(status=404)
        return Response(data=template)

    def put(self, request, vnf_id):
        """
        Update or create a new VNF template
        """
        if request.META['CONTENT_TYPE'] != 'application/json':
            return HttpResponse(status=415)
        try:
            if 'functional-capability' not in request.data.keys():
                return HttpResponse("Missing functional-capability field", status=400)
            capability = request.data['functional-capability']
            template = json.dumps(request.data)
        except:
            return HttpResponse(status=400)
        API.addVNFTemplate(vnf_id, template, capability)
        return HttpResponse(status=200)

    def delete(self, request, vnf_id):
        """
        Delete an existing VNF template
        """
        if API.deleteVNFTemplate(vnf_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)


class VNFTemplateV2(VNFTemplate):
    """
    """

    def put(self, request, vnf_id):
        """
        Update an existing VNF template
        """
        if request.META['CONTENT_TYPE'] != 'application/json':
            return HttpResponse(status=415)
        try:
            if 'functional-capability' not in request.data.keys():
                return HttpResponse("Missing functional-capability field", status=400)
            capability = request.data['functional-capability']
            template = json.dumps(request.data)
        except:
            return HttpResponse(status=400)
        API.updateVNFTemplate(vnf_id, template, capability)
        return HttpResponse(status=200)


class VNFImage(APIView):
    """
    """

    def get(self, request, vnf_id):
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

    def delete(self, request, vnf_id):
        """
        Remove a disk image for a VNF
        """
        try:
            state = VNF.objects.get(vnf_id=str(vnf_id)).image_upload_status
            if state == VNF.COMPLETED:
                os.remove(os.path.join(imagesDir, vnf_id))
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=400)


class VNFImageV2(APIView):
    """
    """

    def __init__(self):
        self.VNFImage = VNFImage()

    def get(self, request, vnf_id):
        """
        Get the disk image of a VNF
        """
        return self.VNFImage.get(request, vnf_id)

    def delete(self, request, vnf_id):
        """
        Remove a disk image for a VNF
        """
        return self.VNFImage.delete(request, vnf_id)


class NFFGraphs(APIView):
    """
    """

    def put(self, request, nf_fgraphs_id):
        """
        Update or create a new Network Functions Forwarding Graph
        """
        if request.META['CONTENT_TYPE'] != 'application/json':
            return HttpResponse(status=415)
        try:
            template = json.dumps(request.data)
        except:
            return HttpResponse(status=400)
        if API.addNF_FGraphs(nf_fgraphs_id, template) == False:
            return HttpResponse("The given ID is different from the template", status=400)
        return Response(data=json.loads(template))

    def delete(self, request, nf_fgraphs_id):
        """
        Delete an existig Network Functions Forwarding Graph
        """
        if API.deleteNF_FGraphs(nf_fgraphs_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)

    def get(self, request, nf_fgraphs_id):
        """
        Get the Network Functions Forwarding Graph
        """
        template = API.getNF_FGraphs(nf_fgraphs_id)
        if template is None:
            return HttpResponse(status=404)
        return Response(data=template)


class NF_FGraphsAll(APIView):
    """
    """

    def get(self, request):
        """
        Get the all Network Functions Forwarding Graph
        """
        template = API.getNF_FGraphs()
        if template is None:
            return HttpResponse(status=404)
        return Response(data=template)


class NF_FGraphsAll_graphs_names(APIView):
    """
    """

    def get(self, request):
        """
        Get the all NFFGs Names and ids
        """
        template = API.getNF_FGraphsAll_graphs_names()
        if template is None:
            return HttpResponse(status=404)
        return Response(data=template)


class Capability(APIView):
    def get(self, request, capability):
        """
        Get the all VNF with the respectively capability
        """
        template = API.getTemplatesFromCapability(capability)
        if template is None:
            return HttpResponse(status=404)
        return Response(data=template)


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
        VNF.objects.filter(vnf_id=str(request.POST['vnf_id'])).update(image_upload_status=VNF.COMPLETED)

    def get_response_data(self, chunked_upload, request):
        filename = chunked_upload.filename
        offset = chunked_upload.offset
        vnf_id = chunked_upload.vnf_id
        # Delete the temp upload both from DB and from disk
        chunked_upload.delete()
        return {'message': ("You successfully uploaded '%s' (%s bytes) for VNF with ID: %s" % (filename, offset, vnf_id)),
                'vnf_id': vnf_id}
