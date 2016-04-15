from django.conf.urls import url
from VNF import views

urlpatterns = [ 
	url(r'^/(?P<vnf_id>[^/]+)/$', views.VNFTemplate.as_view(), name='VNF List'),
	url(r'^/image/(?P<vnf_id>[^/]+)/$', views.VNFImage.as_view(), name='VNF image'),
]
