from django.conf.urls import url
from datastore.views import VnfInstanceView as view


urlpatterns = [
	url(r'^$', view.VNFAll.as_view(),name="Retrieve all the VNFs"),
	url(r'^/(?P<configuration_id>[^/]+)$', view.VNF.as_view(),name="Deploy a VNF"),
	url(r'^/(?P<configuration_id>[^/]+)/bootconfiguration$', view.VNFBootingConfiguration.as_view(),name="CRUD on the booting configuration of a VNF"),
	#url(r'^/status$', views.VNFStatus.as_view(),name="CRUD on the current status of the VNF"),
	url(r'^/(?P<configuration_id>[^/]+)/restendpoint$', view.RestEndpoint.as_view(),name="CRUD on the REST endpoint of the VNF")
]

