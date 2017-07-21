from django.conf.urls import url
from datastore.views import NfCapabilityView as view


urlpatterns = [
	url(r'^$', view.CapabilityAll.as_view(), name="Retrieve all the capabilities"),
	url(r'^/(?P<capability>[^/]+)$', view.Capability.as_view(), name="Capability")
]

