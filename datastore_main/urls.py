from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^docs/', include('rest_framework_swagger.urls')),
                       url(r'^yang', include('datastore.rest_endpoints.YangUrls')),
                       url(r'^user', include('datastore.rest_endpoints.UserUrls')),
                       url(r'^nffg', include('datastore.rest_endpoints.NffgUrls')),
                       url(r'^vnf', include('datastore.rest_endpoints.VnfInstanceUrls')),
                       url(r'^nf_template', include('datastore.rest_endpoints.NfTemplateUrls')),
                       url(r'^nf_capability', include('datastore.rest_endpoints.NfCapabilityUrls')),
                       url(r'^nf_image', include('datastore.rest_endpoints.NfImageUrls'))
                       )

urlpatterns += staticfiles_urlpatterns()
