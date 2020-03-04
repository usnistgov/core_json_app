""" Url router for the main application
"""
from django.conf.urls import include
from django.urls import re_path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="REST API")

urlpatterns = [
    re_path(r'^json/', include('core_json_app.rest.urls')),
]
