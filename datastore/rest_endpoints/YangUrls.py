from django.conf.urls import url
from datastore.views import YangView as view

urlpatterns = [
    #url(r'^/(?P<vnf_type>[^/]+)/$', views.YANGmodels.as_view(), name='YANG models get or delete')
    url(r'^/(?P<yang_id>[^/]+)$', view.YANGModels.as_view(), name='YANG models get or delete'),
    url(r'^/yin/(?P<yang_id>[^/]+)$', view.YIN.as_view(), name='YIN of a given yang_id'),
    url(r'^$', view.YANGModelsAll.as_view(), name='Retrieve all the YANG models')
]
