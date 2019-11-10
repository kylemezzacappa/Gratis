from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^bonuses$', views.bonuses),
    url(r'^create$', views.create),
    url(r'^validate_login$', views.validate_login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^process_bonus$', views.process_bonus),
    url(r'^bonus/(?P<bonus_id>\d+)$', views.edit_bonus),
    url(r'^myaccount/(?P<user_id>\d+)$', views.myaccount),
    url(r'^edit_account/(?P<id>\d+)$', views.edit_account),  #for editing users
    url(r'^process_edit/(?P<id>\d+)$', views.process_edit),  #for editing bonuses
    url(r'^delete_bonus/(?P<bonus_id>\d+)$', views.delete_bonus),
    url(r'^user_bonuses/(?P<quote_id>\d+)', views.user_bonuses),
]