from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import API
from ConfigParser import SafeConfigParser
from django.http import HttpResponse
import os, logging
import json
from datastore.imageRepository.LocalRepository import LocalRepository
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from .models import MyChunkedUpload, VNF
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from datastore.YANGParser import YANGParser
from vnf_template_library.validator import ValidateTemplate
from nffg_library.validator import ValidateNF_FG

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

    def put(self, request):
        """
        Create a new VNF template. The 'vnf_id' assigned by the datastore is contained in the response.
        """
        if request.META['CONTENT_TYPE'] != 'application/json':
            return HttpResponse(status=415)

        if 'image-upload-status' not in request.data.keys():
            try:
                if 'functional-capability' not in request.data.keys():
                    return HttpResponse("Missing functional-capability field", status=400)
                capability = request.data['functional-capability']
                ValidateTemplate().validate(request.data)
                template = json.dumps(request.data)
                image_upload_status = VNF.REMOTE
            except:
                return HttpResponse(status=400)
        elif all(request.data['image-upload-status'] not in state for state in VNF.IMAGE_UPLOAD_STATUS):
            return HttpResponse("Wrong value of image-upload-status field", status=400)
        elif 'template' not in request.data.keys():
            return HttpResponse("Missing template field", status=400)
        else:
            try:
                if 'functional-capability' not in request.data['template'].keys():
                    return HttpResponse("Missing functional-capability field", status=400)
                capability = request.data['template']['functional-capability']
                ValidateTemplate().validate(request.data['template'])
                template = json.dumps(request.data['template'])
                image_upload_status = request.data['image-upload-status']
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


    def delete(self, request, vnf_id):
        """
        Delete an existing VNF template
        """
        if API.deleteVNFTemplate(vnf_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)

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
            ValidateTemplate().validate(request.data)
            template = json.dumps(request.data)
        except:
            return HttpResponse(status=400)
        res = API.updateVNFTemplate(vnf_id, template, capability)
        if not res:
            return HttpResponse(status=404)
        return HttpResponse(status=200)



class VNFImage(APIView):
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
            state = VNF.objects.get(vnf_id=str(vnf_id)).image_upload_status
            if state == VNF.COMPLETED:
                imageRepo.deleteImage(vnf_id)
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=400)


class NFFGraphs(APIView):
    """
    """

    def put(self, request, nf_fgraph_id = None):
        """
        Update a Network Functions Forwarding Graph
        """
        if request.META['CONTENT_TYPE'] != 'application/json':
            return HttpResponse(status=415)
        try:
            ValidateNF_FG().validate(request.data)
            nffg = json.dumps(request.data)
            if nf_fgraph_id is None:
                graph_id = API.addNF_FGraphs(nffg)

            else:
                graph_id = API.updateNF_FGraphs(nf_fgraph_id, nffg)
        except:
            return HttpResponse(status=400)
        response_uuid = dict()
        response_uuid["nffg-uuid"] = graph_id
        return HttpResponse(json.dumps(response_uuid), status=200)

    def delete(self, request, nf_fgraph_id):
        """
        Delete an existig Network Functions Forwarding Graph
        """
        try:
            if API.deleteNF_FGraphs(nf_fgraph_id):
                return HttpResponse(status=200)
            return HttpResponse(status=404)
        except:
            return HttpResponse(status=400)

    def get(self, request, nf_fgraph_id):
        """
        Get the Network Functions Forwarding Graph
        """
        try:
            nffg = API.getNF_FGraphs(nf_fgraph_id)
            if nffg is None:
                return HttpResponse(status=404)
            return Response(data=nffg)
        except:
            return HttpResponse(status=400)

class NFFGResource(APIView):
    """
    """

    def put(self, request):
        """
        Create a New Network Functions Forwarding Graph
        Deploy a graph
        """
        return NFFGraphs().put(request)

    def get(self, request):
        """
        Get the all Network Functions Forwarding Graph
        """
        try:
            nffgs = API.getNF_FGraphs()
            if nffgs is None:
                return HttpResponse(status=404)
            return Response(data=nffgs)
        except:
            return HttpResponse(status=400)

class nffg_digest(APIView):
    """
    """

    def get(self, request):
        """
        Get the all NFFGs digest
        """
        try:
            digest = API.getnffg_digest()
            if digest is None:
                return HttpResponse(status=404)
            return Response(data = digest)
        except:
            return HttpResponse(status=400)


class Capability(APIView):
    def get(self, request, capability):
        """
        Get the all VNF with the respectively capability
        """
        try:
            template = API.getTemplatesFromCapability(capability)
            if template is None:
                return HttpResponse(status=404)
            return Response(data=template)
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
        VNF.objects.filter(vnf_id=str(request.POST['vnf_id'])).update(image_upload_status=VNF.COMPLETED)

    def get_response_data(self, chunked_upload, request):
        filename = chunked_upload.filename
        offset = chunked_upload.offset
        vnf_id = chunked_upload.vnf_id
        # Delete the temp upload both from DB and from disk
        chunked_upload.delete()
        return {'message': ("You successfully uploaded '%s' (%s bytes) for VNF with ID: %s" % (filename, offset, vnf_id)),
                'vnf_id': vnf_id}


class YANGModelsAll(APIView):
    parser_classes = (YANGParser,)

    def get(self, request):
        '''
        Retrieve all tye YANG model stored into the repository
        '''
        yang = API.getAllYANG_model()
        if yang is None:
            return HttpResponse(status=404)
        return Response(data=yang)


class YANGModels(APIView):
    parser_classes = (YANGParser,)

    def get(self, request, yang_id):
        '''
        Retrieve a YANG model given the yang id
        '''
        yang = API.getYANG_model(yang_id)
        if yang is None:
            return HttpResponse(status=404)
        return Response(data=yang)

    def delete(self, request, yang_id):
        '''
        Delete a YANG model given the yang id
        '''
        if API.deleteYANG_model(yang_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)

    def post(self, request, yang_id):
        '''
        Insert a new YANG model into the repository.
        Before saving the yang model into the DB, it is checked that the it is sintactically correct
        '''
        yang_model = request.data
        res = API.addYANG_model(yang_id, yang_model)
        return HttpResponse(status=200)

    def put(self, request, yang_id):
        '''
        Update a YANG model
        '''
        yang_model = request.data
        if API.updateYANG_model(yang_id, yang_model):
            return HttpResponse(status=200)
        return HttpResponse(status=404)


class YIN(APIView):
    def get(self, request, yang_id):
        '''
        Retrieve the YIN associated to a YANG model.
        The YIN is generated run time for each request by pyang
        '''
        yin = API.getYINFromYangID(yang_id)
        if yin is None:
            return HttpResponse(status=404)
        return Response(data=yin)
