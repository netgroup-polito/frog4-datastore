from django.conf.urls import url
from datastore.views import UserView as view


urlpatterns = [
	url(r'^$', view.UserAll.as_view(), name="Retrieve all the tenants"),
	url(r'^/(?P<user_id>[^/]+)$', view.User.as_view(), name="CRUD on tenant entity")
]

