from django.conf.urls import url
from datastore.views import NfCapabilityView as view


urlpatterns = [
	url(r'^/(?P<capability>[^/]+)$', view.Capability.as_view(), name="Capability")
]

