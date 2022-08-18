from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('ajax_update/', update_data, name='update_data')
]