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
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from .models import MyChunkedUpload
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

parser = SafeConfigParser()
parser.read(os.environ["VNF_REPO_CONF"])
logging.basicConfig(filename=parser.get('logging','filename'),format='%(asctime)s %(levelname)s:%(message)s', level=parser.get('logging','level'))
repository = parser.get('repository', 'repository')
if repository == "LOCAL_FILES":
	imagesDir = parser.get('General', 'IMAGE_DIR')
	imageRepo = LocalRepository(imagesDir)

class VNFTemplateAll(APIView):
	"""
	"""
	
	def get(self, request):
		"""
		Get the all VNF with the respectively template
		"""
		template = API.getVNFTemplate()
		if template is None:
			return HttpResponse(status=404)
		return Response(data=template)

	
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
		Insert/update a disk image for a VNF.
		DO NOT use this! A new API that supports upload of large files in chunks was developed.
		For further details see the example web client provided with this project.
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
		try:
			os.remove(os.path.join(imagesDir, vnf_id))
			return HttpResponse(status=200)
		except:
			return HttpResponse(status=400)


class NFFGraphs(APIView):
	"""
	"""
	def put(self, request, nf_fgraphs_id):
		"""
		Update or create a new Network Functions Forwarding Graph
		"""
		if request.META['CONTENT_TYPE'] != 'application/json':
			return HttpResponse(status=415)
		try:
			template = json.dumps(request.data)
		except:
			return HttpResponse(status=400)
		if API.addNF_FGraphs(nf_fgraphs_id, template) == False:
			return HttpResponse(status=400)
		return Response(data=json.loads(template))

	def delete(self, request, nf_fgraphs_id):
		"""
		Delete an existig Network Functions Forwarding Graph
		"""
		if API.deleteNF_FGraphs(nf_fgraphs_id):
			return HttpResponse(status=200)
		return HttpResponse(status=404)


	def get(self, request, nf_fgraphs_id):
		"""
		Get the Network Functions Forwarding Graph
		"""
		template = API.getNF_FGraphs(nf_fgraphs_id)
		#if template is None:
			#return HttpResponse(status=404)
		return Response(data=template)


class NF_FGraphsAll(APIView):
	"""
	"""
	def get(self, request):
		"""
		Get the all Network Functions Forwarding Graph
		"""
		template = API.getNF_FGraphs()
		if template is None:
			return HttpResponse(status=404)
		return Response(data=template)

class NF_FGraphsAll_graphs_names(APIView):
	"""
	"""
	def get(self, request):
		"""
		Get the all NFFGs Names and ids
		"""
		template = API.getNF_FGraphsAll_graphs_names()
		if template is None:
			return HttpResponse(status=404)
		return Response(data=template)


class Capability(APIView):

	def get(self, request, capability):
		"""
		Get the all VNF with the respectively capability
		"""
		template = API.getTemplatesFromCapability(capability)
		if template is None:
			return HttpResponse(status=404)
		return Response(data=template)

class MyChunkedUploadView(ChunkedUploadView):

	field_name = 'the_file'
	model = MyChunkedUpload

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(MyChunkedUploadView, self).dispatch(*args, **kwargs)

	def check_permissions(self, request):
	# Allow non authenticated users to make uploads
		pass


class MyChunkedUploadCompleteView(ChunkedUploadCompleteView):

	model = MyChunkedUpload

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(MyChunkedUploadCompleteView, self).dispatch(*args, **kwargs)

	def check_permissions(self, request):
	# Allow non authenticated users to make uploads
		pass

	def on_completion(self, uploaded_file, request):
	# Do something with the uploaded file
		imageRepo.storeImage(request.POST['vnf_id'], uploaded_file)

	def get_response_data(self, chunked_upload, request):
		filename = chunked_upload.filename
		offset = chunked_upload.offset
		chunked_upload.delete()
		return {'message': ("You successfully uploaded '%s' (%s bytes)!" % (filename, offset))}
