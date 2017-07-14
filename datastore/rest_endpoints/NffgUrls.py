from django.conf.urls import url
from datastore.views import NffgView as view


urlpatterns = [
    url(r'^$', view.NFFGAll.as_view(), name='NFFGAll'),
    url(r'^/digest$', view.NffgDigest.as_view(), name='nf_fgraphs list name'),
    url(r'^/(?P<user_id>[^/]+)$', view.NFFGByUser.as_view(), name='NFFG by username'),
    url(r'^/(?P<user_id>[^/]+)/(?P<graph_id>[^/]+)$', view.NFFGraphs.as_view(), name='NFFGraphs'),
]