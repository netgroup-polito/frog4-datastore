from django.conf.urls import url
from datastore import views


urlpatterns = [
	url(r'^$', views.UserAll.as_view(), name="Retrieve all the tenants"),
	url(r'^/(?P<user_id>[^/]+)$', views.User.as_view(), name="CRUD on tenant entity")
]

