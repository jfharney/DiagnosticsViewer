from django.conf.urls import patterns, url

from exploratory_analysis import views

print dir(views)

urlpatterns = patterns('',
  url(r'^$', views.index, name='index'),
  url(r'^treedata/(?P<user_id>\w+)/$', views.treedata, name='treedata'),
  #url(r'^ar/$', views.arData, name='ar'),
  url(r'^datasets/(?P<user_id>\w+)/$',views.datasets,name='datasets'),
  url(r'^variables/(?P<dataset_id>\w+)/$',views.variables,name='variables'),
  url(r'^times/(?P<variable_id>\w+)/$',views.times,name='times'),
  
  
  
  
  url(r'^tree/$', views.tree, name='tree'),
  url(r'^tree/treedata/(?P<user_id>\w+)/$', views.treedata, name='treedata'),
  #url(r'^ar/$', views.arData, name='ar'),
  url(r'^tree/datasets/(?P<user_id>\w+)/$',views.datasets,name='datasets'),
  url(r'^tree/variables/(?P<dataset_id>\w+)/$',views.variables,name='variables'),
  url(r'^tree/times/(?P<variable_id>\w+)/$',views.times,name='times'),
  
  
  url(r'^maps/$', views.maps, name='maps'),
  url(r'^maps/visualizations/$', views.visualizations, name='visualizations'),
  url(r'^maps/datasets/(?P<user_id>\w+)/$',views.datasets,name='datasets'),
  url(r'^maps/variables/(?P<dataset_id>\w+)/$',views.variables,name='variables'),
  url(r'^maps/times/(?P<variable_id>\w+)/$',views.times,name='times'),
  url(r'^maps/datasetsList/(?P<user_id>\d+)/$', views.datasetsList, name='datasetsList'),
#  url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
)

