import json



import sys, os

sys.path.append(str(os.getcwd() + '/exploratory_analysis'))


from paths import paths

from defaults import parameter_defaults


syspath_append_uvcmetrics = paths.syspath_append_uvcmetrics
syspath_append_cdscan = paths.syspath_append_cdscan

paths_cache_dir = paths.cache_dir
#paths_front_end_cache_dir = paths.front_end_cache_dir

default_sample_data_dir = paths.default_sample_data_dir


def datasetListHelper1(request,user_id):

    #print 'in datasetListHelper1 for user_id: ' + user_id
    #datasets = ['tropics_warming_th_q_co2']
    
    import glob
    
    datasets = []
    
    for f in glob.glob(default_sample_data_dir + '/*'):
      f_arr = f.split('/')
      #print 'f: ' + f_arr[len(f_arr)-1]
      datasets.append(f_arr[len(f_arr)-1])
    
    #datasets = (glob.glob('/Users/8xo/djangoapp_data/*'));
    
    data =  { 'datasets' : datasets }
    data_string = json.dumps(data,sort_keys=False,indent=2)
    #print 'JSON:',data_string
    
    
    return data_string
    
    

def datasetListHelper(request,user_id):
    
    #print '\n\n\nUSERr:' + user_id
  
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
