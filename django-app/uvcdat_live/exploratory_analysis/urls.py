from django.conf.urls import patterns, url

from exploratory_analysis import views

print dir(views)

urlpatterns = patterns('',
                       
  #points to the main page view
  url(r'^$', views.index, name='index'),
  
  #points to the geo view
  url(r'^maps/$', views.maps, name='maps'),
  
  #grabs datasets given a user id (used in an ajax call)
  url(r'^datasets/(?P<user_id>\w+)/$',views.datasets,name='datasets'),
  
  #grabs variables given a dataset
  url(r'^variables/(?P<dataset_id>\w+)/$',views.variables,name='variables'),
  
  #grabs time info given a variable
  url(r'^times/(?P<variable_id>\w+)/$',views.times,name='times'),
  
  #grabs the map
  url(r'^visualizations/$', views.visualizations, name='visualizations'),
  
  
  #points to the tree view
  url(r'^tree/$', views.tree, name='tree'),
  
  #grabs the tree data
  url(r'^treedata/(?P<user_id>\w+)/$', views.treedata, name='treedata'),
  
  
  #grabs the timeseries data
  url(r'^timeseries/$', views.timeseries, name='timeseries'),
  
  
  #url(r'^maps/datasets/(?P<user_id>\w+)/$',views.datasets,name='datasets'),
  #url(r'^maps/variables/(?P<dataset_id>\w+)/$',views.variables,name='variables'),
  #url(r'^maps/times/(?P<variable_id>\w+)/$',views.times,name='times'),
  #url(r'^maps/datasetsList/(?P<user_id>\d+)/$', views.datasetsList, name='datasetsList'),
#  url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
  
  
  ##url(r'^ar/$', views.arData, name='ar'),
  
  
  
  
  #url(r'^tree/treedata/(?P<user_id>\w+)/$', views.treedata, name='treedata'),
  ##url(r'^ar/$', views.arData, name='ar'),
  #url(r'^tree/datasets/(?P<user_id>\w+)/$',views.datasets,name='datasets'),
  #url(r'^tree/variables/(?P<dataset_id>\w+)/$',views.variables,name='variables'),
  #url(r'^tree/times/(?P<variable_id>\w+)/$',views.times,name='times'),
  
  
)

