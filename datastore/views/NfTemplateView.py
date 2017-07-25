import json
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import datastore.services.NfTemplateService as API
import datastore.services.NfCapabilityService as CapabilityApi
from vnf_template_library.validator import ValidateTemplate
from rest_framework.parsers import JSONParser


class VNFTemplateAll(APIView):
    parser_classes = (JSONParser,)

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
        try:
            if request.META['CONTENT_TYPE'] != 'application/json':
                return HttpResponse(status=415)

            if 'functional-capability' not in request.data.keys():
                return HttpResponse("Missing functional-capability field", status=400)

            ValidateTemplate().validate(request.data)
            #template = json.dumps(request.data)
            res = API.addVNFTemplateV2(request.data)
        except Exception as e:
            return HttpResponse(e.message, status=400)
        return HttpResponse(res, status=200)


class VNFTemplate(APIView):
    parser_classes = (JSONParser,)

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
        template = API.getVNFTemplate(template_id)
        if template is None:
            return HttpResponse(status=404)
        capability = template['functional-capability']
        if API.deleteVNFTemplate(template_id):
            if CapabilityApi.getTemplatesFromCapability(capability) is None:
                CapabilityApi.deleteCapability(capability)
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
