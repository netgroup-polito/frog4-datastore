import json
import datastore.services.UserService as API
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from datastore.parsers.TextParser import PlainTextParser


class UserAll(APIView):

    def get(self, request):
        """
            Get all  the users
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

    def post(self, request):
        """
            Create a new user
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: user_and_password
                    required: true
                    paramType: body
                    type: json

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
                  - code: 422
                    message: Missing password inside the body
                  - code: 409
                    message: The user already exists
        """
        if 'password' not in request.data:
            return HttpResponse("No password was provided", status=422)
        if 'username' not in request.data:
            return HttpResponse("No username was provided", status=422)
        username = request.data['username']
        password = request.data['password']
        res = API.addUser(username, password)
        if not res:
            return HttpResponse("The user " + username + " already exists", status=409)
        return HttpResponse(status=200)


class User(APIView):
    parser_classes = (PlainTextParser,)

    def get(self, request, user_id):
        """
            Get the user given the username
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

    def put(self, request, user_id):
        """
            Modify the password of a specific user
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: user_id
                    required: true
                    paramType: path
                    type: string
                  - name: password
                    required: true
                    paramType: body
                    type: json

              consumes:
                  - text/plain
              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
                  - code: 422
                    message: Missing password inside the body
        """
        password = request.data
        if password == "{}":
            return HttpResponse("No password was provided", status=422)
        res = API.updateUser(user_id, password)
        if not res:
            return HttpResponse("The user " + user_id + " does not exist", status=409)
        return HttpResponse(status=200)

    def delete(self, request, user_id):
        """
            Delete a user
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


class BrokerKeys(APIView):
    parser_classes = (JSONParser,)

    def get(self, request, user_id):
        """
            Get the broker keys of a user
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
        keys = API.getUserKeys(user_id)
        if keys is None:
            return HttpResponse(status=404)
        return Response(data=keys)

    def put(self, request, user_id):
        """
            Update the broker keys of a user
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
        broker_keys = request.data
        if broker_keys == {}:
            return HttpResponse("No keys were provided", status=422)
        res = API.updateUserKeys(user_id, json.dumps(broker_keys))
        if not res:
            return HttpResponse("The user " + user_id + " does not exist", status=404)
        return HttpResponse(status=200)

    def delete(self, request, user_id):
        """
            Delete the broker keys of a user
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
        if API.deleteUserKeys(user_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)


class UserConnectedAll(APIView):
    def get(self, request):
        """
            Get all the users connected to the FROG architecture
              ---
              # YAML (must be separated by `---`)
              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
        """
        users = API.getAllUsersConnected()
        if users is None:
            return HttpResponse(status=404)
        return Response(data=users)


class UserFromToker(APIView):
    def get(self, request, token):
        """
            Get the user associated to the given token
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: token
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
        """
        user = API.getUserFromToken(token)
        if user is None:
            return HttpResponse(status=404)
        return Response(data=user)


class Login(APIView):
    def post(self, request):
        """
            Login to the FROG architecture
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: authentication
                    required: true
                    paramType: body
                    type: json

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 401
                    message: Authentication failed
                  - code: 422
                    message: Missing password inside the body
        """
        if 'password' not in request.data:
            return HttpResponse("No password was provided", status=422)
        if 'username' not in request.data:
            return HttpResponse("No user was provided", status=422)
        user = request.data['username']
        password = request.data['password']
        token = API.login(user, password)
        if token is None:
            return HttpResponse("Login failed", status=401)
        return HttpResponse(token, status=200)
