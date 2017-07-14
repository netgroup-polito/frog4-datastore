import json
import datastore.services.VnfInstanceService as API
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView


class VNFAll(APIView):
    def get(self, request):
        """
            ---
            # YAML (must be separated by `---`)
            responseMessages:
                - code: 200
                  message: Ok
                - code: 404
                  message: Not found
        """
        vnf = API.getAllVNFs()
        if vnf is None:
            return HttpResponse(status=404)
        return Response(data=vnf)


class VNF(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, configuration_id):
        """
            ---
            # YAML (must be separated by `---`)
            parameters:
                - name: configuration_id
                  required: true
                  paramType: path
                  type: string

            responseMessages:
                - code: 200
                  message: Ok
                - code: 404
                  message: Not found
        """
        vnf = API.getVNF(configuration_id)
        if vnf == None:
            return HttpResponse(status=404)
        return Response(data=vnf)

    def delete(self, request, configuration_id):
        """
                   ---
                   # YAML (must be separated by `---`)
                   parameters:
                       - name: configuration_id
                         required: true
                         paramType: path
                         type: string

                   responseMessages:
                       - code: 200
                         message: Ok
                       - code: 404
                         message: Not found
               """
        if API.deleteVNF(configuration_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)

    def post(self, request, configuration_id):
        """
               ---
               # YAML (must be separated by `---`)
               parameters:
                   - name: configuration_id
                     required: true
                     paramType: path
                     type: string

               responseMessages:
                   - code: 200
                     message: Ok
                   - code: 404
                     message: Not found
         """
        res = API.addVNF(configuration_id)
        if not res:
            return HttpResponse("The vnf with ID " + configuration_id + " already exists", status=409)
        return HttpResponse(status=200)


class RestEndpoint(APIView):
    def get(self, request, configuration_id):
        """
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: configuration_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
         """
        endpoint = API.getRESTEndpoint(configuration_id)
        if endpoint is None:
            return HttpResponse("The vnf with ID " + configuration_id + " does not exist", status=404)
        if endpoint == "":
            return HttpResponse(status=404)
        return Response(data=endpoint)

    def put(self, request, configuration_id):
        """
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: configuration_id
                    required: true
                    paramType: path
                    type: string
                  - name: endpoint
                    required: true
                    paramType: body
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
         """
        endpoint = request.data
        if endpoint == {}:
            return HttpResponse("No endpoint was provided", status=422)
        if API.putRESTEndpoint(configuration_id, endpoint):
            return HttpResponse(status=200)
        return HttpResponse("The vnf with ID " + configuration_id + " does not exist", status=404)

    def delete(self, request, configuration_id):
        """
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: configuration_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
         """
        if API.deleteRESTEndpoint(configuration_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)


class VNFBootingConfiguration(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, configuration_id):
        """
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: configuration_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
         """
        configuration = API.getBootConfig(configuration_id)
        if configuration is None:
            return HttpResponse("The vnf with ID " + configuration_id + " does not exist", status=404)
        if configuration == "":
            return HttpResponse(status=404)
        return Response(data=json.loads(configuration))

    def delete(self, request, configuration_id):
        """
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: configuration_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
         """
        if API.deleteBootConfig(configuration_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)

    def put(self, request, configuration_id):
        """
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: configuration_id
                    required: true
                    paramType: path
                    type: string
                  - name: configuration
                    required: true
                    paramType: body
                    type: json

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
         """
        if request.META['CONTENT_TYPE'] != 'application/json':
            return HttpResponse(status=415)
        data = request.stream.read()
        if data == {}:
            return HttpResponse("No configuration was provided", status=422)
        if API.updateBootConfig(configuration_id, data.decode()):
            return HttpResponse(status=200)
        return HttpResponse("The vnf with ID " + configuration_id + " does not exist", status=404)
