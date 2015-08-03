from django.conf.urls import patterns, url

from ea_services import views

from ea_services.views import PackagesView, Dataset_AccessView, PublishedView, VariablesView

urlpatterns = [
               
    #points to the main page view
    url(r'^$', views.index, name='index'),
    
    
    url(r'^dataset_packages/(?P<dataset_name>\w+)/$', PackagesView.as_view()),
    
    url(r'^dataset_access/(?P<group_name>\w+)/$', Dataset_AccessView.as_view()),
    
    url(r'^published/(?P<dataset_name>\w+)/$', PublishedView.as_view()),
    
    url(r'^variables/(?P<dataset_name>\w+)/$', VariablesView.as_view()),
    
    #service API for retrieving dataset_published flags
    #url(r'^dataset_published/(?P<dataset_name>\w+)/$',views.dataset_published,name='dataset_published'),  
    
    
    
]


#service API for retrieving dataset variables
#url(r'^dataset_variables/(?P<dataset_name>\w+)/$',views.dataset_variables,name='dataset_variables'),
    
    
#service API for retrieving dataset pacakages
#url(r'^dataset_packages/(?P<dataset_name>\w+)/$',views.dataset_packages,name='dataset_packages'),