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
    
    from django.contrib.auth.models import User
    
    '''
    if User.DoesNotExist:
        user = User(username=user_id,
                         password='password is not used, ESGF handles authentication for us')
        user.save()
    '''
    
    
    #Step 0 - get the user object
    user = User.objects.get(username=user_id)    
    
    
    #Step 1 - grab the groups that this user belongs to
    #This will involve a call to the ESGF node
    #print 'groups: ' + str(user.groups.all())
    
    #example
    groups_list = ['ACME','OTHER']
    
    #examples
    jfhNone_response_str = '{ "groups" : [] }'
    jfhCSSEF_response_str = '{ "groups": [ "CSSEF" ] }'
    jfhACME_response_str = '{ "groups": [ "ACME" ] }'
    jfhACMECSSEF_response_str = '{ "groups" : [ "ACME" , "CSSEF" ] }'
    jfharney_response_str = '{ "groups" : [ "ACME" , "CSSEF" ] }'
    
    response_str = ''
    
    if user.username == 'None':
        print 'None user'
        response_str = jfhNone_response_str
    elif user.username == 'jfhCSSEF':
        print 'jfhCSSEF user'
        response_str = jfhCSSEF_response_str
    elif user.username == 'jfhACME':
        print 'jfhACME user'
        response_str = jfhACME_response_str
    elif user.username == 'jfhACMECSSEF':
        print 'jfhACMECSSEF user'
        response_str = jfhACMECSSEF_response_str
    elif user.username == 'jfharney':
        print 'jfharney user'
        response_str = jfharney_response_str
    else:
        response_str = jfhNone_response_str
    
    import json 
    
    response_json = json.loads(response_str)
    
    g_list = []
    for group in response_json['groups']:
        print 'group: ' + str(group)
        g_list.append(group)
    
    print 'g_list: ' + str(g_list)
    
    groups_list = g_list
    
    #Step 2 - grab all the datasets that all groups in which a user can access 
    
    datasets_in_groups = []
    
    from exploratory_analysis.models import Dataset_Access
    
    for group_name in groups_list:
        da = Dataset_Access.objects.filter(group_name=group_name)
        if da:
            print 'da'
            new_dataset_list_str = da[0].dataset_list
            
            print 'da datasetlists: ' + new_dataset_list_str
            
            for dataset_item in new_dataset_list_str.split(','):
                datasets_in_groups.append(dataset_item)
                print 'dataset_item: ' + dataset_item
        
    
    #take intersection of these groups ^^^^
    #datasets_in_groups = set(ACMEtest_list).union(Group2_list)
    
    #Step 3 - read all the datasets from the root directory
    #list of datasets
    
    import glob
    
    disk_datasets = []
    
    for f in glob.glob(default_sample_data_dir + '/*'):
      f_arr = f.split('/')
      #print 'f: ' + f_arr[len(f_arr)-1]
      disk_datasets.append(f_arr[len(f_arr)-1])
    
    print 'datasets on hard drive: ' + str(disk_datasets)
    
    
    #datasets_in_cades = ['dataset1','dataset2','dataset3','dataset4','dataset5']
    
    
    #Step 4 - take the intersection of steps 1 and 3
    #datasets_set_returned = set(datasets_in_groups).intersection(datasets_in_cades)
    #set(b1).intersection(b2)
    datasets_lists_returned = list(set(datasets_in_groups).intersection(disk_datasets))
    
    print 'intersection of datasets: ' + str(datasets_lists_returned)
    
    #Step 5 - return result to the app
    data = {'datasets' : datasets_lists_returned } #datasets_in_groups}
    data_string = json.dumps(data,sort_keys=False,indent=2)
    #datasets = (glob.glob('/Users/8xo/djangoapp_data/*'));
    
    print 'data_string: ' + str(data_string)
    
    
    
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
