from django.conf.urls import url
from datastore.views import NfConfigurationView as view


urlpatterns = [
    url(r'^/(?P<user_id>[^/]+)$', view.ConfigurationByuser.as_view(), name="All the NF Configurations of a specific user"),
	url(r'^/(?P<user_id>[^/]+)/(?P<configuration_id>[^/]+)$', view.Configuration.as_view(), name="NF Configuration")
]
