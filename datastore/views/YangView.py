import datastore.services.YangService as API
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from datastore.parsers.YANGParser import YANGParser


class YANGModelsAll(APIView):
    parser_classes = (YANGParser,)

    def get(self, request):
        '''
        Retrieve all tye YANG model stored into the repository
        '''
        yang = API.getAllYANG_model()
        if yang is None:
            return HttpResponse(status=404)
        return Response(data=yang)


class YANGModels(APIView):
    parser_classes = (YANGParser,)

    def get(self, request, yang_id):
        '''
        Retrieve a YANG model given the yang id
        '''
        yang = API.getYANG_model(yang_id)
        if yang is None:
            return HttpResponse(status=404)
        return Response(data=yang)

    def delete(self, request, yang_id):
        '''
        Delete a YANG model given the yang id
        '''
        if API.deleteYANG_model(yang_id):
            return HttpResponse(status=200)
        return HttpResponse(status=404)

    def post(self, request, yang_id):
        '''
        Insert a new YANG model into the repository.
        Before saving the yang model into the DB, it is checked that the it is sintactically correct
        '''
        yang_model = request.data
        res = API.addYANG_model(yang_id, yang_model)
        return HttpResponse(status=200)

    def put(self, request, yang_id):
        '''
        Update a YANG model
        '''
        yang_model = request.data
        if API.updateYANG_model(yang_id, yang_model):
            return HttpResponse(status=200)
        return HttpResponse(status=404)


class YIN(APIView):
    def get(self, request, yang_id):
        '''
        Retrieve the YIN associated to a YANG model.
        The YIN is generated run time for each request by pyang
        '''
        yin = API.getYINFromYangID(yang_id)
        if yin is None:
            return HttpResponse(status=404)
        return Response(data=yin)
