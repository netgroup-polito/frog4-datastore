from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'api.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	

	#url(r'^v1/status', include('v1status.urls')),
	#url(r'^v1/status', v1Status.as_view(), name='status'),
	
	url(r'^v1/VNF', include('VNF.urls')),
	url(r'^docs/', include('rest_framework_swagger.urls')),
)
urlpatterns += staticfiles_urlpatterns()
