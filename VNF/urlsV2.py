from django.conf.urls import url
from VNF import views

urlpatterns = [
        url(r'^/nf_template/$', views.VNFTemplateAll.as_view(), name='VNF Template'),
        url(r'^/nf_template/(?P<vnf_id>[^/]+)/$', views.VNFTemplate.as_view(), name='VNF List'),
        url(r'^/nf_image/(?P<vnf_id>[^/]+)/$', views.VNFImage.as_view(), name='VNF image'),
        #url(r'^/nffg/(?P<nffg_id>[^/]+)/$', views.NFFGTemplate.as_view(), name='NFFG data'),
        #url(r'^/nffg/$', views.NFFGAll.as_view(), name='NFFG list'),
	    url(r'^/nf_capability/(?P<capability>[^/]+)/$', views.Capability.as_view(), name='Capability')
]
