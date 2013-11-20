
# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader

from exploratory_analysis.models import Diags

import json

def tree(request):
  template = loader.get_template('exploratory_analysis/treeview.html')
  #template = loader.get_template('exploratory_analysis/tree.html')
  context = RequestContext(request, {
    'a' : 'aaaaa',
    })
  
  return HttpResponse(template.render(context))
  
  
  
  
def treedata(request,user_id):
    
    username = user_id
  

    file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare2.json';

    from pprint import pprint

    data = ''
    with open(file) as data_file:    
        data = json.load(data_file)
        pprint(data)
    
    url = 'http://cds.ccs.ornl.gov/y9s/singlef/i1850cn_cruncep_CNDA_Cli_b_2000-2009-i1850cn_cruncep_ctl_2000-2009/setsIndex.html'
    
    children_arr = [ { "name": "Set 1" } ]
    
    #data = { 'name' : 'LND_DIAG', 'url' : url, 'children' : children_arr }
    data_string = json.dumps(data,sort_keys=True,indent=2)
    print 'JSON:',data_string
            
            
            
    
    return HttpResponse(data_string)
    


def maps(request):
  print request.GET.get('q')
  template = loader.get_template('exploratory_analysis/mapview.html')
  context = RequestContext(request, {
    'a' : 'aaaaa',
  })
#  latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#  template = loader.get_template('polls/index.html')
#  context = RequestContext(request, {
#    'latest_poll_list' : latest_poll_list,
#  })

  return HttpResponse(template.render(context))




def index(request):
  print request.GET.get('q')
  template = loader.get_template('exploratory_analysis/index.html')
  context = RequestContext(request, {
    'a' : 'aaaaa',
  })
#  latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
#  template = loader.get_template('polls/index.html')
#  context = RequestContext(request, {
#    'latest_poll_list' : latest_poll_list,
#  })

  return HttpResponse(template.render(context))

def datasets(request,user_id):
  
  username = 'jfharney'
  
  #list of paths
  paths = ['path1','path2','path3']

  #list of datasets
  datasets = ['dataset1','dataset2','dataset3']


  #list of year range per dataset
  dataset1years = ['150','151','152']
  dataset2years = ['150','151','152']
  dataset3years = ['150','151','152']

  year_range = [dataset1years, dataset2years, dataset3years]
    
  data =  { 'username' : username, 'datasets' : datasets, 'paths' : paths, 'year_range' : year_range }
  print 'DATA:',repr(data)
  data_string = json.dumps(data,sort_keys=True,indent=2)
  print 'JSON:',data_string
  data_string = json.dumps(data,sort_keys=False,indent=2)
  print 'JSON:',data_string

  jsonStr = json.loads(data_string)

    
    

  return HttpResponse(data_string)


def variables(request,dataset_id):
  
  #dataset_id = 'dataset1'
  if(dataset_id == None):
      dataset_id = 'dataset1' 
  
  if(dataset_id == 'dataset3'):
      variables = ['AR','BTRAN','CWDC','DEADCROOTC','DEADSTEMC','ER','FROOTC','FSDS','GPP','HR','LIVECROOTC','LIVESTEMC','NEE','NPP','PCO2', 'RAIN', 'TBOT', 'TLAI', 'TOTECOSYSC', 'TOTLITC','TOTSOMC','TOTVEGC', 'WOODC'    ]
  else:
      variables = ['ALL', 'AR','BTRAN','CWDC','DEADCROOTC','DEADSTEMC','ER','FROOTC','FSDS','GPP','HR','LIVECROOTC','LIVESTEMC','NEE','NPP','PCO2', 'RAIN', 'TBOT', 'TLAI', 'TOTECOSYSC', 'TOTLITC','TOTSOMC','TOTVEGC', 'WOODC'    ]
  
  data =  { 'dataset_id' : dataset_id, 'variables' : variables }
  print 'DATA:',repr(data)
  data_string = json.dumps(data,sort_keys=True,indent=2)
  #print 'JSON:',data_string
  #data_string = json.dumps(data,sort_keys=False,indent=2)
  #print 'JSON:',data_string

  jsonStr = json.loads(data_string)


  return HttpResponse(data_string)






def times(request,variable_id):
  
    print 'times for variable ', variable_id
  
    #dataset_id = 'dataset1'
    if(variable_id == None):
        variable_id = 'AR' 
  
    if(variable_id == 'AR'):
        times = ['jan','feb','mar']
    else:
        times = ['april','may','june']
    
    data =  { 'variable_id' : variable_id, 'times' : times }
    print 'DATA:',repr(data)
    data_string = json.dumps(data,sort_keys=True,indent=2)
    jsonStr = json.loads(data_string)
    
    return HttpResponse(data_string)







def visualizations(request):
    
  print request.GET.get('variable')
  
  variable = ''
  if(request.GET.get('variable') == None):
      variable = 'AR'
  else:
      variable = request.GET.get('variable')
  
  #file = '/Users/csg/Desktop/uvcdat-web/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/' + variable + '.json' 
  file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/' + variable + '.json' 
  
 
  with open(file , 'r') as myfile:
      data = myfile.read().replace('\n','')
      
  jsonData = json.dumps(data)

  #jsonData = json.dumps("{ 'variable' : '" + variable  +  "'} ")
  #print jsonData
  return HttpResponse(jsonData)


def getDatasetListJSONStr(user_id):
    
  #list of paths
  paths = ['path1','path2','path3']

  #list of datasets
  datasets = ['dataset1','dataset2','dataset3']


  #list of year range per dataset
  dataset1years = ['150','151','152']
  dataset2years = ['150','151','152']
  dataset3years = ['150','151','152']

  year_range = [dataset1years, dataset2years, dataset3years]
    
  data =  { 'datasets' : datasets, 'paths' : paths, 'year_range' : year_range }
  print 'DATA:',repr(data)
  data_string = json.dumps(data,sort_keys=True,indent=2)
  print 'JSON:',data_string
  data_string = json.dumps(data,sort_keys=False,indent=2)
  print 'JSON:',data_string

  jsonStr = json.loads(data_string)

  print jsonStr
  #print dir(json)

  return jsonStr



  

#
'''
#URL String:
  http://<host>/exploratory_analysis/datasetsList/<user_id>

lists all the datasets given a user
output is:
{
  user : '',
  datasets : [],
  paths: [],
  year_range: [[]]
  
}

'''
def datasetsList(request,user_id):
  #get user query parameter
  user = ''
  if(request.GET.get('user') == None):
      user = 'Chad'
  else:
      user = request.GET.get('user')
      
  
  
  #from the user, get all the datasets that are available to that user
  print user_id
  
  jsonStr = getDatasetListJSONStr(user_id)
  
  
  #print 'Returning dataset list for user ' + user
  
  return HttpResponse(jsonStr['year_range'][0])  


  


