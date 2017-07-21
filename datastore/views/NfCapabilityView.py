from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import datastore.services.NfCapabilityService as API

class CapabilityAll(APIView):
    def get(self, request):
        """
        Get all the capabilities currently supported
        """
        capabilities = API.getAllCapabilities()
        if capabilities is None:
            return HttpResponse(status=404)
        return Response(data=capabilities)


class Capability(APIView):
    def get(self, request, capability):
        """
        Get all the templates with the respectively capability
        """
        try:
            template = API.getTemplatesFromCapability(capability)
            if template is None:
                return HttpResponse(status=404)
            return Response(data=template)
        except Exception as e:
            return HttpResponse(e.message, status=400)