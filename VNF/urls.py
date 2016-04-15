from django.conf.urls import url
from PSA import views

urlpatterns = [ 
	url(r'^/(?P<vnf_id>[^/]+)/$', views.VNFList.as_view(), name='VNF List'),
	url(r'^/image/(?P<vnf_id>[^/]+)/$', views.VNFImage.as_view(), name='VNF image'),
]
