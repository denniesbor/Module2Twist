from . import views
from django.urls import path

from dashapp.test import test


urlpatterns = [
    path('',views.index, name='index'),
    path('charts/',views.charts, name='charts')
]
