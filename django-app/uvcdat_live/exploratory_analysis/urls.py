from django.conf.urls import patterns, url

from exploratory_analysis import views

print dir(views)

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  #url(r'^ar/$', views.arData, name='ar'),
  url(r'^datasets/$', views.datasets, name='datasets'),
  url(r'^datasetsList/(?P<user_id>\d+)/$', views.datasetsList, name='datasetsList'),
#  url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
)

