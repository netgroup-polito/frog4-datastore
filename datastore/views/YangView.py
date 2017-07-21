import datastore.services.YangService as API
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from datastore.parsers.YANGParser import YANGParser


class YANGModelsAll(APIView):
    parser_classes = (YANGParser,)

    def get(self, request):
        """
            Retrieve all the YANG models stored
              ---
              # YAML (must be separated by `---`)
              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
        """
        yang = API.getAllYANG_model()
        if yang is None:
            return HttpResponse(status=404)
        return Response(data=yang)


class YANGModels(APIView):
    parser_classes = (YANGParser,)

    def get(self, request, yang_id):
        """
              Retrieve a YANG models given the yang id
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: yang_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
                  - code: 400
                    message: Bad request
        """
        yang = API.getYANG_model(yang_id)
        if yang is None:
            return HttpResponse(status=404)
        return Response(data=yang)

    def delete(self, request, yang_id):
        """
              Delete a YANG models given the yang id
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: yang_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
                  - code: 400
                    message: Bad request
        """
        if API.deleteYANG_model(yang_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)

    def post(self, request, yang_id):
        """
              Insert a new YANG models into the repository.
              Before saving the yang models into the DB, it is checked that the it is sintactically correct
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: yang_id
                    required: true
                    paramType: path
                    type: string
                  - name: yang models
                    required: true
                    paramType: body
                    type: application/yang
              consumes:
                  - application/yang
              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 422
                    message: Missing yang models inside the body
                  - code: 409
                    message: The yang already exists
                  - code: 400
                    message: Bad request
        """
        yang_model = request.data
        res = API.addYANG_model(yang_id, yang_model)
        return HttpResponse(status=200)

    def put(self, request, yang_id):
        """
              Update a YANG models
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: yang_id
                    required: true
                    paramType: path
                    type: string
                  - name: yang models
                    required: true
                    paramType: body
                    type: application/yang

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
                  - code: 422
                    message: Missing yang models inside the body
                  - code: 400
                    message: Bad request
        """
        yang_model = request.data
        if API.updateYANG_model(yang_id, yang_model):
            return HttpResponse(status=200)
        return HttpResponse(status=404)


class YIN(APIView):
    def get(self, request, yang_id):
        """
              Retrieve the YIN associated to a YANG models.
              The YIN is generated run time for each request by pyang
              ---
              # YAML (must be separated by `---`)
              parameters:
                  - name: yang_id
                    required: true
                    paramType: path
                    type: string

              responseMessages:
                  - code: 200
                    message: Ok
                  - code: 404
                    message: Not found
                  - code: 400
                    message: Bad request
        """
        yin = API.getYINFromYangID(yang_id)
        if yin is None:
            return HttpResponse(status=404)
        return Response(data=yin)
