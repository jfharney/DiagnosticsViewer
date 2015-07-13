from django.conf.urls import patterns, url

from exploratory_analysis import views

from exploratory_analysis.views import PackagesView, Dataset_AccessView, PublishedView, VariablesView

urlpatterns = [
               
    #points to the main page view
    url(r'^$', views.index, name='index'),
    
    #login view
    url(r'^login/$',views.login,name='login'),
    
    #auth view
    url(r'^auth/$',views.auth,name='auth'),
    
    #main page view
    url(r'^main/(?P<user_id>\w+)/$',views.main,name='main'),
    
    #service API for retrieving dataset variables
    #url(r'^dataset_variables/(?P<dataset_name>\w+)/$',views.dataset_variables,name='dataset_variables'),
    
    
    #service API for retrieving dataset pacakages
    #url(r'^dataset_packages/(?P<dataset_name>\w+)/$',views.dataset_packages,name='dataset_packages'),
    url(r'^dataset_packages/(?P<dataset_name>\w+)/$', PackagesView.as_view()),
    
    
    url(r'^dataset_access/(?P<group_name>\w+)/$', Dataset_AccessView.as_view()),
    
    
    url(r'^published/(?P<dataset_name>\w+)/$', PublishedView.as_view()),
    
    url(r'^variables/(?P<dataset_name>\w+)/$', VariablesView.as_view()),
    
    #service API for retrieving dataset_published flags
    #url(r'^dataset_published/(?P<dataset_name>\w+)/$',views.dataset_published,name='dataset_published'),  
    
    
    
]