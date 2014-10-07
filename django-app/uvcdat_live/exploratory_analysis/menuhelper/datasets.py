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

def is_in_ACME(user):
    return user.groups.filter(name='ACME-test').exists()

def datasetListHelper1(request,user_id):

    print 'in datasetListHelper1 for user_id: ' + user_id
    #datasets = ['tropics_warming_th_q_co2']
    
    import glob
    
    datasets = []
    
    for f in glob.glob(default_sample_data_dir + '/*'):
      f_arr = f.split('/')
      #print 'f: ' + f_arr[len(f_arr)-1]
      datasets.append(f_arr[len(f_arr)-1])
    
    
    #Step 0 - get the user object
    user = User.objects.get(username=user_id)    
    
    
    #Step 1 - grab the groups that this user belongs to
    print 'groups: ' + str(user.groups.all())
    
    #example
    groups_list = ['ACME-test','Group2']
    
    
    #Step 2 - grab all the datasets that all groups in which a user can access 
    
    datasets_in_groups = []
    
    #example
    for group in groups_list:
        temp_list = []
        if group == 'ACME-test':
            temp_list = ['dataset1','dataset2','dataset6']
        else:
            temp_list = ['dataset1','dataset3']
        datasets_in_groups = set(temp_list).union(datasets_in_groups)
    
    #ACMEtest_list = ['dataset1','dataset2','dataset6']
    #Group2_list = ['dataset1','dataset3']
    #take intersection of these groups ^^^^
    #datasets_in_groups = set(ACMEtest_list).union(Group2_list)
    #print 'datasets_in_groups: ' + str(list(datasets_in_groups))
    
    
    #Step 3 - read all the datasets from the root directory
    
    datasets_in_cades = ['dataset1','dataset2','dataset3','dataset4','dataset5']
    
    
    #Step 4 - take the intersection of steps 1 and 3
    datasets_set_returned = set(datasets_in_groups).intersection(datasets_in_cades)
    
    datasets_list_returned = list(datasets_set_returned)
    
    #Step 5 - return result to the app
    data = {'datasets' : datasets_list_returned}
    data_string = json.dumps(data,sort_keys=False,indent=2)
    #datasets = (glob.glob('/Users/8xo/djangoapp_data/*'));
    
    print 'data_string: ' + str(data_string)
    
    '''
    from django.contrib.auth.models import User
    user = User.objects.get(username=user_id)
    
    print 'groups: ' + str(user.groups.all())
    print 'datasets: ' + str(datasets)
    print 'is in ACME-test?: ' + str(is_in_ACME(user))
    
    if not is_in_ACME(user):
        datasets.remove('tropics_warming_th_q_co2_3year')
    
    
    print 'datasets: ' + str(datasets)
    
    data =  { 'datasets' : datasets }
    data_string = json.dumps(data,sort_keys=False,indent=2)
    #print 'JSON:',data_string
    '''
    
    return data_string
    
    

def datasetListHelper(request,user_id):
    print 'in datasetListHelper for user_id: ' + user_id
    
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
