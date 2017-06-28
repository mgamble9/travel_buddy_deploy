from django.conf.urls import url
from . import views
app_name = 'travel'
urlpatterns = [
    url(r'^$', views.index),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    url(r'^travel_dashboard$', views.travel_dashboard),
    url(r'^travel/add$', views.travel_add, name='travel_add'),
    url(r'^travel_add_trip$', views.travel_add_trip, name='travel_add_trip'),
    url(r'^join/(?P<id>\d+)$', views.join_trip, name='join_trip'),
    url(r'^destination/(?P<id>\d+)$', views.destination, name='destination'),

]
