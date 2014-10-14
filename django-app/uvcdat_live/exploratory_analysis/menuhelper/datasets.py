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


datasetListDebug = True


def getGroupsFromESGF(username):
        
    defaultGroups = '{ "groups" : [] }'    


    import urllib2
    data = urllib2.urlopen("http://esg.ccs.ornl.gov:7070/groups/" + username).read()


    return data



def datasetListHelper1(request,user_id):


    import glob
    import json
    from django.http import HttpResponse
    from django.http import HttpResponseServerError
    
    
    if datasetListDebug:
        print 'in datasetListHelper1 for user_id: ' + user_id
    #datasets = ['tropics_warming_th_q_co2']
    
    
    datasets = []
    
    for f in glob.glob(default_sample_data_dir + '/*'):
      f_arr = f.split('/')
      #print 'f: ' + f_arr[len(f_arr)-1]
      datasets.append(f_arr[len(f_arr)-1])
    
    from django.contrib.auth.models import User
    print 'dataset_list: ' + str(datasets)
    
    
    data = {'datasets' : datasets } #datasets_in_groups}
    data_string = json.dumps(data,sort_keys=False,indent=2)
    
    '''Commented out 10-14 so that a commit will be stable - still marked as TODO
    if datasetListDebug:
        print 'paths.esgfAccess: ' + str(paths.esgfAccess)
        
    
    #Step 0 - get the user object
    user = User.objects.get(username=user_id)    
    
    #print 'userrrrrrrr: ' + user.username
    
    if User.DoesNotExist:
        data = {'dataset_list' : ''}
        data_string = json.dumps(data,sort_keys=False,indent=2)
        
        if datasetListDebug:
            print 'user does not exist - no datasets will be listed'
    
        return HttpResponse(data_string + "\n")
        
    #Step 1 - grab the groups that this user belongs to
    #This will involve a call to the ESGF node
    
    if paths.esgfAccess:
        groups_list_str = getGroupsFromESGF(user_id)
        
        if datasetListDebug:
            print 'Groups returned by ESGF: ' + groups_list_str
            
        response_str = groups_list_str
    else:
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
        
    
    print 'response_str: ' + response_str
    
    import json 
    
    response_json = json.loads(response_str)
    
    groups_list = []
    for group in response_json['groups']:
        groups_list.append(group)
    
    print 'groups_list: ' + str(groups_list)
    
    
    #Step 2 - grab all the datasets from all groups in which a user can access 
    datasets_in_groups = []
    
    from exploratory_analysis.models import Dataset_Access
    
    for group_name in groups_list:
        da = Dataset_Access.objects.filter(group_name=group_name)
        if da:
            new_dataset_list_str = da[0].dataset_list
            
            #take intersection of these groups ^^^^
            for dataset_item in new_dataset_list_str.split(','):
                datasets_in_groups.append(dataset_item)
                print 'dataset_item: ' + dataset_item
        
    
    #Step 3 - read all the datasets from the root directory
    #list of datasets
    disk_datasets = []
    
    
    print '\nIn GET functionality\n'    
        
    #grab the group record
    da = Dataset_Access.objects.filter(group_name=group_name)
    
    
    if not da:
        print 'list is empty'
        data = {'dataset_list' : ''}
        data_string = json.dumps(data,sort_keys=False,indent=2)
        return HttpResponse(data_string + "\n")
    
    dataset_list = []
    
    
    for dataset in da[0].dataset_list.split(','):
        dataset_list.append(dataset)
    
    disk_datasets = dataset_list
    print '\nEnd in GET functionality\n'      
    
    print 'datasets on hard drive: ' + str(disk_datasets)
    
    
    
    #Step 4 - take the intersection of steps 1 and 3
    #datasets_set_returned = set(datasets_in_groups).intersection(datasets_in_cades)
    #set(b1).intersection(b2)
    datasets_lists_returned = list(set(datasets_in_groups).intersection(disk_datasets))
    
    #print 'intersection of datasets: ' + str(datasets_lists_returned)
    
    #Step 5 - return result to the app
    data = {'datasets' : datasets_lists_returned } #datasets_in_groups}
    data_string = json.dumps(data,sort_keys=False,indent=2)
    
    print 'data_string: ' + str(data_string)
    
    
    data = {'datasets' : datasets_lists_returned } #datasets_in_groups}
    data_string = json.dumps(data,sort_keys=False,indent=2)
    
    '''
    return data_string



'''
        user = User(username=user_id,
                         password='password is not used, ESGF handles authentication for us')
        user.save()
'''

'''
    import glob
    for f in glob.glob(default_sample_data_dir + '/*'):
      f_arr = f.split('/')
      #print 'f: ' + f_arr[len(f_arr)-1]
      disk_datasets.append(f_arr[len(f_arr)-1])
'''
    

'''
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
'''