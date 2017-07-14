import json
import datastore.services.UserService as API
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView


class UserAll(APIView):
    parser_classes = (JSONParser,)

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
        users = API.getAllUser()
        if users is None:
            return HttpResponse(status=404)
        return Response(data=users)


class User(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, user_id):
        """
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
        user = API.getUser(user_id)
        if user is None:
            return HttpResponse(status=404)
        return Response(data=user)

    def post(self, request, user_id):
        """
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: user_id
                    required: true
                    paramType: path
                    type: string
                  - name: broker keys
                    required: true
                    paramType: body
                    type: json

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
                  - code: 422
                    message: Missing 'broker key' parameter inside the body
                  - code: 409
                    message: The user already exists
        """
        broker_keys = json.dumps(request.data)
        if broker_keys == "{}":
            return HttpResponse("No keys were provided", status=422)
        res = API.addUser(user_id, broker_keys)
        if not res:
            return HttpResponse("The user " + user_id + " already exists", status=409)
        return HttpResponse(status=200)

    def delete(self, request, user_id):
        """
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
        if API.deleteUser(user_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)
