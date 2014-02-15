from django.conf.urls import patterns, url

from exploratory_analysis import views

print dir(views)

urlpatterns = patterns('',
             
  ############
  #Page views#
  ############
  
  #points to the main page view
  url(r'^$', views.index, name='index'),
  
  url(r'^main/(?P<user_id>\w+)/$',views.main,name='main'),
  
  
  
  #points to the geo view
  url(r'^maps/(?P<user_id>\w+)/$', views.maps, name='maps'),
  
  #the diagnostic tree view
  #example url: http://localhost:8081/exploratory_analysis/treex/jfharney
  url(r'^treeex/(?P<user_id>\w+)/$', views.treeex, name='treeex'),
  
  
  
            
             
  ############
  #Services#
  ############
  
  #####Used in the geo page#####
  
  #grabs datasets given a user id (used in an ajax call)
  url(r'^datasets/(?P<user_id>\w+)/$',views.datasets,name='datasets'),
  
  #grabs variables given a dataset
  url(r'^variables/(?P<dataset_id>\w+)/$',views.variables,name='variables'),
  
  #grabs time info given a variable
  url(r'^times/(?P<variable_id>\w+)/$',views.times,name='times'),
  
  #grabs the map
  url(r'^visualizations/$', views.visualizations, name='visualizations'),
  
  
  
  
  url(r'^figure_generator/$', views.figureGenerator, name='figureGenerator'),
  
  #grabs the tree data
  url(r'^treedata/(?P<user_id>\w+)/$', views.treedata, name='treedata'),
  
  
  #grabs the timeseries data
  url(r'^timeseries/$', views.timeseries, name='timeseries'),
  
  ############
  #Tree stuff#
  ############
  url(r'^diagplot/$', views.diagplot, name='diagplot'),
  
  
  ############
  #Treeview bookmarks API#
  ############
  url(r'^tree_bookmarks/$', views.tree_bookmarks, name='tree_bookmarks'),
  url(r'^figure_bookmarks/$', views.figure_bookmarks, name='figure_bookmarks'),

  ############
  #Variables Names API#
  ############
  url(r'^variable_names/(?P<variable_short_name>\w+)/$', views.variable_names, name='variable_names'),
   
  
  #Not used but keeping just in case
  
  #points to the tree view
  url(r'^tree/$', views.tree, name='tree'),
  
  
  
  #login view
  url(r'^login/$',views.login,name='login'),
  
  
  
  
  url(r'^timeseries1/$',views.timeseries1,name='timeseries1'),
  
  
)

