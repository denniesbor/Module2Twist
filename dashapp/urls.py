from . import views
from django.urls import path

from dashapp.test import map,price_dist,price_quantity,climate,table,model


urlpatterns = [
    path('',views.index, name='index'),
    path('charts/',views.charts, name='charts'),
    path('table/',views.table,name='table'),
    path('model/',views.model,name='model'),
    path('report/',views.report,name='report')
]
