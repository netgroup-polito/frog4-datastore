from django.conf.urls import url
from datastore.views import NfTemplateView as view


urlpatterns = [
    url(r'^$', view.VNFTemplateAll.as_view(), name='VNF Template'),
    url(r'^/(?P<template_id>[^/]+)$', view.VNFTemplate.as_view(), name='VNF List'),
]