
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^/play', views.play, name='info'),
    url(r'^/simulate', views.simulate, name='simulate'),
]
