from django.conf.urls import url
from datastore.views import UserView as view


urlpatterns = [
    url(r'^$', view.UserAll.as_view(), name="Retrieve all the users"),
    url(r'^/token/(?P<token>[^/]+)$', view.UserFromToker.as_view(), name="Retrieve the user from the given token"),
    url(r'^/connected', view.UserConnectedAll.as_view(), name="Retrieve all the users logged"),
    url(r'^/login', view.Login.as_view(), name="login"),
    url(r'^/(?P<user_id>[^/]+)$', view.User.as_view(), name="CRUD on user entity"),
    url(r'^/(?P<user_id>[^/]+)/broker-keys$', view.BrokerKeys.as_view(), name="CRD on user broker keys")
]

