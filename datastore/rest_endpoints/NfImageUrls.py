from django.conf.urls import url
from datastore.views import NfImageView as view

urlpatterns = [
        url(r'^/chunked_upload/?$', view.MyChunkedUploadView.as_view(), name='api_chunked_upload'),
        url(r'^/chunked_upload_complete/?$', view.MyChunkedUploadCompleteView.as_view(), name='api_chunked_upload_complete'),
        url(r'^/(?P<vnf_id>[^/]+)/$', view.VNF_Image.as_view(), name='VNF image'),
        url(r'^/(?P<vnf_id>[^/]+)/template$', view.Template.as_view(), name='Template of the image')
]
