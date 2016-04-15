from django.shortcuts import render
from django.http import Http404
from django.http import Http501
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
			raise Http404("VNF does not exist")
		return Response(data=template)
	
	def put(self, request, vnf_id):
		"""
		Update or create a new VNF template
		"""
		raise Http501()

	def delete(self, request, vnf_id):
		"""
		Delete an existig VNF template
		"""
		raise Http501()


class VNFImage(APIView):
	"""
	"""
	
	def get(self, request, vnf_id):
		"""
		Get the VNF template of a VNF
		"""
		raise Http501()
	
	def put(self, request, vnf_id):
		"""
		Update or create a new VNF template
		"""
		raise Http501()

	def delete(self, request, vnf_id):
		"""
		Delete an existig VNF template
		"""
		raise Http501()
