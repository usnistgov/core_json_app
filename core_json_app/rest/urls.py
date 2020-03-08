""" Url router for the REST API
"""

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from core_json_app.rest.data import views as data_views
from core_json_app.rest.template_version_manager import views as template_version_manager_views

urlpatterns = [

    url(r'^data/$', data_views.DataList.as_view(),
        name='core_json_app_rest_data_list'),

    url(r'^data/download/(?P<pk>\w+)/$', data_views.DataDownload.as_view(),
        name='core_json_app_rest_data_download'),

    url(r'^data/(?P<pk>\w+)/$', data_views.DataDetail.as_view(),
        name='core_json_app_rest_data_detail'),

    url(r'^template/user/$',
        template_version_manager_views.UserTemplateList.as_view(),
        name='core_json_app_rest_user_template_list'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
