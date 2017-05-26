from django.conf.urls import url
from datastore import views

urlpatterns = [
    url(r'^/all/$', views.VNFTemplateAll.as_view(), name='VNF Template'),
    url(r'^/(?P<vnf_id>[^/]+)/$', views.VNFTemplate.as_view(), name='VNF List'),
    url(r'^/image/(?P<vnf_id>[^/]+)/$', views.VNFImage.as_view(), name='VNF image'),
    url(r'^/nf_fgraphs/(?P<nf_fgraph_id>[^/]+)/$', views.NFFGraphs.as_view(), name='NFFGraphs'),
    url(r'^/nf_fgraphs/$', views.NFFGResource.as_view(), name='NFFGResource'),
    url(r'^/nf_fgraphs/all_graphs_names$', views.nffg_digest.as_view(), name='nf_fgraphs list name'),
]
