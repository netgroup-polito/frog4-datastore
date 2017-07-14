from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import datastore.services.NfCapabilityService as API


class Capability(APIView):
    def get(self, request, capability):
        """
        Get the all VNF with the respectively capability
        """
        try:
            template = API.getTemplatesFromCapability(capability)
            if template is None:
                return HttpResponse(status=404)
            return Response(data=template)
        except:
            return HttpResponse(status=400)