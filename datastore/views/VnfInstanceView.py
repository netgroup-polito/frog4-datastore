import datastore.services.VnfInstanceService as API
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView


class VNFAll(APIView):
    def get(self, request):
        """
            Get all the VNF instances registered to the configuration orchestrator
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

    def get(self, request, instance_id):
        """
            Get the given VNF instance
            ---
            # YAML (must be separated by `---`)
            parameters:
                - name: instance_id
                  required: true
                  paramType: path
                  type: string

            responseMessages:
                - code: 200
                  message: Ok
                - code: 404
                  message: Not found
        """
        vnf = API.getVNF(instance_id)
        if vnf == None:
            return HttpResponse(status=404)
        return Response(data=vnf)

    def delete(self, request, instance_id):
        """
            Delete the given VNF instance
            ---
            # YAML (must be separated by `---`)
            parameters:
               - name: instance_id
                 required: true
                 paramType: path
                 type: string

            responseMessages:
               - code: 200
                 message: Ok
               - code: 404
                 message: Not found
        """
        if API.deleteVNF(instance_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)

    def post(self, request, instance_id):
        """
                Create a new VNF instance
               ---
               # YAML (must be separated by `---`)
               parameters:
                   - name: instance_id
                     required: true
                     paramType: path
                     type: string

               responseMessages:
                   - code: 200
                     message: Ok
                   - code: 404
                     message: Not found
         """
        res = API.addVNF(instance_id)
        if not res:
            return HttpResponse("The vnf with ID " + instance_id + " already exists", status=409)
        return HttpResponse(status=200)


class RestEndpoint(APIView):
    def get(self, request, instance_id):
        """
            Get the REST endpoint of a specific VNF instance
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: instance_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
         """
        endpoint = API.getRESTEndpoint(instance_id)
        if endpoint is None:
            return HttpResponse("The vnf with ID " + instance_id + " does not exist", status=404)
        if endpoint == "":
            return HttpResponse(status=404)
        return Response(data=endpoint)

    def put(self, request, instance_id):
        """
            Update the REST endpoint of a specific VNF instance
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: instance_id
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
        if API.putRESTEndpoint(instance_id, endpoint):
            return HttpResponse(status=200)
        return HttpResponse("The vnf with ID " + instance_id + " does not exist", status=404)

    def delete(self, request, instance_id):
        """
            Delete the REST endpoint of a specific VNF instance
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: instance_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
         """
        if API.deleteRESTEndpoint(instance_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)


class VNFBootingConfiguration(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, instance_id):
        """
            Get the boot configuration of a specific VNF instance
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: instance_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
         """
        configuration, msg = API.getBootConfig(instance_id)
        if configuration is None:
            if msg == "":
                return HttpResponse(status=404)
            return HttpResponse(msg, status=404)
        return Response(data=configuration)

    def delete(self, request, instance_id):
        """
            Delete the boot configuration of a specific VNF instance
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: instance_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
         """
        if API.deleteBootConfig(instance_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)

    def put(self, request, instance_id):
        """
            Update the boot configuration of a specific VNF instance
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: instance_id
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
                    code: 422
                    message: No configuration inserted into the body of the request
         """
        if request.META['CONTENT_TYPE'] != 'application/json':
            return HttpResponse(status=415)
        if 'configuration_id' not in request.data:
            return HttpResponse("No configuration id was provided", status=422)
        if 'user_id' not in request.data:
            return HttpResponse("No user id was provided", status=422)

        res, msg = API.updateBootConfig(instance_id, request.data['configuration_id'], request.data['user_id'])
        if res:
            return HttpResponse(status=200)
        return HttpResponse(msg, status=404)
