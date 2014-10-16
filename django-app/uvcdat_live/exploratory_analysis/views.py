from django.views.decorators.csrf import ensure_csrf_cookie
#flag for toggling connection to the diags backend
isConnected = True

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.template import RequestContext, loader
#from exploratory_analysis.models import Diags
import json
import sys 

from paths import paths

from defaults import parameter_defaults

from treeviewer import treeviewer_treeex


syspath_append_uvcmetrics = paths.syspath_append_uvcmetrics
syspath_append_cdscan = paths.syspath_append_cdscan

paths_cache_dir = paths.cache_dir
#paths_front_end_cache_dir = paths.front_end_cache_dir

default_sample_data_dir = paths.default_sample_data_dir
default_tree_sample_data_dir = paths.default_tree_sample_data_dir
default_map_sample_data_dir = paths.default_map_sample_data_dir

img_cache_path = paths.img_cache_path

timeseries_cache_path = paths.timeseries_cache_path

generated_img_path = paths.generated_img_path

# import the diags code
if isConnected:
    #sys.path.append(syspath_append_uvcmetrics)
    #sys.path.append(syspath_append_cdscan)
   
    
    from metrics.frontend.options import Options
    from metrics.computation.reductions import *
    from metrics.fileio.filetable import *
    from metrics.fileio.findfiles import *
    from metrics.packages.diagnostic_groups import *

    from metrics.exploratory.treeview import TreeView 
    from metrics import *

    from metrics.packages.diagnostic_groups import *
    from metrics.frontend.options import *
    import metrics.frontend.defines as defines

cache_dir = paths_cache_dir
#front_end_cache_dir = paths_front_end_cache_dir#'../../../static/cache/'


#use these objects temporarily
print '\nsetting up figures store\n'
figures_store = {}

    
from django.http import HttpResponseRedirect


def core_parameters(request):
    
    data = {}
    
    data['host'] = paths.ea_hostname
    
    data_string = json.dumps(data,sort_keys=False,indent=2)
    
    return HttpResponse(data_string)

#Service API for the Dataset_Access table
#GET
#http://<host>:<port>/exploratory_analysis/group_dataset/<group>
#POST
#echo '{ "dataset" :  <dataset_name> }' | curl -d @- 'http://<host>:<port>/exploratory_analysis/group_dataset/<group>/' -H "Accept:application/json" -H "Context-Type:application/json"
#DELETE
#http://<host>:<port>/exploratory_analysis/group_dataset/<group>/
def dataset_variables(request,dataset_name):
    
    from exploratory_analysis.models import Variables
        
    if request.method == 'POST':
        
        print '\nIn POST\n'  
        
        #load the json object
        json_data = json.loads(request.body)
            
        #grab the dataset added
        variables = json_data['variables'] #should be a string
        
        #grab the record with the given dataset_name
        da = Variables.objects.filter(dataset_name=dataset_name)
        
        new_dataset_list = ''
        if da:
            #delete the record and rewrite the record with the new dataset list
            da.delete()
        
        
        all = Variables.objects.all()
        
        dataset_variables_record = Variables(
                                                  dataset_name=dataset_name,
                                                  variables=variables
                                                  )
            
        #save to the database
        dataset_variables_record.save()
        
        all = Variables.objects.all()
        
        
        return HttpResponse("POST Done\n")

    elif request.method == 'GET':
        
        print '\nIn GET\n'  
        
        #grab the record with the given dataset_name
        da = Variables.objects.filter(dataset_name=dataset_name)
        
        if not da:
            data = {'variables' : ''}
            data_string = json.dumps(data,sort_keys=False,indent=2)
            return HttpResponse(data_string + "\n")
       
        #otherwise grab the contents and return as a list
        #note: da[0] is the only record in the filtering of the Dataset_Access objects
        dataset_list = []
        
        for dataset in da[0].variables.split(','):
            dataset_list.append(dataset)
            
        data = {'dataset_list' : dataset_list}
        data_string = json.dumps(data,sort_keys=False,indent=2)

        print("GET Done\n")
        return HttpResponse(data_string + "\n")
        
    
    elif request.method == 'DELETE':
        
        print '\nIn DELETE\n'    
        
        #not sure if this is the right behavior but this will delete the ENTIRE record given the group
        #grab the group record
        da = Variables.objects.filter(dataset_name=dataset_name)
        
        if da:
            da.delete()
        
        all = Variables.objects.all()
        
        return HttpResponse("DELETE Done\n")

    else:
        return HttpResponse("Error\n")




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



  ############
  #Page views#
  ############

#Home page view...nothing fancy here just points to the view located at index.html
#corresponds with url: http://<host>/exploratory_analysis
def index(request):
    
    print request.GET.get('q')
    
    template = loader.get_template('exploratory_analysis/index.html')

    context = RequestContext(request, {
        'username' : 'jfharney',
    })

    return HttpResponse(template.render(context))




#Home page view...nothing fancy here just points to the view located at index.html
#corresponds with url: http://<host>/exploratory_analysis
def main(request,user_id):
    
    
  
    
    loggedIn = isLoggedIn(request,user_id)
    
    template = loader.get_template('exploratory_analysis/index.html')
    if(loggedIn == False):
        template = loader.get_template('exploratory_analysis/not_logged_in.html')
    
    
    
    
    context = RequestContext(request, {
        'username' : str(user_id),
        'loggedIn' : str(loggedIn)
    })

    return HttpResponse(template.render(context))


def isLoggedIn(request,user_id):
    print '\n\n\t\tuser_id: ' + str(user_id)
    print 'user: ' + str(request.user)
    
    print 'main: noAuthReq: ', paths.noAuthReq
    loggedIn = paths.noAuthReq
    
    if (str(request.user) == str(user_id)):
        loggedIn = True
        
    return loggedIn


#geo map/time series view
#corresponds with url: http://<host>/exploratory_analysis/maps
def maps(request,user_id):
    print '\n\nrequest user authenticate: ' + str(request.user.is_authenticated()) + '\n\n\n\n'
    
    
    #need a flag to indicated whether a tree 
    print '\n\n\t\tuser_id: ' + str(user_id)
    print 'user: ' + str(request.user)
    
    loggedIn = paths.noAuthReq
    
    if (str(request.user) == str(user_id)):
        loggedIn = True
    
    username = 'jfharney'
    
    #grab the username
    if user_id != None:
        username = user_id
    
    if(loggedIn == True):
        template = loader.get_template('exploratory_analysis/mapview.html')
    else:
        print 'username: ' + username
        template = loader.get_template('exploratory_analysis/not_logged_in.html')
        
    
    
    context = RequestContext(request, {
      'loggedIn' : str(loggedIn),
      'username' : username,
    })
    
    return HttpResponse(template.render(context))


#geo map/time series view
#corresponds with url: http://<host>/exploratory_analysis/maps
def heatmap(request,user_id):
    #print '\n\n\n\n\nrequest user authenticate: ' + str(request.user.is_authenticated()) + '\n\n\n\n'
    
    
    #need a flag to indicated whether a tree 
    #print '\n\n\n\n\n\n\n\t\t\tuser_id: ' + str(user_id)
    #print 'user: ' + str(request.user)
    
    loggedIn = paths.noAuthReq
    
    if (str(request.user) == str(user_id)):
        loggedIn = True
    
    username = 'jfharney'
    
    #grab the username
    if user_id != None:
        username = user_id
    
    print 'LoggedIn: ' + str(loggedIn)
    
    if(loggedIn == True):
        template = loader.get_template('exploratory_analysis/heatmapview.html')
    else:
        print 'username: ' + username
        template = loader.get_template('exploratory_analysis/not_logged_in.html')
        
    context = RequestContext(request, {
      'loggedIn' : str(loggedIn),
      'username' : username,
    })
    
    return HttpResponse(template.render(context))





def figureGenerator(request):
      print 'in figure generator'
    
      print request.POST
      #hard coded\
      
      dataset = str(request.POST['dataset']);
      
      print 'dataset ---> ' + dataset
      variables = request.POST['variables']
      print 'variables passed in: ', variables
      print type(variables)
      if type(variables) is list:
         variables = [str(x) for x in variables]
      else:
         variables = [str(variables)]

      times = request.POST['times']
      if type(times) is list:
         times = [str(x) for x in times]
      else:
         times = [str(times)]

      sets = request.POST['sets']
      if type(sets) is list:
         sets = [str(x) for x in sets]
      else:
         sets = [str(sets)]

      packages = request.POST['packages']
      if type(packages) is list:
         packages = [str(x) for x in packages]
      else:
         packages = [str(packages)]

      realms = request.POST['realms']
      if type(realms) is list:
         realms = [str(x) for x in realms]
      else:
         realms = [str(realms)]
        
      print 'sets: ', sets
#      sets = ['1']
    
      '''
      print 'variables: ' + str(variables)
      print 'times: ' + str(times)
      print 'sets: ' + str(sets)
      print 'packages: ' + str(packages)
      print 'realms: ' + str(realms)
      '''
    
      inCache = False
      

      # First, see if it is in cache_dir (the shared cache; typically pregenerated figures
      filename = str(packages[0] + '_set' + sets[0][0] + '_' + times[0] + '_' + variables[0] + '.png')
      filepath = os.path.join(cache_dir, dataset, filename)
      print 'Looking for cached image in system cache', filepath
#      path = './' +  'exploratory_analysis/static/exploratory_analysis/img/treeex/' + cachedFile
#      print 'absolute path: ' + os.path.abspath(path)
      if os.path.exists(filepath):
         print 'Found in system cache'
         inCache = True

      if not inCache:
      # Now, see if it was previously generated by this user.
         filepath = os.path.join(generated_img_path, dataset, filename)
         print 'Looking for cached image in user cache', filepath
         if os.path.exists(filepath):
            print 'Found in user cache'
            inCache=True
    
      if(not inCache):
          print 'not in cache'
          o= Options()
          
          ''' Old defaults
          o._opts['path']=[default_sample_data_dir]
          o._opts['vars']=['TG']
          o._opts['times']=['MAM']
          #Note: only use 1 or 2 
          o._opts['sets']=['1']
          o._opts['packages']=['lmwg']
          o._opts['realms']=['land']
          '''
        
          o._opts['path']=[default_tree_sample_data_dir + paths.dataset_name ]
          o._opts['vars']=variables
          o._opts['times']=times
          #Note: only use 1 or 2 
          o._opts['sets']=sets
          o._opts['packages']=packages
          o._opts['realms']=realms
          dm = diagnostics_menu()
        
	  #filepath is currently set to generated_img_path plus the filename

          import metrics.fileio.filetable as ft
          import metrics.fileio.findfiles as fi
          dtree1 = fi.dirtree_datafiles(o, pathid=0)
          filetable1 = ft.basic_filetable(dtree1, o)
          filetable2 = None
          #print 'No second dataset for comparison'
             
          package=o._opts['packages'][0]
          print 'PACKAGE ' , package
          
          pclass = dm[package.upper()]()
    
          # this needs a filetable probably, or we just define the maximum list of variables somewhere
#          im = ".".join(['metrics', 'packages', package[0], package[0]])
#          if package[0] == 'lmwg':
#             pclass = getattr(__import__(im, fromlist=['LMWG']), 'LMWG')()
#          elif package[0]=='amwg':
#             pclass = getattr(__import__(im, fromlist=['AMWG']), 'AMWG')()
    
          setname = o._opts['sets'][0]
          varid = o._opts['vars'][0]
          seasonid = o._opts['times'][0]
          print 'CALLING LIST SETS'
          slist = pclass.list_diagnostic_sets()
          print 'DONE CALLIGN LIST SETS'
          keys = slist.keys()
          keys.sort()
          import vcs
	  print 'generating ', filepath
          v = vcs.init()
#          diag_template = diagnostics_template()
          for k in keys:
             fields = k.split()
             if setname[0] == fields[0]:
                print 'calling init for ', k, 'varid: ', varid, 'seasonid: ', seasonid
                plot = slist[k](filetable1, filetable2, varid, seasonid)
                res = plot.compute()
                print type(res)
                v.clear()
                v.plot(res[0].vars, res[0].presentation, bg=1)
#### BES - Merge issues. Not sure what to do here. Need to think about it.
#                filename = filename+'_'+varid+'.png'
#                fname = os.path.join(filepath, dataset, filename)
##                fname = filepath+filename+'_'+varid+'.png'
#                print 'fname: ', fname
                
#                v.png(fname)
# was this:
                v.png(filepath)
          
    
    
      #return HttpResponse()
#      return HttpResponse(cachedFile)
      return HttpResponse(filepath)


#Test classic view
@ensure_csrf_cookie
def classic(request,user_id):
      #print '\n\n\n\n\nrequest user authenticate: ' + str(request.user.is_authenticated()) + '\n\n\n\n'
    
    
    username = 'jfharney'
    
    #grab the username
    if user_id != None:
        username = user_id
        
    loggedIn = isLoggedIn(request,user_id)
    
    template = loader.get_template('exploratory_analysis/classic.html')
    if(loggedIn == False):
        template = loader.get_template('exploratory_analysis/not_logged_in.html')
    
    
    context = RequestContext(request, {
      'loggedIn' : str(loggedIn),
      'username' : username,
    })
    
    return HttpResponse(template.render(context))



#New tree view
@ensure_csrf_cookie
def treeex(request,user_id):
    
    print '\n\t--->request user authenticate: ' + str(request.user.is_authenticated()) + '\n'
    
    
    #need a flag to indicated whether a tree 
    #print '\n\n\t\tuser_id: ' + str(user_id)
    #print 'user: ' + str(request.user)
    
    loggedIn = paths.noAuthReq
    
    if (str(request.user) == str(user_id)):
        loggedIn = True
    
    username = 'jfharney'
    
    #grab the username
    if user_id != None:
        username = user_id
    
    loggedIn = True
    
    loggedIn = paths.noAuthReq
    
    '''
    #get the predefined tree bookmarks of the user
    from exploratory_analysis.models import Tree_Bookmarks
    bookmark_list_obj = Tree_Bookmarks.objects.filter(tree_bookmark_username=username)
  
    bookmark_list = [] 
    for obj in bookmark_list_obj:
        bookmark_list.append(obj.tree_bookmark_name)
 
 

    #get the figure bookmarks of the user
    from exploratory_analysis.models import Figure_Bookmarks
    figure_bookmark_list_obj = Figure_Bookmarks.objects.filter(figure_bookmark_username=username)
 
    figure_bookmark_list = [] 
    for obj in figure_bookmark_list_obj:
        figure_bookmark_list.append(obj.figure_bookmark_name)
 
 
    ##print 'bookmark list: ' + str(bookmark_list)
    #print 'figure bookmark list ' + str(figure_bookmark_list)
 
 
    defaults = parameter_defaults.get_parameter_defaults()
    package_list = defaults['package_list']
    dataset_list = defaults['dataset_list']
    variable_list = defaults['variable_list']
    season_list = defaults['season_list']
    set_list = defaults['set_list']
    '''
 
    
    #first we check if the request is in the cache or if it is the initial call
    #if it is in the cache, no need to do any back end generation
    bookmark = request.GET.get('bookmark')
    
    #print '\nbookmark: ' + str(bookmark)  
    
    
    from bookmarks import t_bookmarks
    #import bookmarks

    #no bookmark is being loaded
    if bookmark == None:
        #print '\n\n\n\nbookmark is none\n\n\n\n'
        
        response = t_bookmarks.noBookmarkHandler(request,user_id)
        
        return response
        
    
    #otherwise there are bookmarks
    else:
        
        #print '\n\n\n\nbookmark is something\n\n\n\n'
        
        
        response = t_bookmarks.bookmarkHandler(request,user_id)
        
        return response
        
        
  ############
  #End Page views#
  ############





  ############
  #Services#
  ############
  
  #####Used in the geo page#####

  #grabs datasets given a user id (used in an ajax call)
  #http://<host>/exploratory_analysis/datasets/<user_id>/

def datasets(request,user_id):
    
    print '\n\n\nIn datasets'
    
    from menuhelper import datasets
  
    data_string = datasets.datasetListHelper(request,user_id)
    
    return HttpResponse(data_string)


def datasets1(request,user_id):
    
    print request.META['REMOTE_ADDR']
    
    print '\n\nIn datasets for user_id: ' + user_id
    
    from menuhelper import datasets
    
    data_string = datasets.datasetListHelper1(request,user_id)
    
    print '\nEnd in datasets for user_id: ' + user_id
    
    return HttpResponse(data_string)

def generate_token_url(filename):
    #!/usr/bin/env python
    import os, time, hashlib
    
    secret = "secret string"                                # Same as AuthTokenSecret
    protectedPath = "/acme-data/"                           # Same as AuthTokenPrefix
    ipLimitation = False                                    # Same as AuthTokenLimitByIp
    hexTime = "{0:x}".format(int(time.time()))              # Time in Hexadecimal      
    fileName = filename                       # The file to access
    
    # Let's generate the token depending if we set AuthTokenLimitByIp
    if ipLimitation:
      token = hashlib.md5(''.join([secret, fileName, hexTime, os.environ["REMOTE_ADDR"]])).hexdigest()
    else:
      token = hashlib.md5(''.join([secret, fileName, hexTime])).hexdigest()
    
    # We build the url
    url = ''.join([protectedPath, token, "/", hexTime, fileName])
    return url   

def token(request,filename):
    #!/usr/bin/env python
    import os, time, hashlib
    
    secret = "secret string"                                # Same as AuthTokenSecret
    protectedPath = "/downloads/"                           # Same as AuthTokenPrefix
    ipLimitation = False                                    # Same as AuthTokenLimitByIp
    hexTime = "{0:x}".format(int(time.time()))              # Time in Hexadecimal      
    fileName = filename                       # The file to access
    
    # Let's generate the token depending if we set AuthTokenLimitByIp
    if ipLimitation:
      token = hashlib.md5(''.join([secret, fileName, hexTime, os.environ["REMOTE_ADDR"]])).hexdigest()
    else:
      token = hashlib.md5(''.join([secret, fileName, hexTime])).hexdigest()
    
    # We build the url
    url = ''.join([protectedPath, token, "/", hexTime, fileName])
    return HttpResponse(url)
          
def variables(request,dataset_id,package_id):
    from exploratory_analysis.models import Variables
    print '\nIn GET\n'  
    
    #grab the record with the given dataset_name
    dataset_name = dataset_id
    da = Variables.objects.filter(dataset_name=dataset_name)
    
    if da:
   
    #otherwise grab the contents and return as a list
    #note: da[0] is the only record in the filtering of the Dataset_Access objects
        dataset_list = []
        
        for dataset in da[0].variables.split(','):
            dataset_list.append(dataset)
            
        data = {'dataset_list' : dataset_list}
        data_string = json.dumps(data,sort_keys=False,indent=2)
    
        print("GET Done\n")
        print(data_string)
        variables = {'vars': [], 'seasons': []} 
        variables['seasons'] = ['ANN', 'DJF', 'MAM', 'JJA', 'SON', 'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        variables['vars'] = dataset_list;
        
        if data_string != "":
             return HttpResponse(json.dumps(variables))


    opts = Options()
    opts['path'] = ['/data/tropics/' + dataset_id + '/']
    opts['packages'] = [package_id.upper()]
    path1 = opts['path'][0]
    filt1 = None

    # create a filetable for the path
    dtree1 = dirtree_datafiles(opts, pathid=0)
    filetable1 = basic_filetable(dtree1, opts)
    print filetable1.nrows()
    print dir(filetable1)
    # you can get all regions from defines.all_regions at any time.
    # you can get the superset of all seasons from defines.all_regions at any time as well
    
    dm = diagnostics_menu()
    for pname in opts['packages']:
        pclass = dm[pname]()

        slist = pclass.list_diagnostic_sets()
        # slist contains "Set 1 - Blah Blah Blah", "Set 2 - Blah Blah Blah", etc 

        # now to get all variables, we need to extract just the integer from the slist entries.
        snums = [setnum(x) for x in slist.keys()]
        print slist
        print snums
        variables = {'vars': [], 'seasons': []}
        for s in slist.keys():
            sclass = slist[s]
            # This season list is a subset for a given diagnostic set. This is NOT implemented in land diags
            # yet; you'll just get the entire season list back. I should work on that.
            seasons = pclass.list_seasons()
    
            variables['vars'].extend(pclass.list_variables(filetable1, None, s))
            variables['seasons'] = seasons
            print 'seasons:' , seasons
            print 'variables: ', variables
    variables['vars']=list(set(variables['vars']))
  
    return HttpResponse(json.dumps(variables))
 
def setnum( setname ):
    """extracts the plot set number from the full plot set name, and returns the number.
    The plot set name should begin with the set number, e.g.
       setname = ' 2- Line Plots of Annual Implied Northward Transport'"""
    mo = re.search( r'\d', setname )   # matches decimal digits
    if mo is None:
        return None
    index1 = mo.start()                        # index of first match
    mo = re.search( r'\D', setname[index1:] )  # matches anything but decimal digits
    if mo is None:                             # everything past the first digit is another digit
        setnumber = setname[index1:]
    else:
        index2 = mo.start()                    # index of first match
        setnumber = setname[index1:index1+index2]
    return setnumber

def variables1(request):
    
    #print '\n\nIn variables'
    
    from menuhelper import variablelist
    
    data_string = variablelist.variableListHelper1(request)
    
    return HttpResponse(data_string)


#times service
#gets time ranges for a given variable id
#http://<host>/exploratory_analysis/times/variable_id'
def times(request,variable_id):
    from menuhelper import times
    
    data_string = times.timesHelper(request,variable_id)
    
    return HttpResponse(data_string)

  
def times1(request):  

    from menuhelper import times
    
    data_string = times.timesHelper1(request)
    
    return HttpResponse(data_string)



def packages1(request):  

    from menuhelper import packages
    
    data_string = packages.packagesHelper1(request)
    
    return HttpResponse(data_string)



  #####End Used in the geo page#####
  
  
  
  
  #####Used in the tree page#####
  
   
   

  
#  url(r'^diagplot/$', views.diagplot, name='diagplot'),
#http://<host>/diagplot
def diagplot(request):
    if request.POST:
        print 'posting diagplot'
        print 'figureName: ' + request.POST['figureName']
    elif request.DELETE:
        print 'deleting diagplot'
        print 'figureName: ' + request.DELETE['figureName']
    return HttpResponse("Here's the text of the Web page.")



#Tree Figures BookmarksAPI
#http://<host>/exploratory_analysis/login
#Need to store Bookmark name, bookmark variables, bookmark time periods, bookmark description
def login1(request):
    template = loader.get_template('exploratory_analysis/login1.html')


    print 'going to login1.html...'
    context = RequestContext(request, {
        
    })

    return HttpResponse(template.render(context))

#Tree Figures BookmarksAPI
#http://<host>/exploratory_analysis/logout
#Need to store Bookmark name, bookmark variables, bookmark time periods, bookmark description
def logout1(request):
    
    
    print 'going to logout1.html...'
    from django.contrib.auth import logout
    logout(request)
    
    template = loader.get_template('exploratory_analysis/logout1.html')

    context = RequestContext(request, {
        
    })

    return HttpResponse(template.render(context))



    
#Tree Figures BookmarksAPI
#http://<host>/exploratory_analysis/login
#Need to store Bookmark name, bookmark variables, bookmark time periods, bookmark description
def login(request):
    template = loader.get_template('exploratory_analysis/login.html')

    print 'going to login.html...'
    context = RequestContext(request, {
        
    })

    return HttpResponse(template.render(context))

#Tree Figures BookmarksAPI
#http://<host>/exploratory_analysis/logout
#Need to store Bookmark name, bookmark variables, bookmark time periods, bookmark description
def logout(request):
    
    
    print 'going to logout.html...'
    
    from django.contrib.auth import logout
    logout(request)
    
    template = loader.get_template('exploratory_analysis/logout.html')

    
    context = RequestContext(request, {
        
    })

    return HttpResponse(template.render(context))

#Authentication to ESGF and synching with django User database
#Caled when the user tries to login
def auth(request):
    
    print '\nin auth\n\n'
    
    from security import signin
    
    response = signin.esgf_login(request)
    
    return response


def register(request):
    
    username = ''
    password = ''
    email = ''
    if request.POST['register_username'] == None or request.POST['register_password'] == None:
        return HttpResponse("Error")
    else:
        username = request.POST['register_username']
        password = request.POST['register_password']
    
    if request.POST['register_email'] == None:
        email = 'N/A'
    
    print 'username: ' + username + ' password: ' + password + ' email: ' + email
    
    from django.db import IntegrityError
    
    try:
        from django.contrib.auth.models import User
        user = User.objects.create_user(username,email,password)
        user.save()
        return HttpResponse("Registered")
    except IntegrityError:
        return HttpResponse("Duplicate")
    
    
    






def tree(request):
    template = loader.get_template('exploratory_analysis/treeview.html')
    
    context = RequestContext(request, {
        'username' : 'jfharney',
    })
    
    return HttpResponse(template.render(context))
 
  
  
#Test classic view
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def classic_views_html(request):
    
    print 'in classic views html'
    
    options = request.GET.get('options')
    
    print 'options: ' + str(options)
    
    html = ""
    
    response = 'error'
    
    if request.method == "POST":
        sets = None
        varlist = None
        times = None
        package = None
        dataset = None
        
        json_data = json.loads(request.body)
        
        sets = json_data['set'] #should be a string. strip off the 'set' part of it, and drop unicode
        sets = str(sets.replace('set',''))
        varlist = json_data['vars'] #should be a list
        times = json_data['times'] #should be a list
        package = json_data['package'] #should be a string
        dataset = json_data['dataset']
        
        print 'sets: ' + str(sets)
        print 'varlist: ' + str(varlist) + ' ' #+ vars.length
        print 'times: ' + str(times) + ' ' #+ times.length
        print 'package: ' + package
        print 'dataset: ' + dataset
        
        
        if package == 'amwg':
            print 'atmosphere diagnostics'
        
            from classic import amwghtmlgenerator
            
            html = None
            html = amwghtmlgenerator.pageGenerator(sets, varlist, times, package, dataset, options)
            if html == None:
               html = '<div>set'+sets+' currently unimplemented</div>'
    
    response = html
    
    return HttpResponse(html);
    
@csrf_exempt
def classic_views(request):
    
    print 'in classic views'
    
    
    curlFlag = False
    
    response = 'error'
    
    if request.method == "POST":
        set = None
        vars = None
        times = None
        package = None
        dataset = None
        
        json_data = json.loads(request.body)
        
        set = json_data['set'] #should be a string
        vars = json_data['vars'] #should be a list
        times = json_data['times'] #should be a list
        package = json_data['package'] #should be a string
        dataset = json_data['dataset']
        
       #To be added region = json_data['region'] #should be a list

        regions = ['Global Land','Northern Hemisphere Land', 'Southern Hemisphere Land', 'Alaskan Arctic', 'Central U.S.', 'Mediterranean and Western Asia']  

        set3Headers = ['reg', 'landf','randf','turbf','cnFlx','frFlx','moistEnergyFlx','snow','albedo','hydro']
        #DONE to be added
        
        
        print 'set: ' + set
        print 'vars: ' + str(vars) + ' ' #+ vars.length
        print 'times: ' + str(times) + ' ' #+ times.length

      
        #change this to the specified directory structure
        #url_prefix = "/static/exploratory_analysis/img/classic/" + package + "/" + set + "/"

        print 'package: ' + str(package)
        print 'dataset: ' + str(dataset)
        
        print 'regions: ' + str(regions)
        
        #RAY's new code
        ####################################################

        
        vardict={}
        vardict['PFT_FIRE_CLOSS']={'RepUnits': 'PgC/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gC/m^2/s', 'desc': 'total pft-level fire C loss'}
        vardict['SNOWDP']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'm', 'desc': 'snow height'}
        vardict['LITHR']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2/s', 'desc': 'litter hetereotrophic respiration'}
        vardict['QSOIL']={'RepUnits': 'mm/d', 'sets': [1, 2, 5], 'NatUnits': 'mm/s', 'desc': 'ground evaporation'}
        vardict['WA']={'RepUnits': 'mm', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'mm', 'desc': 'water in the unconfined aquifer'}
        vardict['FSA']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'W/m^2', 'desc': 'absorbed solar radiation'}
        vardict['GROSS_NMIN']={'RepUnits': 'TgN/y', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2/s', 'desc': 'Gross N Mineralization'}
        vardict['ACTUAL_IMMOB']={'RepUnits': 'TgN/y', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2/s', 'desc': 'Actual Immobilization'}
        vardict['ZBOT']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'm', 'desc': 'atmospheric reference height'}
        vardict['WT']={'RepUnits': 'mm', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'mm', 'desc': 'total water storage'}
        vardict['LHEAT']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'W/m^2', 'desc': 'latent heat:FCTR+FCEV+FGEV'}
        vardict['NBSA']={'RepUnits': 'NA', 'sets': [2, 3, 5], 'NatUnits': 'proportion', 'desc': 'near-IR black-sky albedo'}
        vardict['SNOWAGE']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'unitless', 'desc': 'snow age'}
        vardict['POTENTIAL_IMMOB']={'RepUnits': 'TgN/y', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2/s', 'desc': 'Potential Immobilization'}
        vardict['RR']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2/s', 'desc': 'root respiration (fine root MR + total root GR)'}
        vardict['FSNO']={'RepUnits': 'NA', 'sets': [2, 3, 5], 'NatUnits': 'unitless', 'desc': 'fraction of ground covered by snow'}
        vardict['FGR']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'W/m^2', 'desc': 'heat flux into snow/soil (includes snow melt)'}
        vardict['CWDC_LOSS']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Coarse Woody Debris C Loss'}
        vardict['FSH']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'W/m^2', 'desc': 'sensible heat'}
        vardict['SOIL3N']={'RepUnits': 'TgN', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2', 'desc': 'soil organic matter N (slow pool)'}
        vardict['LITTERC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2', 'desc': 'Total Litter C'}
        vardict['SOIL3C']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'Soil organic matter C (slow pool)'}
        vardict['FSDSVDLN']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'direct vis incident solar radiation at local noon'}
        vardict['LIVESTEMC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'live stem C'}
        vardict['QBOT']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'kg/kg', 'desc': 'atmospheric specific humidity'}
        vardict['GR']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2/s', 'desc': 'total growth respiration'}
        vardict['TBOT']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'K', 'desc': 'atmospheric air temperature'}
        vardict['RETRANSN']={'RepUnits': 'TgN', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2', 'desc': 'plant pool of retranslocated N'}
        vardict['XIM']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': '+/-1', 'desc': 'moisture index'}
        vardict['FLDS']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'W/m^2', 'desc': 'atmospheric longwave radiation'}
        vardict['VWSA']={'RepUnits': 'NA', 'sets': [2, 3, 5], 'NatUnits': 'proportion', 'desc': 'visible white-sky albedo'}
        vardict['AGNPP']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2/s', 'desc': 'above ground net primary production'}
        vardict['GPP']={'RepUnits': 'PgC/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gC/m^2/s', 'desc': 'gross primary production'}
        vardict['TAUX']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'kg/m/s^2', 'desc': 'zonal surface stress'}
        vardict['FIRE_PROB']={'RepUnits': '0-1', 'sets': [1, 2, 3, 5, 6], 'NatUnits': '0-1', 'desc': 'daily fire probability'}
        vardict['FSRNI']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'diffuse nir reflected solar radiation'}
        vardict['RSSUN']={'RepUnits': 's/m', 'sets': [1, 2], 'NatUnits': 's/m', 'desc': 'Sunlit leaf stomatal resistance'}
        vardict['FIRESEASONL']={'RepUnits': 'days', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'days', 'desc': 'annual fire season length'}
        vardict['SOIL4N']={'RepUnits': 'TgN', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2', 'desc': 'Soil organic matter N (slowest pool)'}
        vardict['FSDSNDLN']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'direct nir incident solar radiation at local noon'}
        vardict['RNET']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'W/m^2', 'desc': 'net radiation:fsa-fira'}
        vardict['SOIL4C']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'Soil organic matter C (slowest pool)'}
        vardict['NPP']={'RepUnits': 'PgC/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gC/m^2/s', 'desc': 'net primary production'}
        vardict['TLAI']={'RepUnits': 'm2/m2', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'm2/m2', 'desc': 'total one-sided leaf area index'}
        vardict['FSDS']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'W/m^2', 'desc': 'atmospheric incident solar radiation'}
        vardict['FSDSVI']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'diffuse vis incident solar radiation'}
        vardict['LAISHA']={'RepUnits': 'm^2/m^2', 'sets': [1, 2, 5], 'NatUnits': 'm^2/m^2', 'desc': 'Shaded Projected Leaf Area Index'}
        vardict['TREFMXAV']={'RepUnits': 'K', 'sets': [2], 'NatUnits': 'K', 'desc': 'daily maximum of average 2m temperature'}
        vardict['HR']={'RepUnits': 'PgC/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gC/m^2/s', 'desc': 'total hetereotrophic respiration'}
        vardict['TOTVEGC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'total vegetation C, excluding cpool'}
        vardict['Q2M']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'kg/kg', 'desc': '2m specific humidity'}
        vardict['FSDSVD']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'direct vis incident solar radiation'}
        vardict['TSA']={'RepUnits': 'K', 'sets': [1, 2, 3, 5, 6, 9], 'NatUnits': 'K', 'desc': '2m air temperature'}
        vardict['QDRIP']={'RepUnits': 'mm/y', 'sets': [2], 'NatUnits': 'mm/s', 'desc': 'throughfall'}
        vardict['PREC']={'RepUnits': 'mm/d', 'sets': [1, 2, 3, 5, 6, 9], 'NatUnits': 'mm/s', 'desc': 'ppt: rain+snow'}
        vardict['QCHARGE']={'RepUnits': 'mm/d', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'mm/s', 'desc': 'aquifer recharge rate'}
        vardict['SOMHR']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2/s', 'desc': 'SOM hetereotrophic respiration'}
        vardict['SMINN']={'RepUnits': 'TgN', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2', 'desc': 'soil mineral N'}
        vardict['H2OCAN']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'mm', 'desc': 'intercepted water'}
        vardict['ZWT']={'RepUnits': 'm', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'm', 'desc': 'water table depth'}
        vardict['ALBEDO']={'RepUnits': '% reflected ', 'sets': [3, 6], 'NatUnits': 'proportion', 'desc': 'all-sky albedo:FSR/FSDS'}
        vardict['FCEV']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'W/m^2', 'desc': 'canopy evaporation'}
        vardict['SOILC_HR']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Soil C hetereotrophic respiration'}
        vardict['TOTCOLC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'total ecosystem C, incl veg and cpool'}
        vardict['SABV']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'solar rad absorbed by vegetation'}
        vardict['COL_NTRUNC']={'RepUnits': 'TgN', 'sets': [1, 5], 'NatUnits': 'gN/m^2', 'desc': 'column-level sink for N truncation'}
        vardict['FSRNDLN']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'direct nir reflected solar radiation at local noon'}
        vardict['ERRSEB']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'surface energy conservation error'}
        vardict['QVEGT']={'RepUnits': 'mm/d', 'sets': [1, 2, 5], 'NatUnits': 'mm/s', 'desc': 'canopy transpiration'}
        vardict['TAUY']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'kg/m/s^2', 'desc': 'meridional surface stress'}
        vardict['ERRH2O']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'mm', 'desc': 'total water conservation error'}
        vardict['SABG']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'solar rad absorbed by ground'}
        vardict['CPOOL']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'temporary photosynthate C pool'}
        vardict['TOTLITC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'total litter carbon'}
        vardict['EVAPFRAC']={'RepUnits': 'NA', 'sets': [2, 3], 'NatUnits': 'unitless', 'desc': 'LHEAT/(LHEAT+FSH)'}
        vardict['PFT_CTRUNC']={'RepUnits': 'PgC', 'sets': [1, 5], 'NatUnits': 'gC/m^2', 'desc': 'pft-level sink for C truncation'}
        vardict['LIVECROOTC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'live coarse root carbon'}
        vardict['FIRA']={'RepUnits': 'NA', 'sets': [2, 3, 6], 'NatUnits': 'W/m^2', 'desc': 'net infrared (longwave) radiation'}
        vardict['SOILLIQ']={'RepUnits': 'kg/m^2', 'sets': [1, 2], 'NatUnits': 'kg/m^2', 'desc': 'soil liquid water : layers 1-10'}
        vardict['SOILC_LOSS']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Soil C Loss'}
        vardict['COL_FIRE_CLOSS']={'RepUnits': 'PgC/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gC/m^2/s', 'desc': 'total column-level fire C loss'}
        vardict['TREFMNAV']={'RepUnits': 'K', 'sets': [2], 'NatUnits': 'K', 'desc': 'daily minimum of average 2m temperature'}
        vardict['SOILICE']={'RepUnits': 'kg/m^2', 'sets': [1, 2], 'NatUnits': 'kg/m^2', 'desc': 'soil ice : layers 1-10'}
        vardict['COL_FIRE_NLOSS']={'RepUnits': 'TgN/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gN/m^2/s', 'desc': 'total column-level fire N loss'}
        vardict['ER']={'RepUnits': 'PgC/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gC/m^2/s', 'desc': 'total ecosystem respiration (AR + HR)'}
        vardict['QDRAI']={'RepUnits': 'mm/d', 'sets': [1, 2, 5], 'NatUnits': 'mm/s', 'desc': 'sub-surface drainage'}
        vardict['WOODC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2', 'desc': 'Wood C'}
        vardict['FCOV']={'RepUnits': 'unitless [0-1]', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'unitless [0-1]', 'desc': 'fractional area with water table at surface'}
        vardict['TSAI']={'RepUnits': 'm2/m2', 'sets': [1, 2, 5], 'NatUnits': 'm2/m2', 'desc': 'total one-sided stem area index'}
        vardict['FSRVDLN']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'direct vis reflected solar radiation at local noon'}
        vardict['ESAI']={'RepUnits': 'm2/m2', 'sets': [1, 2], 'NatUnits': 'm2/m2', 'desc': 'exposed one-sided stem area index'}
        vardict['FPSN']={'RepUnits': 'PgC/y', 'sets': [1, 2], 'NatUnits': 'umol/m^2/s', 'desc': 'photosynthesis'}
        vardict['MR']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2/s', 'desc': 'maintenance respiration'}
        vardict['FSH_G']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'sensible heat from ground'}
        vardict['SNOWICE']={'RepUnits': 'kg/m^2', 'sets': [1, 2], 'NatUnits': 'kg/m^2', 'desc': 'snow ice'}
        vardict['WIND']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'm/s', 'desc': 'atmospheric wind velocity magnitude'}
        vardict['PSNSHADE_TO_CPOOL']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2/s', 'desc': 'GPP from Shaded Canopy'}
        vardict['RETRANSN_TO_NPOOL']={'RepUnits': 'TgN/y', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2/s', 'desc': 'Retranslocated N to NPool'}
        vardict['QVEGE']={'RepUnits': 'mm/y', 'sets': [2, 5], 'NatUnits': 'mm/s', 'desc': 'canopy evaporation'}
        vardict['CANOPY_EVAPORATION']={'RepUnits': 'mm/d', 'sets': [1], 'NatUnits': 'mm/s', 'desc': 'Canopy Evaporation'}
        vardict['SMINN_TO_NPOOL']={'RepUnits': 'TgN/y', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2/s', 'desc': 'Mineral N to NPool'}
        vardict['CWDC_HR']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Coarse Woody Debris C Hetereotrophic respiration'}
        vardict['NEE']={'RepUnits': 'PgC/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gC/m^2/s', 'desc': 'net ecosys exchange of C;incl fire flx;pos for source'}
        vardict['FSM']={'RepUnits': 'NA', 'sets': [2, 5], 'NatUnits': 'W/m^2', 'desc': 'snow melt heat flux'}
        vardict['FROOTC_LOSS']={'RepUnits': 'PgC/m2y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Fine root C Loss'}
        vardict['FSR']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'reflected solar radiation'}
        vardict['FGNET']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'net ground heat flux:fgr-fsm'}
        vardict['ET']={'RepUnits': 'mm/d ', 'sets': [3, 5], 'NatUnits': 'mm/s', 'desc': 'Evapotranspiration'}
        vardict['NEP']={'RepUnits': 'PgC/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gC/m^2/s', 'desc': 'net ecosystem production;excl fire flx;pos for sink'}
        vardict['ANN_FAREA_BURNED']={'RepUnits': 'proportion', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'proportion', 'desc': 'annual total fractional area burned'}
        vardict['SMINN_LEACHED']={'RepUnits': 'TgN/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gN/m^2/s', 'desc': 'Nitrogen Leached'}
        vardict['ERRSOL']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'solar radiation conservation error'}
        vardict['TLAKE']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'K', 'desc': 'lake temperature'}
        vardict['BGNPP']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2/s', 'desc': 'below ground net primary production'}
        vardict['ASA']={'RepUnits': 'NA', 'sets': [2, 3, 9], 'NatUnits': 'proportion', 'desc': 'all-sky albedo:FSR/FSDS'}
        vardict['PFT_FIRE_NLOSS']={'RepUnits': 'TgN/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gN/m^2/s', 'desc': 'total pft-level fire N loss'}
        vardict['FSRND']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'direct nir reflected solar radiation'}
        vardict['LEAFC_ALLOC']={'RepUnits': 'PgC/m2y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Leaf C Allocation'}
        vardict['TOTRUNOFF']={'RepUnits': 'mm/d', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'mm/s', 'desc': 'Runoff:qover+qdrai+qrgwl'}
        vardict['CO2_PPMV']={'RepUnits': 'ppmv', 'sets': [1, 5], 'NatUnits': 'ppmv', 'desc': 'CO2 concentration'}
        vardict['BTRAN']={'RepUnits': 'unitless', 'sets': [1, 2, 3, 6], 'NatUnits': 'unitless', 'desc': 'transpiration beta factor'}
        vardict['SNOWLIQ']={'RepUnits': 'kg/m^2', 'sets': [1, 2], 'NatUnits': 'kg/m^2', 'desc': 'snow liquid water'}
        vardict['FSRVI']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'diffuse vis reflected solar radiation'}
        vardict['FSDSND']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'direct nir incident solar radiation'}
        vardict['FSDSNI']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'diffuse nir incident solar radiation'}
        vardict['CWDC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'coarse woody debris carbon'}
        vardict['FCTR']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'W/m^2', 'desc': 'canopy transpiration'}
        vardict['LEAFC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'leaf carbon'}
        vardict['P-E']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'mm/s', 'desc': 'PREC-ET'}
        vardict['SR']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2/s', 'desc': 'total soil respiration (HR + root resp)'}
        vardict['SUPPLEMENT_TO_SMINN']={'RepUnits': 'TgN/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gN/m^2/s', 'desc': 'supplement to mineral nitrogen'}
        vardict['NDEP_TO_SMINN']={'RepUnits': 'TgN/y', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2/s', 'desc': 'nitrogen deposition'}
        vardict['RSSHA']={'RepUnits': 's/m', 'sets': [1, 2], 'NatUnits': 's/m', 'desc': 'shaded leaf stomatal resistance'}
        vardict['FSH_V']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'sensible heat from vegetation'}
        vardict['XSMRPOOL']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'Temporary Photosynthate C Pool'}
        vardict['FGEV']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'W/m^2', 'desc': 'ground evaporation'}
        vardict['QOVER']={'RepUnits': 'mm/d', 'sets': [1, 2, 5], 'NatUnits': 'mm/s', 'desc': 'surface runoff'}
        vardict['DEADSTEMC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'dead stem carbon'}
        vardict['QMELT']={'RepUnits': 'mm/y', 'sets': [2], 'NatUnits': 'mm/s', 'desc': 'snow melt'}
        vardict['MEAN_FIRE_PROB']={'RepUnits': 'proportion', 'sets': [1, 2, 3, 5, 6], 'NatUnits': '0-1', 'desc': 'e-folding mean of daily fire probability'}
        vardict['COL_CTRUNC']={'RepUnits': 'PgC', 'sets': [1, 5], 'NatUnits': 'gC/m^2', 'desc': 'column-level sink for C truncation'}
        vardict['LEAFC_LOSS']={'RepUnits': 'PgC/m2y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Leaf C Loss'}
        vardict['NET_NMIN']={'RepUnits': 'TgN/y', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2/s', 'desc': 'Net N Mineralization'}
        vardict['SNOW']={'RepUnits': 'NA', 'sets': [2, 5], 'NatUnits': 'mm/s', 'desc': 'atmospheric snow'}
        vardict['TOTSOMC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'total SOM carbon'}
        vardict['FROOTC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'fine root carbon'}
        vardict['ELAI']={'RepUnits': 'm2/m2', 'sets': [1, 2], 'NatUnits': 'm2/m2', 'desc': 'exposed one-sided leaf area index'}
        vardict['TOTSOILLIQ']={'RepUnits': 'kg/m^2', 'sets': [1], 'NatUnits': 'kg/m^2', 'desc': 'total soil liquid water'}
        vardict['SOILC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2', 'desc': 'soil organic matter C (fast pool)'}
        vardict['H2OSOI']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'mm3/mm3', 'desc': 'volumetric soil water'}
        vardict['NDEPLOY']={'RepUnits': 'TgN/y', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2/s', 'desc': 'Total N Deployed in New Growth'}
        vardict['TV']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'K', 'desc': 'vegetation temperature'}
        vardict['PSNSUN_TO_CPOOL']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2/s', 'desc': 'GPP from Sunlit Canopy'}
        vardict['FROOTC_ALLOC']={'RepUnits': 'PgC/m2y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Fine root C allocation'}
        vardict['WOODC_ALLOC']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Wood C Allocation'}
        vardict['TOTECOSYSC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'total ecosystem C, incl veg but excl cpool'}
        vardict['TOTSOILICE']={'RepUnits': 'kg/m^2', 'sets': [1], 'NatUnits': 'kg/m^2', 'desc': 'soil ice'}
        vardict['QRGWL']={'RepUnits': 'mm/d', 'sets': [1, 2, 5], 'NatUnits': 'mm/s', 'desc': 'surface runoff at glaciers, wetlands, lakes'}
        vardict['TG']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'K', 'desc': 'ground temperature'}
        vardict['QINFL']={'RepUnits': 'mm/d', 'sets': [1, 2], 'NatUnits': 'mm/s', 'desc': 'infiltration'}
        vardict['VBSA']={'RepUnits': 'NA', 'sets': [2, 3, 5], 'NatUnits': 'proportion', 'desc': 'visible black-sky albedo'}
        vardict['TOTECOSYSN']={'RepUnits': 'TgN', 'sets': [1], 'NatUnits': 'gN/m^2', 'desc': 'total ecosystem N'}
        vardict['TSNOW']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'K', 'desc': 'snow temperature'}
        vardict['FSRVD']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'direct vis reflected solar radiation'}
        vardict['FPG']={'RepUnits': 'proportion', 'sets': [1, 2, 5], 'NatUnits': 'proportion', 'desc': 'fraction of potential GPP'}
        vardict['TSOI']={'RepUnits': 'K', 'sets': [1, 2], 'NatUnits': 'K', 'desc': 'soil temperature : layers 1-10'}
        vardict['FIRE']={'RepUnits': 'NA', 'sets': [2, 3, 5, 6], 'NatUnits': 'W/m^2', 'desc': 'emitted infrared (longwave) radiation'}
        vardict['QINTR']={'RepUnits': 'mm/d', 'sets': [1, 2], 'NatUnits': 'mm/s', 'desc': 'interception'}
        vardict['FPI']={'RepUnits': 'proportion', 'sets': [1, 2, 5], 'NatUnits': 'proportion', 'desc': 'fraction of potential immobilization'}
        vardict['RAIN']={'RepUnits': 'NA', 'sets': [2, 5], 'NatUnits': 'mm/s', 'desc': 'atmospheric rain'}
        vardict['LITTERC_HR']={'RepUnits': 'PgC/m2y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Litter Hetereotrophic Respiration'}
        vardict['AR']={'RepUnits': 'PgC/y', 'sets': [1, 2, 3, 5, 6], 'NatUnits': 'gC/m^2/s', 'desc': 'autotrophic respiration (MR + GR)'}
        vardict['PFT_NTRUNC']={'RepUnits': 'TgN', 'sets': [1, 5], 'NatUnits': 'gN/m^2', 'desc': 'pft-level sink for N truncation'}
        vardict['QVEGEP']={'RepUnits': '%', 'sets': [5], 'NatUnits': '%', 'desc': 'canopy evap:QVEGE/(RAIN+SNOW)*100'}
        vardict['ERRSOI']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'W/m^2', 'desc': 'soil/lake energy conservation error'}
        vardict['LITTERC_LOSS']={'RepUnits': 'PgC/m2y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Litter C Loss'}
        vardict['DEADCROOTC']={'RepUnits': 'PgC', 'sets': [1, 2, 5], 'NatUnits': 'gC/m^2', 'desc': 'dead coarse root carbon'}
        vardict['H2OSNO']={'RepUnits': 'NA', 'sets': [2, 3, 5], 'NatUnits': 'mm', 'desc': 'total snow water equiv (SNOWICE + SNOWLIQ)'}
        vardict['LAISUN']={'RepUnits': 'm^2/m^2', 'sets': [1, 2, 5], 'NatUnits': 'm2/m2', 'desc': 'Sunlit Projected Leaf Area Index'}
        vardict['SOILPSI']={'RepUnits': 'MPa', 'sets': [1], 'NatUnits': 'MPa', 'desc': 'Soil Water Potential in Each Soil Layer'}
        vardict['WOODC_LOSS']={'RepUnits': 'PgC/y', 'sets': [1, 2, 5], 'NatUnits': 'gC/m2s', 'desc': 'Wood C Loss'}
        vardict['THBOT']={'RepUnits': 'NA', 'sets': [2], 'NatUnits': 'K', 'desc': 'atmospheric air potential temperature'}
        vardict['DENIT']={'RepUnits': 'TgN/y', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2/s', 'desc': 'Total Denitrification'}
        vardict['NWSA']={'RepUnits': 'NA', 'sets': [2, 3, 5], 'NatUnits': 'proportion', 'desc': 'near-IR white-sky albedo'}
        vardict['NFIX_TO_SMINN']={'RepUnits': 'TgN/y', 'sets': [1, 2, 5], 'NatUnits': 'gN/m^2/s', 'desc': 'nitrogen fixation'}
        
        
        if set == 'set1': 
        
                  #JOHN's example code
            #########################################
            #change this to the specified directory structure
            url_prefix = paths.staticfiles_dirs + "/img/classic/" + dataset + "/" + package + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package + "/set1_"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_vars = {'TSA', 'PREC'}        
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""        
            
            #Header
            html+="<p>\n" 
            html+="<b><font color=maroon size=+2>Set 1 Description: <b></font>Line plots of annual trends in energy balance, soil water/ice and temperature, runoff, snow water/ice, photosynthesis </b><br>\n"
            html+="<br clear=left>"
            html+="</p>\n"
            html+="<p>\n"
            html+="<A HREF=\"/static/exploratory_analysis/img/classic/lmwg/set1/variableList_1.html\" target=\"set1_Variables\">\n"
            html+="<font color=maroon size=+1 text-align: right><b>Lookup Table: Set 1 Variable Definition</b></font></a>\n"
            html+="</br>\n"
            html+="</p>\n"
           
            
            
            #Start table
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<TH><TH ALIGN=LEFT><font color=maroon>Trend</font>\n"
            html+="</TR>\n"
            
            
            #python for loop----------
            #Descriptions are (predefinedBrianSmithDictionary[key]) 
            
            
            
            for key in vardict:
                if 1 in vardict[key]['sets'] and key in vars:
                    html+="<TR>\n"
                    html+='<TH ALIGN=LEFT>'
                    html+=vardict[key]['desc']
                    html+='('
                    html+=key
                    html+=')'
                    html+='<TH ALIGN=LEFT>'
                    html+='<a href="#" onclick="displayImageClick('
                    #file.write(url_prefixIMAGE)#Here we write gif name
                    html+='\''
                    html+= 'http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + key + '.gif')
                    html+='\''
                    html+=');" onmouseover="displayImageHover(\''
                    #file.write(url_prefixIMAGE)#Here we write gif name again
                    html+='http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + key + '.gif')
                    html+='\''
                    html+=');" onmouseout="nodisplayImage();">plot</A>\n'
                    html+="</TR>\n"
            

            #end for loop and end table generation-------------------------
            
            html+="</TABLE> \n"
            html+="</p>\n"
    
            
            return HttpResponse(html)
        
        
        elif set == 'set2':
            #########################################
            #change this to the specified directory structure

            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            #url_prefixIMAGE = "\'/static/exploratory_analysis/img/classic/" + package + "/" + dataset + "/set2_"
            url_prefixIMAGE = "/" + dataset + "/" + package + "/set2_"

            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_vars = {'TSA', 'PREC'}
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
                    
            #Header
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 2 Description: <b></font>Horizontal contour plots of DJF, MAM, JJA, SON, and ANN means </b><br>\n"
            html+="<br clear=left>"
            html+="</p>\n"
            html+="<p>\n"

            html+="<A HREF=\"/static/exploratory_analysis/img/classic/lmwg/set2/variableList_2.html\" target=\"set2_Variables\">\n"
            html+="<font color=maroon size=+1 text-align: right><b>Lookup Table: Set 2 Variable Definition</b></font></a>\n"

            html+="</br>\n"
            html+="</p>\n"
                   
                        
            #Start table
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n</hr>"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<td ALIGN=LEFT><font color=maroon>Description (variable)</font>\n</td>"
            for time in times:  
               html+="<td ALIGN=LEFT><font color=maroon>"+time+"</font>\n</td>"
            html+="</TR>\n"
          
            
            #python for loop----------
            #Descriptions are (predefinedBrianSmithDictionary[key]) 
            
            
            
            for key in vardict:
                if 2 in vardict[key]['sets'] and key in vars:
                    html+="<TR>\n"
                    html+='<Td ALIGN=LEFT>'
                    html+=vardict[key]['desc']
                    html+='('
                    html+=key
                    html+=')</td>'
                    
                    
                    for time in times:                
                        html+='<td ALIGN=LEFT>'
                        html+='<a href="#" onclick="displayImageClick('
                        html+='http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + time +'_' + key + '.gif')
                        html+=');" onmouseover="displayImageHover('
                        html+='http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + time +'_' + key + '.gif')
                        html+='\''
                        html+=');" onmouseout="nodisplayImage();">plot</A>\n'
                        html+='</td>'
                    html+="</TR>\n"
                    
                    
            #end for loop and end table generation-------------------------
            
       
            html+="</TABLE> \n"
            html+="</p>\n"
            
            
            return HttpResponse(html)
            
            
            
        elif set == 'set3':
             #########################################
            #change this to the specified directory structure
            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package +  "/set3_"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_vars = {'TSA', 'PREC'}
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
            
            #Header
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 3 Description: <b></font>Line plots of monthly climatology: regional air temperature, precipitation, runoff, snow depth, radiative fluxes, and turbulent fluxes</b><br>\n"
            html+="<br clear=left>"
            html+="</p>\n"
            html+="<p>\n"
            html+="<A HREF=\"/static/exploratory_analysis/img/classic/lmwg/set3/variableList_3.html\" target=\"set3_Variables\">\n"
            html+="<font color=maroon size=+1 text-align: right><b>Lookup Table: Set 3 Variable Definition</b></font></a>\n"
            html+="</br>\n"
            html+="</p>\n"
                   
                        
            #Start table
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n</hr>"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<td ALIGN=LEFT><B>All Model Data Regions</font>\n</td>"
            html+='<td>'
            html+='<a href="#" onclick="displayImageClick(\'' + 'http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + 'reg_all.gif') + '\''
            html+=');" onmouseover="displayImageHover(\'' + 'http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + 'reg_all.gif') + '\''
            html+=');" onmouseout="nodisplayImage();">Map</A>\n'
            html+='</td>'
            html+="</TR>\n"
            html+="<TR>\n"
            html+="<td>Region(s)"
            html+="</td>"
            html+="<td ALIGN=LEFT>Map</font>\n</td>"
            for var in vars:  
               html+="<td ALIGN=LEFT>"+var+"</font>\n</td>"
            html+="</tr>\n"
          
            
            #python for loop----------
            #Descriptions are (predefinedBrianSmithDictionary[key]) 
            
            def containedInDictionary( set ):
                "This prints a passed string into this function"
                for key in vardict:
                    if set in vardict[key]['sets']:  
                        return True
                    else:
                        return False
                    
            
            for region in regions:
                if containedInDictionary( 3 ):  
                    html+="<TR>\n"           
                    html+='<Td ALIGN=LEFT>'
                    html+=region
                    html+='</td>\n'
                    html+='\n'
                    html+='<td>'
                    html+='<a href="#" onclick="displayImageClick(\'' + 'http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + 'reg_' + region + '.gif') + '\''
                    html+=');" onmouseover="displayImageHover(\'' + 'http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + 'reg_' + region + '.gif') + '\''
                    html+=');" onmouseout="nodisplayImage();">Map</A>'
                    html+='</td>\n'
                    for var in vars:              
                        html+='<td ALIGN=center>'
                        html+='<a href="#" onclick="displayImageClick('
                        html+='http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + var+'_'+region+'.gif') +'\''
                        html+=');" onmouseover="displayImageHover('
                        html+='http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + var+'_'+region+'.gif') +'\''
                        html+=');" onmouseout="nodisplayImage();">Plot</A>'
                        html+='</td>\n'
                    html+="</TR>\n"
                    
                    
            #end for loop and end table generation-------------------------
            
       
            html+="</TABLE> \n"
            html+="</p>\n"
                    
            
            return HttpResponse(html)
            
            
        elif set == 'set5':
            #########################################
            #change this to the specified directory structure
            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package +  "/set5_"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_vars = {'TSA', 'PREC'}
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
                    
                    #Header
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 5 Description: <b></font>Tables of annual means </b><br>\n"
            html+="<br clear=left>"
            html+="</p>\n"
            html+="<p>\n"
            html+="<A HREF=\"/static/exploratory_analysis/img/classic/lmwg/set5/variableList_5.html\" target=\"set5_Variables\">\n"
            html+="<font color=maroon size=+1 text-align: right><b>Lookup Table: Set 5 Variable Definition</b></font></a>\n"
            html+="</br>\n"
            html+="</p>\n"
                   
                        
            #Start table
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n</hr>"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<td ALIGN=LEFT><font color=maroon>TABLE</font>\n</td>"
            html+="</TR>\n"
          
            html+="<tr>"
            html+='<TH ALIGN=LEFT>Regional Hydrologic Cycle'
            html+='<TH ALIGN=LEFT><font color=black><A HREF= "#" onclick="displayTable('
            html+='http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + 'hydReg.txt') +'\''
            html+=')\";>Table</a></font>'
            html+='</tr>'
                        
            html+="<tr>"
            html+='<TH ALIGN=LEFT>Global Biogeophysics'
            html+='<TH ALIGN=LEFT><font color=black><A HREF= "#" onclick="displayTable('
            html+=u'http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + 'clm.txt')
            html+='\')\";>Table</a></font>'
            html+='</tr>'
            
            html+='<tr>'
            html+='<TH ALIGN=LEFT>Global Carbon/Nitrogen'     
            html+='<TH ALIGN=LEFT><font color=black><A HREF= "#" onclick="displayTable('
            html+='http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + 'cn.json')
            html+='\')\";>Table</a></font>'
            html+='</tr>'
                 
                 
            #end for loop and end table generation-------------------------
            html+="</TABLE> \n"
            html+="</p>\n"
            
            
            return HttpResponse(html)
            
            
        elif set == 'set6':
             #########################################
            #change this to the specified directory structure
            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package +  "/set3_"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_vars = {'TSA', 'PREC'}
            
            def containedInDictionary( set ):
                "This prints a passed string into this function"
                for key in vardict:
                    if set in vardict[key]['sets']:  
                        return True
                    else:
                        return False
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
            
            #Header
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 6 Description: <b></font>Line plots of annual trends in regional soil water/ice and temperature, runoff, snow water/ice, photosynthesis</b><br>\n"
            html+="<br clear=left>"
            html+="</p>\n"
            html+="<p>\n"
            html+="<A HREF=\"/static/exploratory_analysis/img/classic/lmwg/set6/variableList_6.html\" target=\"set6_Variables\">\n"
            html+="<font color=maroon size=+1 text-align: right><b>Lookup Table: Set 6 Variable Definition</b></font></a>\n"
            html+="</br>\n"
            html+="</p>\n"
                   
                        
            #Start table
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n</hr>"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<td ALIGN=LEFT><B>All Model Data Regions</font>\n</td>"
            html+='<td>'
            html+='<a href="#" onclick="displayImageClick(\'' + 'http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + 'reg_all.gif') + '\''
            html+=');" onmouseover="displayImageHover(\'' + 'http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + 'reg_all.gif') + '\''
            html+=');" onmouseout="nodisplayImage();">Map</A>\n'
            html+='</td>'
            html+="</TR>\n"
            html+="<TR>\n"
            html+="<td>Region(s)"
            html+="</td>"
            html+="<td ALIGN=LEFT>Map</font>\n</td>"
            for var in vars:  
               html+="<td ALIGN=LEFT>"+var+"</font>\n</td>"
            html+="</tr>\n"
          
            
            #python for loop----------
            #Descriptions are (predefinedBrianSmithDictionary[key]) 
            
            
                    
            
            for region in regions:
                if containedInDictionary( 6 ):  
                    html+="<TR>\n"            
                    html+='<Td ALIGN=LEFT>'
                    html+=region
                    html+='</td>\n'
                    html+='\n'
                    html+='<td>'
                    html+='<a href="#" onclick="displayImageClick(\'set6_reg_'+region+'.gif\''
                    html+=');" onmouseover="displayImageHover(\'set6_reg_'+region+'.gif\''
                    html+=');" onmouseout="nodisplayImage();">Map</A>'
                    html+='</td>\n'
                    for var in vars:              
                        html+='<td ALIGN=center>'
                        html+='<a href="#" onclick="displayImageClick('
                        html+='http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + var+'_'+region+'.gif') +'\''
                        html+=');" onmouseover="displayImageHover('
                        html+='http://' + paths.ea_hostname + generate_token_url(url_prefixIMAGE + var+'_'+region+'.gif') +'\''
                        html+=');" onmouseout="nodisplayImage();">Plot</A>'
                        html+='</td>\n'
                    html+="</TR>\n"
                    
                    
            #end for loop and end table generation-------------------------
            
       
            html+="</TABLE> \n"
            html+="</p>\n"

            
            return HttpResponse(html)
            
        elif set == 'set7':
            #########################################
            #change this to the specified directory structure
            #url_prefix = "/home/user/Desktop/AptanaWorkspace/climate/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/classic/" + package + "/" + set + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package +  "/set7_"
            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_vars = {'TSA', 'PREC'}
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
            
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 7 Description: <b></font>Line plots, tables, and maps of RTM river flow and discharge to oceans </b><br>\n"
            html+="<br clear=left>\n"
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\">\n"
            html+="<TABLE>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=red>TABLE</font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>RTM flow at station for world's 50 largest rivers\\n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayTable(\'http://"+generate_token_url(url_prefixIMAGE+"table_RIVER_STN_VOL.txt") + "\');\">Table</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=red>SCATTER PLOTS</font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>RTM flow at station versus obs for world's 10 largest rivers (QCHANR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick(\'http://"+generate_token_url(url_prefixIMAGE+"scatter_50riv.gif") + "\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"scatter_50riv.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=red>LINE PLOTS</font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Mean annual cycle of river flow at station for world's 10 largest rivers (QCHANR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"mon_stndisch_10riv.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"mon_stndisch_10riv.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Annual discharge into the Global Ocean (QCHOCNR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ann_disch_globalocean.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ann_disch_globalocean.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Annual discharge into the Atlantic Ocean (QCHOCNR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ann_disch_atlantic.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ann_disch_atlantic.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Annual discharge into the Indian Ocean (QCHOCNR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ann_disch_indian.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ann_disch_indian.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Annual discharge into the Pacific Ocean (QCHOCNR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ann_disch_pacific.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ann_disch_pacific.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Mean annual cycle of discharge into the oceans (QCHOCNR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"mon_disch.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"mon_disch.gif');\" onmouseout=\"nodisplayImage();\">plot</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=red>MAPS</font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Station locations (50 largest rivers)\n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"stations.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"stations.gif');\" onmouseout=\"nodisplayImage();\">Map</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>Ocean Basins\n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ocean_basin_index.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ocean_basin_index.gif');\" onmouseout=\"nodisplayImage();\">Map</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>River Flow (QCHANR) \n"
            html+="<TH ALIGN=LEFT><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"ANN_QCHANR_Ac.gif');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"ANN_QCHANR_Ac.gif');\" onmouseout=\"nodisplayImage();\">Model1</A> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=red>VARIABLES</font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>QCHANR \n"
            html+="<TH ALIGN=LEFT>NativeUnits [m^3/s] \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT>QCHOCNR \n"
            html+="<TH ALIGN=LEFT>NativeUnits [m^3/s] \n"
            html+="<TR>\n"
            html+="</table>\n"
            
            html+="</p>\n"
            
        
            return HttpResponse(html)
            
        elif set == 'set9':
            #########################################
            #change this to the specified directory structure
            #url_prefix = "/home/user/Desktop/AptanaWorkspace/climate/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/classic/" + package + "/" + set + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package +  "/set9_"
            url_prefix = paths.staticfiles_dirs + "/img/classic/" + package + "/" + set + "/"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            #END JOHN's code
        
            #Construct table with description (variable) and link to plot
            #Input from json object from user selection
            #user_selected_vars = {'TSA', 'PREC'}
            
            #Start writing file (SPECIFY LOCATION TO WRITE FILE TO HERE)     Example: land/tropics_warming_th_q/img/
            html=""
                    
            html+="<p>\n"
            html+="<b><font color=maroon size=+2>Set 9 Description: <b></font>Contour plots and statistics for precipitation and temperature.  Statistics include DJF, JJA, and ANN biases, and RMSE, correlation and standard deviation of the annual cycle relative to observations</b><br>\n"
            html+="<br clear=left>\n"
            html+="<p>\n"
            html+="<hr noshade size=2 size=\"100%\"> \n"
            html+="<TABLE> \n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1> 1. RMSE </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"rmse_TSA.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"rmse_TSA.gif\');\" onmouseout=\"nodisplayImage();\">TSA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"rmse_PREC.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"rmse_PREC.gif\');\" onmouseout=\"nodisplayImage();\">PREC</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"rmse_ASA.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"rmse_ASA.gif\');\" onmouseout=\"nodisplayImage();\">ASA</A>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1> 2. Seasonal bias </font>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1>&nbsp&nbsp&nbsp&nbsp TSA </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_TSA_DJF.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_TSA_DJF.gif\');\" onmouseout=\"nodisplayImage();\">DJF</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_TSA_MAM.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_TSA_MAM.gif\');\" onmouseout=\"nodisplayImage();\">MAM</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_TSA_JJA.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_TSA_JJA.gif\');\" onmouseout=\"nodisplayImage();\">JJA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_TSA_SON.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_TSA_SON.gif\');\" onmouseout=\"nodisplayImage();\">SON</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_TSA_ANN.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_TSA_ANN.gif\');\" onmouseout=\"nodisplayImage();\">ANN</A>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1>&nbsp&nbsp&nbsp&nbsp PREC </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_PREC_DJF.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_PREC_DJF.gif\');\" onmouseout=\"nodisplayImage();\">DJF</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_PREC_MAM.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_PREC_MAM.gif\');\" onmouseout=\"nodisplayImage();\">MAM</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_PREC_JJA.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_PREC_JJA.gif\');\" onmouseout=\"nodisplayImage();\">JJA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_PREC_SON.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_PREC_SON.gif\');\" onmouseout=\"nodisplayImage();\">SON</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_PREC_ANN.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_PREC_ANN.gif\');\" onmouseout=\"nodisplayImage();\">ANN</A>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1>&nbsp&nbsp&nbsp&nbsp ASA </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_ASA_DJF.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_ASA_DJF.gif\');\" onmouseout=\"nodisplayImage();\">DJF</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_ASA_MAM.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_ASA_MAM.gif\');\" onmouseout=\"nodisplayImage();\">MAM</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_ASA_JJA.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_ASA_JJA.gif\');\" onmouseout=\"nodisplayImage();\">JJA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_ASA_SON.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_ASA_SON.gif\');\" onmouseout=\"nodisplayImage();\">SON</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"bias_ASA_ANN.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"bias_ASA_ANN.gif\');\" onmouseout=\"nodisplayImage();\">ANN</A>\n"
            html+="<TR>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1> 3. Correlation </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"corr_TSA.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"corr_TSA.gif\');\" onmouseout=\"nodisplayImage();\">TSA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"corr_PREC.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"corr_PREC.gif\');\" onmouseout=\"nodisplayImage();\">PREC</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"corr_ASA.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"corr_ASA.gif\');\" onmouseout=\"nodisplayImage();\">ASA</A>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1> 4. Standard Deviation </font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"stdev_TSA.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"stdev_TSA.gif\');\" onmouseout=\"nodisplayImage();\">TSA</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"stdev_PREC.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"stdev_PREC.gif\');\" onmouseout=\"nodisplayImage();\">PREC</A>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayImageClick("+url_prefixIMAGE+"stdev_ASA.gif\');\" onmouseover=\"displayImageHover("+url_prefixIMAGE+"stdev_ASA.gif\');\" onmouseout=\"nodisplayImage();\">ASA</A>\n"
            html+="<TR>\n"
            html+="<TH ALIGN=LEFT><font color=navy size=+1> 5. Tables</font>\n"
            html+="<TH ALIGN=center><a href=\"#\" onclick=\"displayTable("+url_prefixIMAGE+"statTable.html\');\">All Variables</A>\n"
            html+="<TR>\n"
            html+="<TR>\n"
            html+="<TR>\n"
            html+="</TABLE>\n"
            html+="</p>\n"
            
            return HttpResponse(html)
            
        else:
            url_prefix = "/static/exploratory_analysis/img/classic/" + package + "/" + set + "/"
            
            #assemble the url to be returned
            url = url_prefix + set + ".html"
            response = url;
        
        
        
        #except KeyError:
        #    print 'in key error'
        #    HttpResponseServerError("Malformed data!")
    else:
        print 'not post'
        
    
    
    #added the '\n' for 
    return HttpResponse(response + '\n')  
  



def datasetsList(request,user_id):
    
    print 'in dataset list'
    
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

    return jsonStr







  ############
  #Treeview bookmarks API#
  ############
  
  
  #http://<host>/exploratory_analysis/tree_bookmarks
#Tree Bookmarks API
#Need to store Bookmark name, bookmark variables, bookmark time periods, bookmark description
def tree_bookmarks(request):
    
    from exploratory_analysis.models import Tree_Bookmarks
    
    tree_bookmark_name = None
    tree_bookmark_datasetname = None
    tree_bookmark_realm = None
    tree_bookmark_username = None
    tree_bookmark_variables = None
    tree_bookmark_times = None
    tree_bookmark_sets = None
    tree_bookmark_description = None
    tree_cache_url = None
    
    print 'in tree bookmarks...request method: ' + request.method
    
    if request.method == 'POST':
        
        
        tree_bookmark_name = request.POST['tree_bookmark_name']
        #print 'tree_bookmark_name: ' + tree_bookmark_name
        
        tree_bookmark_datasetname = request.POST['tree_bookmark_datasetname']
        print 'tree_bookmark_datasetname: ' + tree_bookmark_datasetname
        
        tree_bookmark_realm = request.POST['tree_bookmark_realm']
        #print 'tree_bookmark_realm: ' + tree_bookmark_realm
        
        
        tree_bookmark_username = request.POST['tree_bookmark_username']
        #print 'tree_bookmark_username: ' + tree_bookmark_username
        
        tree_bookmark_variables = request.POST['tree_bookmark_variables']
        #print 'tree_bookmark_variables: ' + tree_bookmark_variables
        
        tree_bookmark_times = request.POST['tree_bookmark_times']
        tree_bookmark_sets = request.POST['tree_bookmark_sets']
        tree_bookmark_description = request.POST['tree_bookmark_description']
        tree_cache_url = request.POST['tree_cache_url']
        
        print 'tree_cache_url: ' + tree_cache_url
        
        tree_bookmark_record = Tree_Bookmarks(
                                              tree_bookmark_name=tree_bookmark_name,
                                              tree_bookmark_datasetname=tree_bookmark_datasetname,
                                              tree_bookmark_realm=tree_bookmark_realm,
                                              tree_bookmark_username=tree_bookmark_username,
                                              tree_bookmark_variables=tree_bookmark_variables,
                                              tree_bookmark_times=tree_bookmark_times,
                                              tree_bookmark_sets=tree_bookmark_sets,
                                              tree_bookmark_description=tree_bookmark_description,
                                              tree_cache_url=tree_cache_url
                                              )
        
        print 'tree_cache_url ' + tree_cache_url
        
        #save to the database
        tree_bookmark_record.save()
        
        #save the json file
        
        
        
        print 'POST'
        
        return HttpResponse()
        
        
    elif request.method == 'GET':
        
        print 'in get'
        
        tree_bookmark_name = request.GET.get('tree_bookmark_name')
        tree_bookmark_datasetname = request.GET.get('tree_bookmark_datasetname')
        tree_bookmark_realm = request.GET.get('tree_bookmark_realm')
        tree_bookmark_username = request.GET.get('tree_bookmark_username')
    
        from exploratory_analysis.models import Tree_Bookmarks
    
        
        
        
        
        
        try:
            tree_bookmark_record = Tree_Bookmarks.objects.get(tree_bookmark_name=tree_bookmark_name,
                                      tree_bookmark_datasetname=tree_bookmark_datasetname,
                                      tree_bookmark_realm=tree_bookmark_realm,
                                      tree_bookmark_username=tree_bookmark_username)
    
            #print tree_bookmark_record.tree_cache_url
            data =  { 
                     'tree_bookmark_name' : tree_bookmark_record.tree_bookmark_name, 
                     'tree_bookmark_datasetname' : tree_bookmark_record.tree_bookmark_datasetname, 
                     'tree_bookmark_realm' : tree_bookmark_record.tree_bookmark_realm, 
                     'tree_bookmark_username' : tree_bookmark_record.tree_bookmark_username,
                     'tree_bookmark_variables' : tree_bookmark_record.tree_bookmark_variables, 
                     'tree_bookmark_times' : tree_bookmark_record.tree_bookmark_times, 
                     'tree_bookmark_sets' : tree_bookmark_record.tree_bookmark_sets, 
                     'tree_bookmark_description' : tree_bookmark_record.tree_bookmark_description,
                     'tree_cache_url' : tree_bookmark_record.tree_cache_url
                     }
            print 'DATA:',repr(data)
            data_string = json.dumps(data,sort_keys=True,indent=2)
        
            return HttpResponse(data_string)
        
    
        except:
            print "Unexpected error:"
            data =  { }
            data_string = json.dumps(data,sort_keys=True,indent=2)
            return HttpResponse(data_string)
            
        
        
        
        
        
        return HttpResponse(data_string)
    
        print 'GET'
    elif request.method == 'DELETE':
        
        tree_bookmark_name = request.GET.get('tree_bookmark_name')
        tree_bookmark_datasetname = request.GET.get('tree_bookmark_datasetname')
        tree_bookmark_realm = request.GET.get('tree_bookmark_realm')
        tree_bookmark_username = request.GET.get('tree_bookmark_username')
    
        from exploratory_analysis.models import Tree_Bookmarks
    
        Tree_Bookmarks.objects.filter(tree_bookmark_name=tree_bookmark_name,
                                      tree_bookmark_datasetname=tree_bookmark_datasetname,
                                      tree_bookmark_realm=tree_bookmark_realm,
                                      tree_bookmark_username=tree_bookmark_username).delete()
        
        print 'DELETE'
    
    
        return HttpResponse()
    
    else: 
        return HttpResponse()
    '''
#    season_list_str = ', '.join(season_list)
#    #default bookmark: bookmark + currentmillitime
#        if bookmark_name == None:
#            import time
#            print 'tme ' + str(time.time())
#            millis = int(round(time.time()*1000))
#            print 'millis' + str(millis)
#            bookmark_name = 'bookmark' + str(millis)
#            print 'using default bookmark name ' + bookmark_name
               
    
    '''  
  
def figure_bookmarks_get_helper(figure_bookmark_name,
                                figure_bookmark_datasetname,
                                figure_bookmark_realm,
                                figure_bookmark_username,
                                figure_bookmark_description,
                                figure_cache_ur
                                ):
    figure_bookmark_record = Figure_Bookmarks(
                                            figure_bookmark_name = figure_bookmark_name,
                                            figure_bookmark_datasetname = figure_bookmark_datasetname,
                                            figure_bookmark_realm = figure_bookmark_realm,
                                            figure_bookmark_username = figure_bookmark_username,
                                            figure_bookmark_description = figure_bookmark_description,
                                            figure_cache_url = figure_cache_url
                                              )
        
    figure_bookmark_record.save()
  
  
#Tree Figures BookmarksAPI
#http://<host>/exploratory_analysis/figure_bookmarks
#Need to store Bookmark name, bookmark variables, bookmark time periods, bookmark description
def figure_bookmarks(request):
    
    from exploratory_analysis.models import Figure_Bookmarks
    
    figure_bookmark_name = None
    figure_bookmark_realm = None
    figure_bookmark_datasetname = None
    figure_bookmark_username = None
    figure_bookmark_description = None
    figure_cache_url = None
    
    if request.method == 'POST':
        
        print 'In POST figure_bookmarks'
        
        
        figure_bookmark_name = request.POST['figure_bookmark_name']
        figure_bookmark_realm = request.POST['figure_bookmark_realm']
        figure_bookmark_datasetname = request.POST['figure_bookmark_datasetname']
        figure_bookmark_username = request.POST['figure_bookmark_username']
        figure_bookmark_description = request.POST['figure_bookmark_description']
        figure_cache_url = request.POST['figure_cache_url']
        
        
        
        figure_bookmark_record = Figure_Bookmarks(
                                            figure_bookmark_name = figure_bookmark_name,
                                            figure_bookmark_datasetname = figure_bookmark_datasetname,
                                            figure_bookmark_realm = figure_bookmark_realm,
                                            figure_bookmark_username = figure_bookmark_username,
                                            figure_bookmark_description = figure_bookmark_description,
                                            figure_cache_url = figure_cache_url
                                              )
        
        p = Figure_Bookmarks.objects.filter(
                                            figure_bookmark_name = request.POST['figure_bookmark_name'],
                                            figure_bookmark_datasetname = request.POST['figure_bookmark_datasetname']
                                            )
        
        if not p:
            figure_bookmark_record.save()
        
        
        
        return HttpResponse()
        
    
    elif request.method == 'GET':
        
        
        print 'In GET figure_bookmarks'
        
        figure_bookmark_name = request.GET.get('figure_bookmark_name')
        figure_bookmark_datasetname = request.GET.get('figure_bookmark_datasetname')
        figure_bookmark_realm = request.GET.get('figure_bookmark_realm')
        figure_bookmark_username = request.GET.get('figure_bookmark_username')
    
        from exploratory_analysis.models import Figure_Bookmarks
    
        print 'figure_bookmark_name: ' + figure_bookmark_name
        print 'figure_bookmark_datasetname: ' + figure_bookmark_datasetname
        print 'figure_bookmark_realm: ' + figure_bookmark_realm
        print 'figure_bookmark_username: ' + figure_bookmark_username
        
    
        try:
            figure_bookmark_record = Figure_Bookmarks.objects.get(figure_bookmark_name=figure_bookmark_name,
                                      figure_bookmark_datasetname=figure_bookmark_datasetname,
                                      figure_bookmark_realm=figure_bookmark_realm,
                                      figure_bookmark_username=figure_bookmark_username)
    
            #print tree_bookmark_record.tree_cache_url
            data =  { 
                 'figure_bookmark_name' : figure_bookmark_record.figure_bookmark_name, 
                 'figure_bookmark_datasetname' : figure_bookmark_record.figure_bookmark_datasetname, 
                 'figure_bookmark_realm' : figure_bookmark_record.figure_bookmark_realm, 
                 'figure_bookmark_username' : figure_bookmark_record.figure_bookmark_username,
                 'figure_bookmark_description' : figure_bookmark_record.figure_bookmark_description,
                 'figure_cache_url' : figure_bookmark_record.figure_cache_url
                 }
            print 'DATA:',repr(data)
            
            data_string = json.dumps(data,sort_keys=True,indent=2)
            return HttpResponse(data_string)
        
    
        except:
            print "Unexpected error:"
            data =  { }
            data_string = json.dumps(data,sort_keys=True,indent=2)
            return HttpResponse(data_string)
            
    
    elif request.method == 'DELETE':
        
        print 'DELETE'
        
        figure_bookmark_name = request.GET.get('figure_bookmark_name')
        figure_bookmark_datasetname = request.GET.get('figure_bookmark_datasetname')
        figure_bookmark_realm = request.GET.get('figure_bookmark_realm')
        figure_bookmark_username = request.GET.get('figure_bookmark_username')
    
        from exploratory_analysis.models import Figure_Bookmarks
    
        print 'figure_bookmark_name ' + figure_bookmark_name
        print 'figure_bookmark_datasetname ' + figure_bookmark_datasetname
        print 'figure_bookmark_realm ' + figure_bookmark_realm
        print 'figure_bookmark_username ' + figure_bookmark_username
        
        Figure_Bookmarks.objects.filter(figure_bookmark_name=figure_bookmark_name,
                                      figure_bookmark_datasetname=figure_bookmark_datasetname,
                                      figure_bookmark_realm=figure_bookmark_realm,
                                      figure_bookmark_username=figure_bookmark_username).delete()
        
        
        
        
    
        return HttpResponse()
    
    
#variable_namesAPI
#http://<host>/exploratory_analysis/variable_names/<short_name>
def variable_names(request,variable_short_name):
    
    print 'variable_short_name: ' + variable_short_name
    
    if request.method == 'POST':
        print 'POST Variable'
    elif request.method == 'DELETE':
        print 'DELETE Variable'
    elif request.method == 'GET':
        print 'GET Variable'
    else:
        print 'OTHER'
        
    return HttpResponse()






    
    
def timeseries(request, lat, lon, variable):
   import cdms2, json, cdutil.times
   # need lat/lon, dataset name, variable from the request
   #variable = str(request.POST['variable'])
   #lat = float(request.POST['lat'])
   #lon = float(request.POST['lon'])

   lon = int(lon)
   lat = int(lat)

   # To make URL values positive integers, we add +90 to lat and multiply by 60
   # And +180 to lon and multiply by 60. Need to undo that first.
   print 'values passed in: ',lat, lon
   mylat = lat/60
   mylat = mylat - 90
   mylon = lon/60
   mylon = mylon - 180

   # THIS NEEDS GREPPED FROM DATASET BUT FINE FOR NOW
   xf = 2
   yf = 2
   mylat = (mylat+90) * yf

   if(mylon < 0):
      mylon = (mylon+360)*xf
   elif(mylon >= 0):
      mylon = mylon*xf

   print 'my new coordinates: ', mylat, mylon

   #   might need to be changed on other machines. I'm not really sure why there is a problem with this
   #   dataset = os.path.join(default_sample_data_dir+'tropics_warming_th_q_co2', 'test.xml')
   dataset = os.path.join(default_sample_data_dir, 'test.xml')


   print 'dataset: ' + dataset
   # Note: It is assumed that we are given an index into the dataset rather
   # than actual lat/lon coordinates. This is not a problem currently, but
   # if this code gets used more, we should probably fix that.

   data = []
   f = cdms2.open(dataset)
   thevar = f(variable)
#   thevar = thevar(latitude=(-90,90), longitude=(-180, 180, 'cob'))
   
   axisIndex = thevar.getAxisIndex('time')
   timeAxis = thevar.getTime()
   #print timeAxis
   cdutil.times.setAxisTimeBoundsMonthly(timeAxis)
   #axisIndex = 0;
   # This code assumes time is the 0th axis. The slice/subregion methods
   # in CDAT don't appear to work, so I can't slice out a region based on
   # naming an axis. There must be a better way to do this, but I don't 
   # know what it is currently.
   # Also, for some reason data = thevar.data[:][lat][lon] doesn't work.
   # This could also be adapted to take subranges pretty trivially
   if(axisIndex == 0): 
     for i in range(thevar.shape[axisIndex]):
       data.append(float(thevar.data[i][int(mylat)][int(mylon)]))
   else:
      print 'Unsupported timeaxis != 0'
      quit()

   print data
   f.close()
   # Make the json now
   # Note - Most of the land datasets we have make it challenging to trivially get the
   # start/end month/year. They are all encoded as days since 1-1-1, but it is not necessarily
   # obvious that that is the case. There doesn't appear to be a trivial way to fix that. needs
   # more thought
   j = {}
   j['start_year'] = 151   
   j['start_month'] = 1
   j['end_year'] = 165
   j['end_month'] = 12
   j['timeseries_data'] = data


   return HttpResponse(json.dumps(j, separators=(',',':'), indent=2))




def avgmap(request, year, month, variable):
   dataset = os.path.join(default_map_sample_data_dir,"tropics_warming_th_q.clm2.h0.")
   dataset = dataset+year+'-'+month+'.nc'
   f = cdms2.open(dataset)
   thevar = f(variable)

   j = {}
   j['geo_data'] = thevar.data.tolist()
   f.close()
   return HttpResponse(json.dumps(j, separators=(',',':'), indent=2))







####Example...
def postStateExample(request):
    
    print 'in post state example'
    a = {'a' : 'hello'}
    return HttpResponse('hello')



