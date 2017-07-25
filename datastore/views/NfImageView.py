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
from datastore.models.MyChunkedUpload import My_ChunkedUpload
from datastore.models.NfImage import VNF_Image
import datastore.services.NfImageService as API
import json
from datastore.parsers.TextParser import PlainTextParser


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
        ---
              # YAML (must be separated by `---`)

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
        """
        res = API.getImage(vnf_id)
        if res is None:
            return Response(status=404)
        wrapper = res[0]
        file_len = res[1]
        response = HttpResponse(wrapper, content_type='text/plain', status=status.HTTP_200_OK)
        response['Content-Length'] = file_len
        return response

    def delete(self, request, vnf_id):
        """
        Remove a disk image for a VNF
        ---
              # YAML (must be separated by `---`)

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
        """
        if API.deleteImage(vnf_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)

    def put(self, request, vnf_id):
        """
        Insert/update a disk image for a VNF.
        ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: vnf_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
        """
        if not 'file' in request.data:
            return HttpResponse("No image was provided", status=422)
        if API.updateImage(vnf_id, request.data['file']):
            return HttpResponse(status=200)
        return HttpResponse(status=400)


class Template(APIView):
    parser_classes = (PlainTextParser,)

    def get(self, request, vnf_id):
        """
            Get the template of a specific VNF image
            ---
            # YAML (must be separated by `---`)
            parameters:
              - name: vnf_id
                required: true
                paramType: path
                type: string

            responseMessages:
              - code: 200
                message: Ok
              - code: 404
                message: Not found
        """
        template_id, msg = API.getTemplate(vnf_id)
        if template_id is None:
            if msg == "":
                return HttpResponse(status=404)
            return HttpResponse(msg, status=404)
        return Response(data=template_id)

    def put(self, request, vnf_id):
        """
            Update the template of a specific VNF image
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: vnf_id
                    required: true
                    paramType: path
                    type: string
                  - name: template_id
                    required: true
                    paramType: body
                    type: string

              consumes:
                  - text/plain

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
                    code: 422
                    message: No configuration inserted into the body of the request
         """
        if request.data == {}:
            return HttpResponse("No template was provided", status=422)

        res, msg = API.updateTemplate(vnf_id, request.data)
        if res:
            return HttpResponse(status=200)
        return HttpResponse(msg, status=404)

    def delete(self, request, vnf_id):
        """
            Delete the template of a specific VNF image
            ---
            # YAML (must be separated by `---`)
            parameters:
              - name: vnf_id
                required: true
                paramType: path
                type: string

            responseMessages:
              - code: 200
                message: Ok
              - code: 404
                message: Not found
        """
        if API.deleteTemplate(vnf_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)


class MyChunkedUploadView(ChunkedUploadView, APIView):
    """
    """
    field_name = 'the_file'
    model = My_ChunkedUpload

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
        print("post: " + request.POST['vnf_id'])
        if request.POST['vnf_id'] == "":
            image_id = API.addImage()
            request.POST['vnf_id'] = image_id
        else:
            image_id = request.POST['vnf_id']
        res = super(MyChunkedUploadView, self).post(request, *args, **kwargs)
        data = json.loads(res.content)
        data['vnf_id'] = image_id
        res.content = json.dumps(data)
        return res

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(MyChunkedUploadView, self).dispatch(*args, **kwargs)

    def check_permissions(self, request):
        # Allow non authenticated users to make uploads
        pass


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView, APIView):
    """
    """
    model = My_ChunkedUpload

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
        API.completeImageUpload(str(request.POST['vnf_id']))

    def get_response_data(self, chunked_upload, request):
        filename = chunked_upload.filename
        offset = chunked_upload.offset
        vnf_id = chunked_upload.vnf_id
        # Delete the temp upload both from DB and from disk
        chunked_upload.delete()
        return {'message': ("You successfully uploaded '%s' (%s bytes) for VNF with ID: %s" % (filename, offset, vnf_id)),
                'vnf_id': vnf_id}
