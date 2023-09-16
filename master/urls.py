from django.urls import path
from . import views

urlpatterns = [
    path('get_configuration_data/', views.GetConfiguration.as_view(), name="get_configuration_data"),
    path('get_configuration_data/<organization_id>', views.GetConfiguration.as_view(), name="get_configuration_data"),
    path('save_default_configuration/', views.SaveDefaultConfiguration.as_view(), name="save_default_configuration"),
]
