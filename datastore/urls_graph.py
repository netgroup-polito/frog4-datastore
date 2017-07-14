from django.conf.urls import url
from datastore import views


urlpatterns = [
    url(r'^$', views.NFFGAll.as_view(), name='NFFGAll'),
    url(r'^/(?P<user_id>[^/]+)$', views.NFFGByUser.as_view(), name='NFFG by username'),
    url(r'^/(?P<user_id>[^/]+)/(?P<graph_id>[^/]+)$', views.NFFGraphs.as_view(), name='NFFGraphs'),
    url(r'^/digest$', views.nffg_digest.as_view(), name='nf_fgraphs list name')
    #url(r'^/$', views.GraphAll.as_view(),name="Retrieve all the graphs stored"),
    #url(r'^/$', views.Graph.as_view(),name="Update graph list"),
]