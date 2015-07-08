from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import View

import json

import logging

import traceback

logger = logging.getLogger('exploratory_analysis')
logger.setLevel(logging.DEBUG)



fh = logging.FileHandler('exploratory_analysis.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)


# Create your views here.
def index(request):
    return HttpResponse("Hello ea user.")




























#gets packages information
#Service API for the Dataset_Access table
#GET
#http://<host>:<port>/exploratory_analysis/group_dataset/<group_name>
#POST
#echo '{ "dataset" :  <dataset_name> }' | curl -d @- 'http://<host>:<port>/exploratory_analysis/dataset_packages/(?P<dataset_name>\w+)/$' -H "Accept:application/json" -H "Context-Type:application/json"
#DELETE
#http://<host>:<port>/exploratory_analysis/dataset_packages/<dataset_name>/

class Dataset_AccessView(View):
    
    
    def put(self, request, group_name):
    
        #print '\nIn GET\n'  
        logger.debug('\nIn Dataset_Access PUT\n')
        
        #load the json object
        json_data = json.loads(request.body)
            
        
        #grab the dataset added
        dataset = json_data['dataset'] #should be a string
    
        from exploratory_analysis.models import Dataset_Access
        
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        #for put, APPEND the new dataset given
        #append dataset to the end of the dataset list
        
        new_dataset_list = ''
        if da:
            new_dataset_list = da[0].dataset_list
            
            new_dataset_list_list = new_dataset_list.split(',')
            
            isDuplicate = False
            
            #check for duplicates
            for entry in new_dataset_list_list:
                logger.debug('entry: ' + entry + ' dataset: ' + dataset)
                if entry == dataset:
                    logger.debug('match')
                    isDuplicate = True
            if not isDuplicate:
                new_dataset_list = new_dataset_list + ',' + dataset
                logger.debug('\nNew Dataset List: ' + str(new_dataset_list))
                da.delete()
        else:
            new_dataset_list = dataset
        
        
        #logger.debug('new_dataset_list: ' + str(new_dataset_list))
        
        dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
        
          
        #save to the database
        dataset_access_record.save()
        
        all = Dataset_Access.objects.all()
        
        #logger.debug('all: ' + str(all))
        
    
        return HttpResponse("PUT Done\n")   
    
    def post(self, request, group_name):
        
        #load the json object
        json_data = json.loads(request.body)
            
        
        #grab the dataset added
        dataset = json_data['dataset'] #should be a string
    
        #print 'Group_name: ' + group_name
        #print 'dataset: ' + str(dataset)
        
        from exploratory_analysis.models import Dataset_Access
        
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        
        #for post, remove ALL datasets from the list and substitute the new one given
        new_dataset_list = dataset
            
        if da:
            da.delete()
        
        dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
        
        
        
        
        #save to the database
        dataset_access_record.save()
        
        all = Dataset_Access.objects.all()
        
    
        return HttpResponse("POST Done\n")   
        
    
    
    def get(self, request, group_name):
        
        
        #print '\nIn GET\n'  
        logger.debug('\nIn Dataset_Access GET\n')
        
        from exploratory_analysis.models import Dataset_Access
    
        
        try:
            
            #grab the group record
            da = Dataset_Access.objects.filter(group_name=group_name)
            
            #if the dataset list is empty then return empty list
            if not da:
                data = {'dataset_list' : ''}
                data_string = json.dumps(data,sort_keys=False,indent=2)
                return HttpResponse(data_string + "\n")
            
            #otherwise grab the contents and return as a list
            #note: da[0] is the only record in the filtering of the Dataset_Access objects
            dataset_list = []
            
            for dataset in da[0].dataset_list.split(','):
                dataset_list.append(dataset)
                
            data = {'dataset_list' : dataset_list}
            data_string = json.dumps(data,sort_keys=False,indent=2)
    
            return HttpResponse(data_string + "\n")
            
            return HttpResponse("response")
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
        
        return HttpResponse("respone")






#gets packages information
#Service API for the Dataset_Access table
#GET
#http://<host>:<port>/exploratory_analysis/dataset_packages/<dataset_name>
#POST
#echo '{ "dataset" :  <dataset_name> }' | curl -d @- 'http://<host>:<port>/exploratory_analysis/dataset_packages/(?P<dataset_name>\w+)/$' -H "Accept:application/json" -H "Context-Type:application/json"
#DELETE
#http://<host>:<port>/exploratory_analysis/group_dataset/<group_name>
class PackagesView(View):
    
    #dbname = acme_services_config.get("db_options","dbname")
    #dbuser = acme_services_config.get("db_options","dbuser")
    #dbpassword = acme_services_config.get("db_options","dbpassword")
    #isConnectedToDB = acme_services_config.get("db_options","isConnectedToDB")
    
    
    def get(self, request, dataset_name):
        
        from exploratory_analysis.models import Packages
    
        #print '\nIn GET\n'  
        logger.debug('\nIn GET\n')
        
        #grab the record with the given dataset_name
        da = Packages.objects.filter(dataset_name=dataset_name)
        
        if not da:
            data = {'packages' : ''}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            return HttpResponse(data_string + "\n")
       
        #otherwise grab the contents and return as a list
        #note: da[0] is the only record in the filtering of the Dataset_Access objects
        dataset_list = []
        
        for dataset in da[0].packages.split(','):
            dataset_list.append(dataset)
            
        data = {'packages' : dataset_list}
        data_string = json.dumps(data,sort_keys=False)#,indent=2)

        
        logger.debug("End GET\n")
        return HttpResponse(data_string)# + "\

    
    def post(self, request, dataset_name):
        
        from exploratory_analysis.models import Packages
        
        
        
        logger.debug('\nIn POST\n')
        
        #load the json object
        json_data = json.loads(request.body)
            
        #grab the dataset added
        packages = json_data['packages'] #should be a string
        
        logger.debug('\nrequest.body' + str(request.body) + '\n')
        logger.debug('\ndataset name: ' + str(dataset_name) + '\n')
        
        #grab the record with the given dataset_name
        try:
            da = Packages.objects.filter(dataset_name=dataset_name)
            
            new_dataset_list = ''
            if da:
                #delete the record and rewrite the record with the new dataset list
                da.delete()
            
            
            all = Packages.objects.all()
            
            dataset_packages_record = Packages(
                                                  dataset_name=dataset_name,
                                                  packages=packages
                                                  )
            
            #save to the database
            dataset_packages_record.save()
            
            all = Packages.objects.all()
            
            
            logger.debug('\nEnd POST\n')
            return HttpResponse("Success\n")

        except:
            
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
     
        
    def delete(self, request, dataset_name):
       
        from exploratory_analysis.models import Packages
        
        logger.debug('\nIn DELETE\n')   
        
        #not sure if this is the right behavior but this will delete the ENTIRE record given the group
        #grab the group record
        da = Packages.objects.filter(dataset_name=dataset_name)
        
        if da:
            da.delete()
        
        all = Packages.objects.all()
        
        logger.debug('\nEnd DELETE\n')   
        return HttpResponse("Success\n")
    











''' 
Commented out 6-4-15
#Service API for the Dataset_Access table
#GET
#http://<host>:<port>/exploratory_analysis/dataset_packages/<dataset_name>
#POST
#echo '{ "dataset" :  <dataset_name> }' | curl -d @- 'http://<host>:<port>/exploratory_analysis/dataset_packages/(?P<dataset_name>\w+)/$' -H "Accept:application/json" -H "Context-Type:application/json"
#DELETE
#http://<host>:<port>/exploratory_analysis/dataset_packages/<dataset_name>/
def dataset_packages(request,dataset_name):
    
    from exploratory_analysis.models import Packages
        
    if request.method == 'POST':
        
        logger.debug('\nIn POST\n')
        
        #load the json object
        json_data = json.loads(request.body)
            
        #grab the dataset added
        packages = json_data['packages'] #should be a string
        
        #grab the record with the given dataset_name
        da = Packages.objects.filter(dataset_name=dataset_name)
        
        new_dataset_list = ''
        if da:
            #delete the record and rewrite the record with the new dataset list
            da.delete()
        
        
        all = Packages.objects.all()
        
        dataset_packages_record = Packages(
                                                  dataset_name=dataset_name,
                                                  packages=packages
                                                  )
            
        #save to the database
        dataset_packages_record.save()
        
        all = Packages.objects.all()
        
        
        logger.debug('\nEnd POST\n')
        return HttpResponse("Success\n")

    elif request.method == 'GET':
        
        #print '\nIn GET\n'  
        logger.debug('\nIn GET\n')
        
        #grab the record with the given dataset_name
        da = Packages.objects.filter(dataset_name=dataset_name)
        
        if not da:
            data = {'packages' : ''}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            return HttpResponse(data_string + "\n")
       
        #otherwise grab the contents and return as a list
        #note: da[0] is the only record in the filtering of the Dataset_Access objects
        dataset_list = []
        
        for dataset in da[0].packages.split(','):
            dataset_list.append(dataset)
            
        data = {'packages' : dataset_list}
        data_string = json.dumps(data,sort_keys=False)#,indent=2)

        
        logger.debug("End GET\n")
        return HttpResponse(data_string)# + "\n")
        
    
    elif request.method == 'DELETE':
        
        
        logger.debug('\nIn DELETE\n')   
        
       #not sure if this is the right behavior but this will delete the ENTIRE record given the group
        #grab the group record
        da = Packages.objects.filter(dataset_name=dataset_name)
        
        if da:
            da.delete()
        
        all = Packages.objects.all()
        
        logger.debug('\nEnd DELETE\n')   
        return HttpResponse("Success\n")

    else:
        return HttpResponse("Error\n")











#Service API for the Dataset_Access table
#GET
#http://<host>:<port>/exploratory_analysis/group_dataset/<group>
#POST
#echo '{ "dataset" :  <dataset_name> }' | curl -d @- 'http://<host>:<port>/exploratory_analysis/dataset_variables/ne30/' -H "Accept:application/json" -H "Context-Type:application/json"
#DELETE
#http://<host>:<port>/exploratory_analysis/group_dataset/<group>/
def dataset_variables(request,dataset_name):
    
    from exploratory_analysis.models import Variables
        
    if request.method == 'POST':
        
        logger.debug('\nIn POST\n')
        
        #load the json object
        json_data = json.loads(request.body)
            
        #grab the dataset added
        variables = json_data['variables'] #should be a string
        
        
        #grab the record with the given dataset_name
        da = Variables.objects.filter(dataset_name=dataset_name)
        
        
        new_dataset_list = ''
        
        #if there is an existing record
        #delete the record and rewrite the record with the new dataset list
        #SHOULD BE CHANGED TO AN ARRAY
        if da:
            da.delete()
        
        all = Variables.objects.all()
        
        dataset_variables_record = Variables(
                                                  dataset_name=dataset_name,
                                                  variables=variables
                                                  )
        #save to the database
        dataset_variables_record.save()
        
        all = Variables.objects.all()
        
        
        logger.debug('\nEnd POST\n')
        return HttpResponse("Success\n")

    elif request.method == 'GET':
        
        #print '\nIn GET\n'  
        logger.debug('\nIn GET\n')
        
        #grab the record with the given dataset_name
        da = Variables.objects.filter(dataset_name=dataset_name)
        
        #if the record doesn't exist, then return and empty variables string
        if not da:
            data = {'variables' : ''}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            return HttpResponse(data_string + "\n")
       
        #otherwise grab the contents and return as a list
        #note: da[0] is the only record in the filtering of the Dataset_Access objects
        dataset_list = []
        
        for dataset in da[0].variables.split(','):
            dataset_list.append(dataset)
            
        data = {'variables' : dataset_list}
        data_string = json.dumps(data,sort_keys=False)#,indent=2)

        
        logger.debug("End GET\n")
        return HttpResponse(data_string)# + "\n")
        
    
    elif request.method == 'DELETE':
        
        
        logger.debug('\nIn DELETE\n')   
        
        #not sure if this is the right behavior but this will delete the ENTIRE record given the group
        #grab the group record
        da = Variables.objects.filter(dataset_name=dataset_name)
        
        if da:
            da.delete()
        
        all = Variables.objects.all()
        
        logger.debug('\nEnd DELETE\n')   
        return HttpResponse("Success\n")

    else:
        return HttpResponse("Error\n")
'''
    
    

'''
#Models table has the form
#group_name  |   dataset_list
#where dataset_list is a comma separated text blob
def group_dataset(request,group_name):
    
    from exploratory_analysis.models import Dataset_Access
        
    if request.method == 'POST':
    
        print '\nPOSTING new Dataset\n'    
    
        #load the json object
        json_data = json.loads(request.body)
            
        #grab the dataset added
        dataset = json_data['dataset'] #should be a string
    
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        #append dataset to the end of the dataset list
        
        new_dataset_list = ''
        if da:
            new_dataset_list = da[0].dataset_list
            new_dataset_list = new_dataset_list + ',' + dataset
        else:
            new_dataset_list = dataset
        
        
        #update the record
        #delete the record and rewrite the record with the new dataset list
        da.delete()
        
        
        all = Dataset_Access.objects.all()
        
        
        dataset_access_record = Dataset_Access(
                                                  group_name=group_name,
                                                  dataset_list=new_dataset_list
                                                  )
            
        #save to the database
        dataset_access_record.save()
        
        all = Dataset_Access.objects.all()
        
        print '\nEND POSTING new Dataset\n'    
    
        return HttpResponse("POST Done\n")
    
    elif request.method == 'GET':

        print '\nIn GET\n'    
        
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        #if the dataset list is empty then return empty list
        if not da:
            data = {'dataset_list' : ''}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            return HttpResponse(data_string + "\n")
        
        #otherwise grab the contents and return as a list
        #note: da[0] is the only record in the filtering of the Dataset_Access objects
        dataset_list = []
        
        for dataset in da[0].dataset_list.split(','):
            dataset_list.append(dataset)
            
        data = {'dataset_list' : dataset_list}
        data_string = json.dumps(data,sort_keys=False,indent=2)

        return HttpResponse(data_string + "\n")
    
    elif request.method == 'DELETE':

        print '\nIn DELETE\n'    
        
        #not sure if this is the right behavior but this will delete the ENTIRE record given the group
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        da.delete()
        
        all = Dataset_Access.objects.all()
        
        return HttpResponse("DELETE Done\n")

    return HttpResponse('DeleteError')    
'''


