from django.conf.urls import patterns, url

from exploratory_analysis import views

from exploratory_analysis.views import PackagesView, Dataset_AccessView

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    
    
    
    
    
    
    #service API for retrieving dataset variables
    #url(r'^dataset_variables/(?P<dataset_name>\w+)/$',views.dataset_variables,name='dataset_variables'),
    
    
    #service API for retrieving dataset pacakages
    #url(r'^dataset_packages/(?P<dataset_name>\w+)/$',views.dataset_packages,name='dataset_packages'),
    url(r'^dataset_packages/(?P<dataset_name>\w+)/$', PackagesView.as_view()),
    
    
    url(r'^dataset_access/(?P<group_name>\w+)/$', Dataset_AccessView.as_view()),
    
    
    
    
    #service API for retrieving dataset_published flags
    #url(r'^dataset_published/(?P<dataset_name>\w+)/$',views.dataset_published,name='dataset_published'),  
    
    
    
]