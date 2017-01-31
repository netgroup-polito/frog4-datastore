from django.conf.urls import url
from datastore import views

urlpatterns = [
    #url(r'^/(?P<vnf_type>[^/]+)/$', views.YANGmodels.as_view(), name='YANG model get or delete')
    url(r'^/(?P<yang_id>[^/]+)/$', views.YANGModels.as_view(), name='YANG model get or delete'),
    url(r'^/yin/(?P<yang_id>[^/]+)/$', views.YIN.as_view(), name='YIN of a given yang_id'),
    url(r'^/$', views.YANGModelsAll.as_view(), name='Retrieve all the YANG models')
]
