import json

def datasetListHelper1(request,user_id):

    print 'in datasetListHelper1'
    datasets = ['tropics_warming_th_q_co2']
    data =  { 'datasets' : datasets }
    data_string = json.dumps(data,sort_keys=False,indent=2)
    print 'JSON:',data_string
    
    return data_string
    
    

def datasetListHelper(request,user_id):
    
    print '\n\n\nUSERr:' + user_id
  
    #grab the username
    username = 'jfharney'
      
    #list of paths
    paths = ['path1','path2','path3']
    
    #list of datasets
    datasets = ['dataset1','dataset2','tropics_warming_th_q_co2']
    
    
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
    
    return data_string
    #return HttpResponse(data_string)
