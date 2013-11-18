
# Create your views here.

from django.http import HttpResponse
from django.template import RequestContext, loader

from exploratory_analysis.models import Diags

import json

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


def datasets(request):
    
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


  


