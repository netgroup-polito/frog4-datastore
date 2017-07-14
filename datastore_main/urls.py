from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^v2', include('datastore.urls')),
                       url(r'^docs/', include('rest_framework_swagger.urls')),
                       url(r'^yang', include('datastore.urls_yang')),
                       url(r'^user', include('datastore.urls_user')),
                       url(r'^nffg', include('datastore.urls_graph')),
                       url(r'^vnf', include('datastore.urls_vnf'))
                       )

urlpatterns += staticfiles_urlpatterns()
