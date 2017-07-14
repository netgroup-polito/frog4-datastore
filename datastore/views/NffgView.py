import json
import datastore.services.NffgService as API
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from nffg_library.exception import InexistentLabelFound
from nffg_library.exception import NF_FGValidationError
from nffg_library.exception import WrongNumberOfPorts
from nffg_library.validator import ValidateNF_FG


class NFFGraphs(APIView):
    def put(self, request, user_id, graph_id):
        """
        Update a Network Functions Forwarding Graph
        ---
         # YAML (must be separated by `---`)
            parameters:
                - name: user_id
                  required: true
                  paramType: path
                  type: string
                - name: graph_id
                  required: true
                  paramType: path
                  type: string
                - name: nffg
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
        try:
            ValidateNF_FG().validate(request.data)
            nffg = json.dumps(request.data)
            if not API.updateNF_FGraphs(user_id, graph_id, nffg):
                return HttpResponse("NFFG of user " + user_id + " with ID " + graph_id + " not found", status=404)
        except (NF_FGValidationError, WrongNumberOfPorts, InexistentLabelFound) as error:
            return HttpResponse("NFFG validation failed: " + error.message, status=400)
        response_uuid = dict()
        response_uuid["nffg-uuid"] = graph_id
        return HttpResponse(json.dumps(response_uuid), status=200)

    def delete(self, request, user_id, graph_id):
        """
        Delete an existig Network Functions Forwarding Graph
        ---
        # YAML (must be separated by `---`)
            parameters:
                - name: user_id
                  required: true
                  paramType: path
                  type: string
                - name: graph_id
                  required: true
                  paramType: path
                  type: string

            responseMessages:
                - code: 200
                  message: Ok
                - code: 404
                  message: Not found
        """
        try:
            if API.deleteNF_FGraphs(user_id, graph_id):
                return HttpResponse(status=200)
            return HttpResponse(status=404)
        except:
            return HttpResponse(status=400)

    def get(self, request, user_id, graph_id):
        """
        Get the Network Functions Forwarding Graph
        ---
        # YAML (must be separated by `---`)
            parameters:
                - name: user_id
                  required: true
                  paramType: path
                  type: string
                - name: graph_id
                  required: true
                  paramType: path
                  type: string

            responseMessages:
                - code: 200
                  message: Ok
                - code: 404
                  message: Not found
        """
        try:
            nffg = API.getNF_FGraphs(user_id, graph_id)
            if nffg is None:
                return HttpResponse(status=404)
            return Response(data=nffg)
        except:
            return HttpResponse(status=400)


class NFFGByUser(APIView):
    def get(self, request, user_id):
        """
        Get all the NFFGs of the specified user
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
        nffgs = API.getNFFGByUser(user_id)
        if nffgs is None:
            return HttpResponse(status=404)
        return Response(data=nffgs)

    def post(self, request, user_id):
        """
        Create a New Network Functions Forwarding Graph
        Deploy a graph
        ---
            # YAML (must be separated by `---`)
            parameters:
                - name: user_id
                  required: true
                  paramType: path
                  type: string
                - name: nffg
                  required: true
                  paramType: body
                  type: json

            responseMessages:
                - code: 200
                  message: Ok
                - code: 404
                  message: Not found
        """
        nffg = request.data
        if nffg == {}:
            return HttpResponse("No nffg was provided", status=422)
        try:
            ValidateNF_FG().validate(request.data)
            nffg = json.dumps(request.data)
        except (NF_FGValidationError, WrongNumberOfPorts, InexistentLabelFound) as error:
            return HttpResponse("NFFG validation failed: " + error.message, status=400)
        graph_id = API.addNF_FGraphs(user_id, nffg)
        if graph_id is None:
            return HttpResponse("User " + user_id + " not found" , status=400)
        response_uuid = dict()
        response_uuid["nffg-uuid"] = graph_id
        return HttpResponse(json.dumps(response_uuid), status=200)


class NFFGAll(APIView):
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


class NffgDigest(APIView):
    def get(self, request):
        """
        Get all NFFGs digest
        """
        try:
            digest = API.getNffgDigest()
            if digest is None:
                return HttpResponse(status=404)
            return Response(data = digest)
        except Exception as e:
            return HttpResponse(e.message, status=400)
