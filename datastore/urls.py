from django.conf.urls import url
from datastore import views

urlpatterns = [
	url(r'^/all/$', views.VNFTemplateAll.as_view(), name='VNF Template'),
	url(r'^/(?P<vnf_id>[^/]+)/$', views.VNFTemplate.as_view(), name='VNF List'),
	url(r'^/image/(?P<vnf_id>[^/]+)/$', views.VNFImage.as_view(), name='VNF image'),
	url(r'^/nf_fgraphs/(?P<nf_fgraphs_id>[^/]+)/$', views.NFFGraphs.as_view(), name='NFFGraphs data'),
	url(r'^/nf_fgraphs/all$', views.NF_FGraphsAll.as_view(), name='nf_fgraphs list'),
	url(r'^/nf_fgraphs/all_graphs_names$', views.NF_FGraphsAll_graphs_names.as_view(), name='nf_fgraphs list name'),
]
