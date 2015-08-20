from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login

from metrics.frontend import lmwgmaster
#from metrics.frontend.lmwgmaster import *

import amwg
import lmwg

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

import json
import logging
import traceback
import os

from utils import generate_token_url

logger = logging.getLogger('exploratory_analysis')
logger.setLevel(logging.DEBUG)



fh = logging.FileHandler('exploratory_analysis.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# add handler to logger object
logger.addHandler(fh)

import ConfigParser

print 'This one is looking for ./exploratory_analysis/eaconfig.cfg'
config = ConfigParser.ConfigParser()
config.read('./exploratory_analysis/eaconfig.cfg')



#various variables that need to go into a config file
#esgfAuth - flag for turning on (True) or turning off (False) esgf authentication
#esgfAuth = False
esgfAuth = config.get("options", "esgfAuth")

#the directory for the certs to be fetched
#proxy_cert_dir = '/tmp'
proxy_cert_dir = config.get("certificate", "proxy_cert_dir")


#naAuthReq - authentication via the cookie on (True) or off (False)
#authReq = True
authReq = config.get("options", "authReq")



#certNameSuffix - the suffix of the certificate file
#certNameSuffix = 'x509acme'
certNameSuffix = config.get("certificate","certNameSuffix")

#ea_root = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer'
ea_root = config.get('paths','ea_root')

#uvcdat_live_root = ea_root+ '/django-app-1.8/uvcdat_live/' 
uvcdat_live_root = config.get('paths','uvcdat_live_root')

#img_cache_path = uvcdat_live_root + '/exploratory_analysis/static/exploratory_analysis/cache/'
img_cache_path = config.get('paths','img_cache_path')

#staticfiles_dirs = uvcdat_live_root + "/exploratory_analysis/static/exploratory_analysis"
staticfiles_dirs = config.get('paths','staticfiles_dirs')


#javascript_namespace = 'EA_CLASSIC_VIEWER.functions.'
javascript_namespace = config.get('namespaces','javascript_namespace')


# Main page.
def index(request):
    
    template = loader.get_template('exploratory_analysis/index.html')

    context = RequestContext(request, {
        'username' : '',
    })

    return HttpResponse(template.render(context))


#http://<host>/exploratory_analysis/login
def login(request):
    
    template = loader.get_template('exploratory_analysis/login.html')

    context = RequestContext(request, {
        
    })

    return HttpResponse(template.render(context))




#Example: curl -i -H "Accept: application/json" -X POST -d '{ "username" :  "u1" }'  http://localhost:8081/exploratory_analysis/auth/
#@ensure_csrf_cookie
def auth(request):
    
    print 'in auth request'
    
    
    if request.method == "POST":
        
        json_data = json.loads(request.body)
        
        username = json_data['username']
        password = json_data['password']
        
        #return a None message if the username is blank
        if username == '':
            return HttpResponse("None")
        elif username == None:
            return HttpResponse("None")
        
        #insert code for authentication here
        #create a valid user object
        
        from fcntl import flock, LOCK_EX, LOCK_UN
        print '*****Begin ESGF Login*****'
        import traceback
        cert_name = certNameSuffix
        outdir = os.path.join(proxy_cert_dir, username)
        
        print 'outdir: ' + str(outdir)
        
        try:
                
                if not os.path.exists(outdir):
                    os.makedirs(outdir)
                else:
                    print 'path already exists'
                
                outfile = os.path.join(outdir, cert_name)
                outfile = str(outfile)
                
                # outfile = '/tmp/x509up_u%s' % (os.getuid()) 
                print '----> OUTFILE: ', outfile
                   
                import myproxy_logon
                
                #username = username1
                #password = password1
                peernode = 'esg.ccs.ornl.gov'
           
                myproxy_logon.myproxy_logon(peernode,
                      username,
                      password,
                      outfile,#os.path.join(cert_path,username + '.pem').encode("UTF-8"),
                      lifetime=43200,
                      port=7512
                      )
            
                print '*****End ESGF login*****'
                
        except:
                tb = traceback.format_exc()
                logger.debug('tb: ' + tb)
                print "couldn't make directory " + str(outdir)
                return HttpResponse("Not Authenticated")
        
        return HttpResponse("POST")
    else:
        
        return HttpResponse("Not available")
    
    '''
    if request.method == "POST":
        json_data = json.loads(request.body)
        
        username = json_data['username'] 
        password = json_data['password'] 
        
        
        #return a None message if the username is blank
        if username == '':
            return HttpResponse("None")
        if username == None:
            return HttpResponse("None")
    
        #insert code for authentication here
        #create a valid user object
        
        
        #authenticates to ESGF
        if esgfAuth:
            print 'esgfAuth is true, so authenticate'
    
            from fcntl import flock, LOCK_EX, LOCK_UN
            
            cert_name = certNameSuffix
            
            outdir = os.path.join(proxy_cert_dir, username)
                
            try:
                
                if not os.path.exists(outdir):
                    os.makedirs(outdir)
                else:
                    print 'path already exists'
                
                outfile = os.path.join(outdir, cert_name)
                outfile = str(outfile)
                
                # outfile = '/tmp/x509up_u%s' % (os.getuid()) 
                print '----> OUTFILE: ', outfile
                
                    
                    
                
            except:
                tb = traceback.format_exc()
                logger.debug('tb: ' + tb)
                print "couldn't make directory " + str(outdir)
                return HttpResponse("Not Authenticated")
            
    
        else:
            print 'esgfAuth is false, so dont authenticate'
            return HttpResponse("Authenticated")
           
    '''
    return HttpResponse("Hello")



#Main view
def main(request,user_id):
  
    #check to see if the user is logged in
    loggedIn = isLoggedIn(request,user_id)
    
    template = loader.get_template('exploratory_analysis/index.html')
    
    if(loggedIn == False):
        template = loader.get_template('exploratory_analysis/not_logged_in.html')
    
    context = RequestContext(request, {
        'username' : str(user_id),
        'loggedIn' : str(loggedIn)
    })

    return HttpResponse(template.render(context))



#Belongs in a common utils package
def isLoggedIn(request,user_id):
    
    print 'user: ' + str(request.user) + ' user_id: ' + user_id
    
    if authReq:
        
        
        return True
    
    else:
        if (str(request.user) == str(user_id)):
            loggedIn = True
        else: 
            return False



def classic(request,user_id):


    template = loader.get_template('exploratory_analysis/classic.html')
    
    context = RequestContext(request, {
      'username' : user_id,
    })

    return HttpResponse(template.render(context))




def classic_set_list_html(request):

    print 'in classic_set_list_html'

    package = request.GET.get('package','')
    print 'package: ' + package

    '''
    json_data = json.loads(request.body)
    project = json_data['project']
    dataset = json_data['dataset']
    pckg = json_data['pckg']
    variables = json_data['variables']
    times = json_data['times']
    '''
    
    if package == 'atm':
        print 'getting atm home'
        template = loader.get_template('exploratory_analysis/atm_home.html')
        context = RequestContext(request, {
            
        })
        return HttpResponse(template.render(context))
    else:
        print 'getting lnd home'
        template = loader.get_template('exploratory_analysis/land_home.html')
        context = RequestContext(request, {
            
        })
        return HttpResponse(template.render(context))
    
    #return HttpResponse(html);


def classic_views_html(request):
    """
    Generate new clasic view html
    The view shown depends on the package
    """    
    sets = str(request.GET.get('set',''))
    
    #sets = str(set[3:])
    varlist = 'TLAI'
    times = 't1'
    dataset = 'd1'
    options = []
    package = ''
    
    html = ''
    
    try:
        if package == 'lnd':
            html = lmwg.pageGenerator(sets, varlist, times, package, dataset, options)
        else:
            html = amwg.pageGenerator(sets, varlist, times, package, dataset, options)
    
    except:
        tb = traceback.format_exc()
        print 'tb: ' + tb
        return HttpResponse("error")
        
    print 'returning html: ' + str(html)
    
    return HttpResponse(html)
















#Moved the services to its own app 8-2-15
'''
#GET
#curl -X GET http://localhost:8081/exploratory_analysis/published/<dataset_name>/
#POST
#curl -i -H "Accept: application/json" -X POST -d '{ "published" :  "true" }'  http://localhost:8081/exploratory_analysis/published/<dataset_name>/
#PUT
#curl -i -H "Accept: application/json" -X PUT -d '{ "published" :  "true" }'  http://localhost:8081/exploratory_analysis/published/<dataset_name>/

class PublishedView(View):
    
    def put(self, request, dataset_name):
        
        try:
            #load the json object
            json_data = json.loads(request.body)
                
            #grab the dataset added
            published = json_data['published'] #should be a string
        
            from exploratory_analysis.models import Published
            
            #grab the group record
            da = Published.objects.filter(dataset_name=dataset_name)
            
            #for put, remove ALL datasets from the list and substitute the new one given
            published_values = published
                
            if da:
                da.delete()
            
            published_record = Published(
                                                      dataset_name=dataset_name,
                                                      published=published_values
                                                      )
            
            
            logger.debug('\nPublished record: ' + str(published_record))
            
            #save to the database
            published_record.save()
            
            
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
        
        
        return HttpResponse("Published Put")
    
    def post(self, request, dataset_name):
        
        try:
            #load the json object
            json_data = json.loads(request.body)
                
            #grab the dataset added
            published = json_data['published'] #should be a string
        
            from exploratory_analysis.models import Published
            
            #grab the group record
            da = Published.objects.filter(dataset_name=dataset_name)
            
            #for post, remove ALL datasets from the list and substitute the new one given
            published_values = published
                
            if da:
                da.delete()
            
            published_record = Published(
                                                      dataset_name=dataset_name,
                                                      published=published_values
                                                      )
            
            logger.debug('\nPublished record: ' + str(published_record))
            
            #save to the database
            published_record.save()
            
            
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
        
        return HttpResponse("Published Post")
    
    
    def get(self, request, dataset_name):
        
        
        #print '\nIn GET\n'  
        logger.debug('\nIn Published GET\n')
        
        from exploratory_analysis.models import Published
    
        try:
            
            logger.debug('dataset_name: ' + dataset_name)
            
            #grab the group record
            da = Published.objects.filter(dataset_name=dataset_name)
            
            #if the dataset list is empty then return empty list
            if not da:
                data = {'published' : ''}
                data_string = json.dumps(data,sort_keys=False,indent=2)
                return HttpResponse(data_string + "\n")
            
            #otherwise grab the contents and return as a list
            #note: da[0] is the only record in the filtering of the Dataset_Access objects
            published = []
            
            for publish in da[0].published.split(','):
                published.append(publish)
            
            
            data = {'published' : published}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            
                
            return HttpResponse(data_string + "\n")
            #return HttpResponse("response")
        
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
        
        return HttpResponse("Variables Get")





#GET
#curl -X GET http://localhost:8081/exploratory_analysis/variables/<dataset_name>/
#POST
#curl -i -H "Accept: application/json" -X POST -d '{ "variables" :  "a,b,c" }'  http://localhost:8081/exploratory_analysis/variables/<dataset_name>/
#PUT
#curl -i -H "Accept: application/json" -X PUT -d '{ "variables" :  "a,b,c" }'  http://localhost:8081/exploratory_analysis/variables/<dataset_name>/
#NOTE: PUT functionality is buggy and shouldn't be used for now
class VariablesView(View):
    
    def put(self, request, dataset_name):
        
        
        #print '\nIn GET\n'  
        logger.debug('\nIn Variables PUT\n')
        
        #load the json object
        json_data = json.loads(request.body)
            
        
        #grab the dataset added
        variables = json_data['variables'] #should be a string
    
        from exploratory_analysis.models import Dataset_Access
        
        #grab the group record
        da = Dataset_Access.objects.filter(group_name=group_name)
        
        #for put, APPEND the new dataset given
        #append dataset to the end of the dataset list
        
        new_variables_list = ''
        if da:
            new_variables = da[0].variables
            
            new_variables_list = new_variables.split(',')
            
            isDuplicate = False
            
            #check for duplicates
            for entry in new_variables_list:
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
        
        
        
        
        return HttpResponse("Variables Put")
    def post(self, request, dataset_name):
        
        #load the json object
        json_data = json.loads(request.body)
            
        
        #grab the dataset added
        variables = json_data['variables'] #should be a string
    
        #print 'Group_name: ' + group_name
        #print 'dataset: ' + str(dataset)
        
        from exploratory_analysis.models import Variables
        
        #grab the group record
        da = Variables.objects.filter(dataset_name=dataset_name)
        
        
        #for post, remove ALL datasets from the list and substitute the new one given
        new_variables = variables
            
        if da:
            da.delete()
        
        variables_record = Variables(
                                                  dataset_name=dataset_name,
                                                  variables=new_variables
                                                  )
        
        
        
        
        logger.debug('\nVariables record: ' + str(variables_record))
        
        #save to the database
        variables_record.save()
        
        all = Variables.objects.all()
        
        return HttpResponse("POST Done\n")   
    
    
    def get(self, request, dataset_name):
        
        #print '\nIn GET\n'  
        logger.debug('\nIn Variables GET\n')
        
        from exploratory_analysis.models import Variables
    
        
        try:
            
            logger.debug('dataset_name: ' + dataset_name)
            
            #grab the group record
            da = Variables.objects.filter(dataset_name=dataset_name)
            
            #if the dataset list is empty then return empty list
            if not da:
                data = {'variables' : ''}
                data_string = json.dumps(data,sort_keys=False,indent=2)
                return HttpResponse(data_string + "\n")
            
            #otherwise grab the contents and return as a list
            #note: da[0] is the only record in the filtering of the Dataset_Access objects
            variables = []
            
            for variable in da[0].variables.split(','):
                variables.append(variable)
            
            
            data = {'variables' : variables}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            
                
            return HttpResponse(data_string + "\n")
            #return HttpResponse("response")
        
        except:
            tb = traceback.format_exc()
            logger.debug('tb: ' + tb)
            return HttpResponse("error")
        
        return HttpResponse("Variables Get")



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

    
