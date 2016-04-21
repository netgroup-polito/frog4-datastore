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
from VNF.imageRepository.LocalRepository import LocalRepository

parser = SafeConfigParser()
parser.read(os.environ["VNF_REPO_CONF"])
logging.basicConfig(filename=parser.get('logging','filename'),format='%(asctime)s %(levelname)s:%(message)s', level=parser.get('logging','level'))
repository = parser.get('repository', 'repository')
if repository == "LOCAL_FILES":
	imagesDir = parser.get('General', 'IMAGE_DIR')
	imageRepo = LocalRepository(imagesDir)
	
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
		Get the disk image of a VNF
		"""
		try:
			(wrapper, fileLen) = imageRepo.getImage(vnf_id)
			response = HttpResponse(wrapper, content_type='text/plain', status=status.HTTP_200_OK)
			response['Content-Length'] = fileLen
			return response
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)
	
	def put(self, request, vnf_id):
		"""
		Insert/update a disk image for a VNF
		"""
		try:
			imageRepo.storeImage(vnf_id, request.data['file'])
			return HttpResponse(status=200)
		except:
			return HttpResponse(status=400)

	def delete(self, request, vnf_id):
		"""
		Remove a disk image for a VNF
		"""
		return HttpResponse(status=501)
