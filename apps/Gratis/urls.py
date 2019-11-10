from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^validate_login$', views.validate_login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^home$', views.home),
    url(r'^liveStocks$', views.liveStocks),
    # url(r'^home/(?P<user_id>\d+)$', views.home_user),
]