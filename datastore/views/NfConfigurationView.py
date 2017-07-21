import json
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import datastore.services.NfConfigurationService as API
from rest_framework.parsers import JSONParser


class ConfigurationByuser(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, user_id):
        """
            Get all the configurations of the given user
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: user_id
                    required: true
                    paramType: path
                    type: string
              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
         """
        configurations = API.getConfigurationsByUser(user_id)
        if configurations is None:
            return HttpResponse(status=404)
        return Response(data=configurations)


class Configuration(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, user_id, configuration_id):
        """
            Get a specific configuration of the given user
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: user_id
                    required: true
                    paramType: path
                    type: string
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
        configuration = API.getConfiguration(user_id, configuration_id)
        if configuration is None:
            return HttpResponse(status=404)
        return Response(data=configuration)

    def post(self, request, user_id, configuration_id):
        """
            Create a new configuration for the given user
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: user_id
                    required: true
                    paramType: path
                    type: string
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
                  - code: 422
                    message: Missing 'configuration' and/or 'yang id' parameters inside the body
                  - code: 409
                    message: The configuration already exists
                  - code: 400
                    message: Bad request
        """
        try:
            if 'yang_id' not in request.data:
                return HttpResponse("No yang id was provided", status=422)
            if 'configuration' not in request.data:
                return HttpResponse("No configuration was provided", status=422)
            yang_id = request.data['yang_id']
            configuration = json.dumps(request.data['configuration'])
            res = API.addConfiguration(user_id=user_id, configuration_id=configuration_id, yang_id=yang_id, configuration=configuration)
            if not res:
                return HttpResponse("The configuration " + configuration_id + " already exists", status=409)
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(e.message, status=400)

    def delete(self, request, user_id, configuration_id):
        """
            Delete a configuration of the given user
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: user_id
                    required: true
                    paramType: path
                    type: string
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
        if API.deleteConfiguration(user_id, configuration_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)
