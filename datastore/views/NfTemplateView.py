import json
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import datastore.services.NfTemplateService as API
from vnf_template_library.validator import ValidateTemplate
from datastore.models import VNF_Image


class VNFTemplateAll(APIView):
    """
    """

    def get(self, request):
        """
         Get the all VNF with the respectively template
              ---
              # YAML (must be separated by `---`)

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
        """
        template = API.getVNFTemplate()
        if template is None:
            return HttpResponse(status=404)
        return Response(data=template)

    def post(self, request):
        """
        Create a new VNF template. The 'vnf_id' assigned by the datastore is contained in the response.
        ---
         # YAML (must be separated by `---`)
            parameters:
                - name: template
                  required: true
                  paramType: body
                  type: json

            responseMessages:
                - code: 200
                  message: Ok
                - code: 400
                  message: Bad request
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
                image_upload_status = VNF_Image.REMOTE
            except Exception as e:
                return HttpResponse(e.message, status=400)
        elif all(request.data['image-upload-status'] not in state for state in VNF_Image.IMAGE_UPLOAD_STATUS):
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
            except Exception as e:
                return HttpResponse(e.message, status=400)

        res = API.addVNFTemplateV2(template, capability, image_upload_status)
        return HttpResponse(res, status=200)


class VNFTemplate(APIView):
    """
    """

    def get(self, request, template_id):
        """
        Get the VNF template of a VNF
        ---
         # YAML (must be separated by `---`)
            parameters:
                - name: template_id
                  required: true
                  paramType: path
                  type: string

            responseMessages:
                - code: 200
                  message: Ok
                - code: 404
                  message: Not found
        """
        template = API.getVNFTemplate(template_id)
        if template is None:
            return HttpResponse(status=404)
        return Response(data=template)


    def delete(self, request, template_id):
        """
        Delete an existing VNF template
        ---
         # YAML (must be separated by `---`)
            parameters:
                - name: template_id
                  required: true
                  paramType: path
                  type: string

            responseMessages:
                - code: 200
                  message: Ok
                - code: 404
                  message: Not found
        """
        if API.deleteVNFTemplate(template_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)

    def put(self, request, template_id):
        """
        Update an existing VNF template
        ---
         # YAML (must be separated by `---`)
            parameters:
                - name: template_id
                  required: true
                  paramType: path
                  type: string
                - name: template
                  required: true
                  paramType: body
                  type: json

            responseMessages:
                - code: 200
                  message: Ok
                - code: 400
                  message: Bad request
                - code: 404
                  message: Not found
                - code: 415
                  message: Invalid content type
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
        res = API.updateVNFTemplate(template_id, template, capability)
        if not res:
            return HttpResponse(status=404)
        return HttpResponse(status=200)
