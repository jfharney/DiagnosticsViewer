import json

def timeSeriesHelper(request):
    
    print 'in time series'
    
  
    print request.GET.get('variable')
  
    variable = ''
    if(request.GET.get('variable') == None):
         variable = 'AR'
    else:
         variable = request.GET.get('variable')
  
    #file = '/Users/csg/Desktop/uvcdat-web/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/' + variable + '.json' 
    #file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/' + variable + '.json' 
    #file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/src/time-plot-example/data/TLAI-avg.csv' 
    #file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/src/time-plot-example/data/time/TLAI-avg.json' 
    file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/time/TLAI-avg.json'
    
    data = ''
    with open(file , 'r') as myfile:
        data = myfile.read().replace('\n','')
      
    jsonData = json.dumps(data)

    return jsonData
