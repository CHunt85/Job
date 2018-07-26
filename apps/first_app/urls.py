from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^dashboard$', views.dashboard),
    url(r'^add_fun$', views.add_fun),
    url(r'^new$', views.new),
    url(r'^login_fun$', views.login_fun),
    url(r'^destroy$', views.destroy),
    url(r'^logout$', views.logout),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^edit$', views.edit),
    url(r'^info/(?P<id>\d+)$', views.info),
    url(r'^edit_fun$', views.edit_fun),

]