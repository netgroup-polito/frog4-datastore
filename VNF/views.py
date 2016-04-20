from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import API
from subprocess import call
from django.core.exceptions import ObjectDoesNotExist
from ConfigParser import SafeConfigParser
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.db.models import Q
import os, logging
import xml.etree.ElementTree as ET
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.parsers import FileUploadParser, MultiPartParser
from subprocess import call
from xml.dom import minidom
import json


parser = SafeConfigParser()
parser.read('vnfRepo.conf')
logging.basicConfig(filename=parser.get('logging','filename'),format='%(asctime)s %(levelname)s:%(message)s', level=parser.get('logging','level'))

class VNFTemplate(APIView):
	"""
	"""
	
	def get(self, request, vnf_id):
		"""
		Get the VNF template of a VNF
		"""
		template = API.getVNFTemplate(vnf_id)
		if template is None:
			return HttpResponse(status=404)
		return Response(data=template)
	
	def put(self, request, vnf_id):
		"""
		Update or create a new VNF template
		"""
		if request.META['CONTENT_TYPE'] != 'application/json':
			return HttpResponse(status=415)
		try:
			template = json.dumps(request.data)
		except:
			return HttpResponse(status=400)	
		API.addVNFTemplate(vnf_id, template)
		return HttpResponse(status=200)

	def delete(self, request, vnf_id):
		"""
		Delete an existig VNF template
		"""
		if API.deleteVNFTemplate(vnf_id):
			return HttpResponse(status=200)
		return HttpResponse(status=404)
		
		


class VNFImage(APIView):
	"""
	"""
	
	def get(self, request, vnf_id):
		"""
		Get the VNF template of a VNF
		"""
		return HttpResponse(status=501)
	
	def put(self, request, vnf_id):
		"""
		Update or create a new VNF template
		"""
		return HttpResponse(status=501)

	def delete(self, request, vnf_id):
		"""
		Delete an existig VNF template
		"""
		return HttpResponse(status=501)
