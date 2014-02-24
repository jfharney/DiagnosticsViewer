#flag for toggling connection to the diags backend
isConnected = True

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
#from exploratory_analysis.models import Diags
import json
import sys 

from paths import paths

from defaults import parameter_defaults

syspath_append_uvcmetrics = paths.syspath_append_uvcmetrics
syspath_append_cdscan = paths.syspath_append_cdscan

paths_cache_dir = paths.cache_dir
paths_front_end_cache_dir = paths.front_end_cache_dir

default_sample_data_dir = paths.default_sample_data_dir
img_cache_path = paths.img_cache_path

timeseries_cache_path = paths.timeseries_cache_path

generated_img_path = paths.generated_img_path

# import the diags code
if isConnected:
    #sys.path.append('/Users/8xo/software/exploratory_analysis/DiagnosticsGen/uvcmetrics/src/python')
    #sys.path.append('/Users/8xo/software/exploratory_analysis/uvcdat_light/build-uvcdat/install/Library/Frameworks/Python.framework/Versions/2.7/bin/cdscan')
    #sys.path.append(syspath_append_uvcmetrics)
    #sys.path.append(syspath_append_cdscan)
   
    
    from metrics.frontend.options import Options
    from metrics.computation.reductions import *
    from metrics.fileio.filetable import *
    from metrics.fileio.findfiles import *

    from metrics.frontend.treeview import TreeView 

cache_dir = paths_cache_dir#'/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/cache/'
    #cache_dir = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/'
front_end_cache_dir = paths_front_end_cache_dir#'../../../static/cache/'


#use these objects temporarily
print '\n\n\n\n\nsetting up figures store\n\n\n\n'
figures_store = {}

    
from django.http import HttpResponseRedirect








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
    
    print request.GET.get('q')
    
    template = loader.get_template('exploratory_analysis/index.html')
    
    context = RequestContext(request, {
        'username' : user_id,
    })

    return HttpResponse(template.render(context))





#geo map/time series view
#corresponds with url: http://<host>/exploratory_analysis/maps
def maps(request,user_id):
    username = 'jfharney'
    
    if user_id != None:
        username = user_id 
    
    template = loader.get_template('exploratory_analysis/mapview.html')
    
    context = RequestContext(request, {
      'username' : username,
    })
    
    return HttpResponse(template.render(context))


#geo map/time series view
#corresponds with url: http://<host>/exploratory_analysis/maps
def heatmap(request,user_id):
    username = 'jfharney'
    
    if user_id != None:
        username = user_id 
    
    template = loader.get_template('exploratory_analysis/heatmapview.html')
    
    context = RequestContext(request, {
      'username' : username,
    })
    
    return HttpResponse(template.render(context))





def figureGenerator(request):
      print 'in figure generator'
    
      #hard coded
      #path = default_sample_data_dir + 'tropics_warming_th_q_co2'
      
      
        
      variables = [request.POST['variables']]
      times = [request.POST['times']]
      sets = [request.POST['sets']]
      packages = [request.POST['packages']]
      realms = [request.POST['realms']]
      ''' 
      variables = ['TG']
      times = ['MAM']
      
      sets = ['1']
      packages = ['lmwg']
      realms = ['land']
      '''
      sets = ['1']
    
      print 'variables: ' + str(variables)
      print 'times: ' + str(times)
      print 'sets: ' + str(sets)
      print 'packages: ' + str(packages)
      print 'realms: ' + str(realms)
        
    
      inCache = False
      
      cachedFile = realms[0] + '_' + packages[0] + '_set' + sets[0] + '_' + times[0] + '_' + variables[0] + '.png'
      
      print 'cachedFile: ' + cachedFile
      
      #. => /Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/
      
      #. + exploratory_analysis/static/exploratory_analysis/img/treeex/
      #path = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/treeex/' + cachedFile
      path = './' +  'exploratory_analysis/static/exploratory_analysis/img/treeex/' + cachedFile
      print 'path: ' + path
      print 'absolute path: ' + os.path.abspath(path)
      print 'not in cache: ' + str(not inCache) + ' os isfile: ' + str(os.path.exists(path))
      
      if(os.path.exists(path)):
          inCache = True
    
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
        
          o._opts['path']=[default_sample_data_dir + 'tropics_warming_th_q_co2']
          o._opts['vars']=variables
          o._opts['times']=times
          #Note: only use 1 or 2 
          o._opts['sets']=sets
          o._opts['packages']=packages
          o._opts['realms']=realms
        
          
          #filepath = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/treeex/'
          filepath = generated_img_path
          filename = request.POST['realms'] + '_' + request.POST['packages'] + '_' + request.POST['sets'] + '_' + request.POST['times'] + '_' + request.POST['variables']
          import metrics.fileio.filetable as ft
          import metrics.fileio.findfiles as fi
          dtree1 = fi.dirtree_datafiles(o, pathid=0)
          filetable1 = ft.basic_filetable(dtree1, o)
          filetable2 = None
          print 'No second dataset for comparison'
             
          package=o._opts['packages']
    
          # this needs a filetable probably, or we just define the maximum list of variables somewhere
          im = ".".join(['metrics', 'packages', package[0], package[0]])
          if package[0] == 'lmwg':
             pclass = getattr(__import__(im, fromlist=['LMWG']), 'LMWG')()
          elif package[0]=='amwg':
             pclass = getattr(__import__(im, fromlist=['AMWG']), 'AMWG')()
    
          setname = o._opts['sets'][0]
          varid = o._opts['vars'][0]
          seasonid = o._opts['times'][0]
          print 'CALLING LIST SETS'
          slist = pclass.list_diagnostic_sets()
          print 'DONE CALLIGN LIST SETS'
          keys = slist.keys()
          keys.sort()
          import vcs
          print 'generating output.png ...'
          v = vcs.init()
          for k in keys:
             fields = k.split()
             if setname[0] == fields[0]:
                print 'calling init for ', k, 'varid: ', varid, 'seasonid: ', seasonid
                plot = slist[k](filetable1, filetable2, varid, seasonid)
                res = plot.compute()
                v.plot(res[0].vars, res[0].presentation, bg=1)
                
                v.png(filepath + filename)
          
    
    
      #return HttpResponse()
      return HttpResponse(cachedFile)



#New tree view
def treeex(request,user_id):
    
    
    
    
    #need a flag to indicated whether a tree 
    
    
    username = 'jfharney'
    
    #grab the username
    if user_id != None:
        username = user_id
    
    
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
 
 
    print 'bookmark list: ' + str(bookmark_list)
    print 'figure bookmark list ' + str(figure_bookmark_list)
 
 
    defaults = parameter_defaults.get_parameter_defaults()
    package_list = defaults['package_list']
    dataset_list = defaults['dataset_list']
    variable_list = defaults['variable_list']
    season_list = defaults['season_list']
    set_list = defaults['set_list']
    
 
    
    #first we check if the request is in the cache or if it is the initial call
    #if it is in the cache, no need to do any back end generation
    bookmark = request.GET.get('bookmark')
    
    print '\nbookmark: ' + str(bookmark)  
    
    #no bookmark is being loaded
    if bookmark == None:
        print '\n\n\n\nbookmark is none\n\n\n\n'
        
        
        #if something has been posted, then a tree could be built       
        if request.POST:
            
            posttype = request.POST['posttype']
            
            tree_bookmark_datasetname = request.POST['dataset']
            
            print 'tree_bookmark_datasetname----->' + tree_bookmark_datasetname + '\n\n\n\n'
            
            print 'in a post request with parameters'
            
            
            treename = request.POST['treename']
            
            #if there is no tree name give the tree a default name based on the timestamp
            if treename == None or treename == '':
                import time
                millis = int(round(time.time() * 1000))
                treename = 'tree' + str(millis)
            
            
            
            packages = ''
            #defaults here
            if request.POST['package'] == None:
                packages = ['lmwg']
            else:
                packages = [request.POST['package'] ]
            
            
            
            vars= ''
            variable_arr_str = request.POST['variable_arr_str']
            if variable_arr_str == None:
                print 'variable_arr_str is None'
                vars = ['TLAI', 'TG','NPP']
            else:
                print 'variable_arr_str: ' + variable_arr_str
                variable_arr = variable_arr_str.split(';')
                vars = variable_arr
                
            times = ''
            season_arr_str = request.POST['season_arr_str']
            if season_arr_str == None:
                print 'season_arr_str is None'
                times = ['MAR','APR','MAY','JUNE','JULY']
            else:
                season_arr = season_arr_str.split(';')
                times = season_arr
            
            sets_arr = ''
            sets_arr_str = request.POST['sets_arr_str']
            if sets_arr_str == None:
                print 'sets_arr_str is None'
            else:
                sets_arr = sets_arr_str.split(';')
                print 's: ' + sets_arr[0] 
                
            
            dataset = ''
            path = ''
            if request.POST['dataset'] == None:
                dataset = 'tropics_warming_th_q_co2'
                path = [default_sample_data_dir + 'tropics_warming_th_q_co2']
            else:
                dataset = request.POST['dataset']
                path = path = [default_sample_data_dir + request.POST['dataset']]
            
                
            
            #build tree here 
            #if the post type is "submit" then grab "temp.json", otherwise it is a saved bookmark
            if posttype == 'submit':
                treeFile = cache_dir + 'temp' + '.json'
            else:
                treeFile = cache_dir + treename + '.json'
            
            #### Start diagnostics generation here...
            #username = user_id
        
            o = Options()
       
       
            print 'varsssss---->' + str(vars)
       
            ##### SET THESE BASED ON USER INPUT FROM THE GUI
            o._opts['packages'] = packages
            o._opts['vars'] = vars
            o._opts['path'] = path
            o._opts['times'] = times
        
            
            
            ### NOTE: 'ANN' won't work for times this way, but that shouldn't be a problem
            datafiles = []
            filetables = []
            vars = o._opts['vars']
            #   print vars
    
            print 'packages--->' + str(packages)
            print 'vars--->' + str(vars)
            print 'times--->' + str(times)
            print 'dataset_list[0]--->' + dataset_list[0]
    
            for p in range(len(o._opts['path'])):
                print '\ndirtree\n',dirtree_datafiles(o,pathid=p)
                datafiles.append(dirtree_datafiles(o,pathid=p))
                filetables.append(basic_filetable(datafiles[p],o))
            
            print 'Creating diags tree view JSON file...'
        
            
        
            tv = TreeView()
            dtree = tv.makeTree(o, filetables,None,user=username,ftnames=[dataset_list[0]])
            tv.dump(filename=treeFile)
            
            
            
            response_data = {}
            response_data['treename'] = treename
            response_data['username'] = username
            return HttpResponse(json.dumps(response_data), content_type="application/json")
            
        #end if request.POST  
            
        
        template = loader.get_template('exploratory_analysis/treeex.html')
        treeloaded = 'false'
        
        
        
        '''
        tree_bookmark_datasetname = None
        
        #if information was relayed in the post, that means a tree is being created
        if request.POST:
            #tree_bookmark_name = request.POST['tree_bookmark_name']
            tree_bookmark_datasetname = request.POST['tree_bookmark_datasetname']
            
        
        
        #if this is the first time visiting the page (or no params given)
        if tree_bookmark_datasetname == None:
            print 'no dataset name given, display empty tree/only the options'
            
            
            
        
        else:
            print 'there is a dataset name given, display the new tree'
            treeloaded = 'true'
        '''   
        
       
        
        context = RequestContext(request, {
            'treeloaded' : treeloaded,
            'package_list' : package_list,
            'dataset_list' : dataset_list,
            'variable_list' : variable_list,
            'season_list' : season_list,
            'set_list' : set_list,
            'bookmark_list' : bookmark_list,
            'figure_bookmark_list' : figure_bookmark_list,
            'posttype':'save'
                                          
        })
        

        return HttpResponse(template.render(context))

        
        
    
    #otherwise there are bookmarks
    else:
        
        
        
        treeloaded = 'true'
        
            
   
        bookmark_name = bookmark
    
    
        #bookmark = 'Bookmark1'
        fileName = bookmark + ".json"
    
        cached_file_name = front_end_cache_dir + fileName
           
           
        #check if bookmark exists
        
        #mapping
        #/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/cache/
        #../../../static/cache/Bookmark2.json
        #
        mapped_file_name = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/'
        p = re.compile('../../../')
        check_file_name = p.sub( mapped_file_name, cached_file_name)
        
        treeFile = None
        
        '''
        print '\ntreeFile: ' + cached_file_name + \
              ' cached_file_name: ' +  cached_file_name + \
              ' check_file_name: ' + check_file_name + \
              '\n\texists? ' + str(os.path.exists(cached_file_name)) + \
              '\n\texists? ' + str(os.path.exists(check_file_name)) + \
              '\n\n'
        '''
        
        #if exists then return the tree state of that bookmark
        if os.path.exists(check_file_name):
            print 'Bookmark is there - proceed'   
            treeFile = diagsHelper(user_id,bookmark_name)
        else:
            print 'Bookmark is not there - do not proceed'
            treeloaded = 'false'
        
        
        
        
        
        #else return nothing
        
        
            
        template = loader.get_template('exploratory_analysis/treeex.html')
    
    
        
        
    
    
        context = RequestContext(request, {
            'treeloaded' : treeloaded,
            'username' : username,
            'cachedfile' : cached_file_name,
            'package_list' : package_list,
            'dataset_list' : dataset_list,
            'variable_list' : variable_list,
            'season_list' : season_list,
            'set_list' : set_list,
            'bookmark_list' : bookmark_list,
            'figure_bookmark_list' : figure_bookmark_list,
            'treefile': treeFile,
            'current_bookmark': bookmark,
            'posttype':'save'
            #'treeFile' : treeFile,
            })
        

        return HttpResponse(template.render(context))



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


  #grabs variables given a dataset
  #http://<host>/exploratory_analysis/variables/dataset_id
def variables(request,dataset_id):
    
    from menuhelper import variablelist
    
    data_string = variablelist.variableListHelper(request,dataset_id)
    
    return HttpResponse(data_string)
 
  
  
#times service
#gets time ranges for a given variable id
#http://<host>/exploratory_analysis/times/variable_id'
def times(request,variable_id):
    from menuhelper import times
    
    data_string = times.timesHelper(request,variable_id)
    
    return HttpResponse(data_string)

  
  

  #grabs the map
#
'''
Visualizations
#URL String:
  http://<host>/exploratory_analysis/datasetsList/<user_id>
  http://<host>/exploratory_analysis/visualizations

lists all the datasets given a user
output is:
{
  user : '',
  datasets : [],
  paths: [],
  year_range: [[]]
  
}
'''
def visualizations(request):
    
    
    print 'in visualizations'
    print request.GET.get('variable')
  
  
    variable = ''
    if(request.GET.get('variable') == None):
        variable = 'AR'
    else:
        variable = request.GET.get('variable')
  
  
  
    #statically load the json file from the cache - each file is labelled by variable <variable_name>.json
    
    #file = '/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/' + variable + '.json' 
  
  
    file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/' + variable + '.json' 
    
    
    with open(file , 'r') as myfile:
       data = myfile.read().replace('\n','')
      
    jsonData = json.dumps(data)

    return HttpResponse(jsonData)




  #####End Used in the geo page#####
  
  
  
  
  #####Used in the tree page#####
  
   
   
  
  #grabs the tree data
  #http://<host>/treedata/<user_id>
def treedata(request,user_id):
  
  username = user_id

  file = '/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare3.json';
  #file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare2.json';
  

  from pprint import pprint

  data = ''
  with open(file) as data_file:    
      data = json.load(data_file)
      pprint(data)
  
  url = 'http://cds.ccs.ornl.gov/y9s/singlef/i1850cn_cruncep_CNDA_Cli_b_2000-2009-i1850cn_cruncep_ctl_2000-2009/setsIndex.html'
  
  children_arr = [ { "name": "Set 1" } ]
  
  #data = { 'name' : 'LND_DIAG', 'url' : url, 'children' : children_arr }
  data_string = json.dumps(data,sort_keys=True,indent=2)
  print 'JSON:',data_string
          
          
          
  
  return HttpResponse(data_string)

  
  
  
  
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
def login(request):
    template = loader.get_template('exploratory_analysis/login.html')

    context = RequestContext(request, {
        
    })

    return HttpResponse(template.render(context))




def diagsHelper(user_id,bookmark_name):
    print 'in diags helper'
    
    
    #check the bookmark name
    
    
    treeFile = cache_dir + bookmark_name + '.json'
    
    import os
    
    print '\n\ntreeFile: ' + treeFile + '\n\texists? ' + str(os.path.exists(treeFile)) + '\n\n'
    
    treeFileExists = os.path.exists(treeFile)
    
    #if the file is not in the cache already, then we have to generate the file
    if not treeFileExists:
        #### Start diagnostics generation here...
        username = user_id
      
        print username
        
        o = Options()
        #   o.processCmdLine()
        #   o.verifyOptions()
       
       ##### SET THESE BASED ON USER INPUT FROM THE GUI
       
        #defaults here
        packages = ['lmwg']
        vars = ['TLAI', 'TG','NPP']
        path = [default_sample_data_dir + 'tropics_warming_th_q_co2']
        times = ['MAR','APR','MAY','JUNE','JULY']
        
        
        o._opts['packages'] = packages
        o._opts['vars'] = vars
        o._opts['path'] = path
        o._opts['times'] = times
        
        
        ### NOTE: 'ANN' won't work for times this way, but that shouldn't be a problem
        datafiles = []
        filetables = []
        vars = o._opts['vars']
        #   print vars
    
        for p in range(len(o._opts['path'])):
            print '\ndirtree\n',dirtree_datafiles(o,pathid=p)
            datafiles.append(dirtree_datafiles(o,pathid=p))
            filetables.append(basic_filetable(datafiles[p],o))
        '''
        index = 0
        for p in o._opts['path']:
          print '\ndirtree\n' , dirtree_datafiles(p)
          datafiles.append(dirtree_datafiles(p))
          filetables.append(basic_filetable(datafiles[index], o))
          index = index+1
        '''
        print 'Creating diags tree view JSON file...'
        
        
        
        tv = TreeView()
        dtree = tv.makeTree(o, filetables,None,user=username,ftnames=['tropics_warming_th_q_co2'])
        tv.dump(filename=treeFile)
        
        
        
    #return the file and the location of the file
    return treeFile











def tree(request):
    template = loader.get_template('exploratory_analysis/treeview.html')
    #template = loader.get_template('exploratory_analysis/tree.html')
    
    context = RequestContext(request, {
        'username' : 'jfharney',
    })
    
    return HttpResponse(template.render(context))
 
  
  
'''
def treedataBrian(request,user_id):
    
    username = user_id
  
    o = Options()
    #   o.processCmdLine()
    #   o.verifyOptions()
   
   ##### SET THESE BASED ON USER INPUT FROM THE GUI
    o._opts['packages'] = ['lmwg'] 
    o._opts['vars'] = ['TG']
    o._opts['path'] = [default_sample_data_dir + 'tropics_warming_th_q_co2']
    o._opts['times'] = ['JAN']
    ### NOTE: 'ANN' won't work for times this way, but that shouldn't be a problem
    datafiles = []
    filetables = []
    vars = o._opts['vars']
    #   print vars

    index = 0
    for p in o._opts['path']:
      datafiles.append(dirtree_datafiles(p))
      filetables.append(basic_filetable(datafiles[index], o))
      index = index+1

    print 'Creating diags tree view JSON file...'
    tv = TreeView()
    dtree = tv.makeTree(o, filetables)
    tv.dump(filename='flare11.json')
    
    


    file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare4.json';

    from pprint import pprint

    data = ''
    with open(file) as data_file:    
        data = json.load(data_file)
        pprint(data)
    
    url = 'http://cds.ccs.ornl.gov/y9s/singlef/i1850cn_cruncep_CNDA_Cli_b_2000-2009-i1850cn_cruncep_ctl_2000-2009/setsIndex.html'
    
    children_arr = [ { "name": "Set 1" } ]
    
    #data = { 'name' : 'LND_DIAG', 'url' : url, 'children' : children_arr }
    data_string = json.dumps(data,sort_keys=True,indent=2)
    print 'JSON:',data_string
            
            
            
    
    return HttpResponse(data_string)
'''  
 










'''
http://
'''
'''
def visualizationsBrian(request):
    
   print 'in visualizations Brian'
   
   o = Options()
#   o.processCmdLine()
#   o.verifyOptions()

   ##### SET THESE BASED ON USER INPUT FROM THE GUI
   o._opts['vars'] = ['PBOT'] 
  # o._opts['path'] = ['/path/to/a/dataset'] 
   o._opts['path'] = [default_sample_data_dir + 'tropics_warming_th_q_co2'] 
   o._opts['times'] = ['DJF']
   ### NOTE: 'ANN' won't work for times this way, but that shouldn't be a problem
   #####

   #### This will generate {var}-{times}-climatology.json

   # At this point, we have our options specified. Need to generate some climatologies and such
   datafiles = []
   filetables = []
   vars = o._opts['vars']
#   print vars

   index = 0
   for p in o._opts['path']:
      datafiles.append(dirtree_datafiles(p))
      filetables.append(basic_filetable(datafiles[index], o))
      index = index+1

   for var in o._opts['vars']:
      if var in filetables[0]._varindex.keys():
         for seas in o._opts['times']:
            vid = str(var)+'_'+str(seas)
            season = cdutil.times.Seasons([seas])
            rvar = reduced_variable(variableid = var,
               filetable = filetables[0],
               reduction_function=(lambda x, vid=vid: reduce_time_seasonal(x, season, vid=vid)))

            print 'Reducing ', var, ' for climatology ', seas
            data = {}
            red = rvar.reduce(o)
            filename = var+"-"+seas+"-climatology.json"
            print 'Writing to ', filename
            g = open(filename, 'w')
            data['geo_average_min'] = red.min()
            data['geo_average_max'] = red.max()
            mv = red.missing_value
            data['missing_value'] = mv
            data['geo_average_data'] = red.data.tolist()
            g_avg = cdutil.averager(red, axis='xy')
            data['geo_average_global'] = g_avg.data.tolist()
            json.dump(data, g, separators=(',',':'))
            g.close()
            print 'Done writing ', filename

  
  
  
   print request.GET.get('variable')
  
   variable = ''
   if(request.GET.get('variable') == None):
        variable = 'AR'
   else:
        variable = request.GET.get('variable')
  
   #file = '/Users/csg/Desktop/uvcdat-web/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/' + variable + '.json' 
   file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/' + variable + '.json' 
 
   with open(file , 'r') as myfile:
      data = myfile.read().replace('\n','')
      
   jsonData = json.dumps(data)

   #jsonData = json.dumps("{ 'variable' : '" + variable  +  "'} ")
   #print jsonData
  
  
  
  
   return HttpResponse(jsonData)

'''



  



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
    season_list_str = ', '.join(season_list)
    #default bookmark: bookmark + currentmillitime
        if bookmark_name == None:
            import time
            print 'tme ' + str(time.time())
            millis = int(round(time.time()*1000))
            print 'millis' + str(millis)
            bookmark_name = 'bookmark' + str(millis)
            print 'using default bookmark name ' + bookmark_name
               
    
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
    
    '''
    'figure_bookmark_name' : figure_bookmark_name,
    'figure_bookmark_realm' : figure_bookmark_realm,
    'figure_bookmark_datasetname' : figure_bookmark_datasetname,
    'figure_bookmark_username' : figure_bookmark_username,
    'figure_bookmark_description' : figure_bookmark_description,
    'figure_cache_url' : '../figure_cache_url.html'
    '''
    
    if request.method == 'POST':
        
        
        
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
        
        
        #print tree_bookmark_record
        print 'POST'
        
        return HttpResponse()
        
    
    elif request.method == 'GET':
        
        
        print '\n\n\nIN GET\n\n\n'
        
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
            
    
        '''
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
    
        print 'GET'
        '''
    elif request.method == 'DELETE':
        
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
        
        
        print 'DELETE'
        
        
    
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






    ''' from diagsHelper
    import os
    import shutil
    
    #srcfile = treeFile
    dstroot = cache_dir


    assert not os.path.isabs(treeFile)
    dstdir =  os.path.join(dstroot, os.path.dirname(treeFile))

    

    #file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare4.json';
    file = cache_dir + treeFile

    from pprint import pprint
    
    data = ''
    with open(file) as data_file:    
        data = json.load(data_file)
        pprint(data)
    
    url = 'http://cds.ccs.ornl.gov/y9s/singlef/i1850cn_cruncep_CNDA_Cli_b_2000-2009-i1850cn_cruncep_ctl_2000-2009/setsIndex.html'
    
    children_arr = [ { "name": "Set 1" } ]
    
    #data = { 'name' : 'LND_DIAG', 'url' : url, 'children' : children_arr }
    data_string = json.dumps(data,sort_keys=True,indent=2)
    print 'JSON:',data_string
    '''
    
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

   dataset = os.path.join(default_sample_data_dir, 'test.xml')

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








'''
'username' : username,
'cachedfile' : cached_file_name,
'variable_list' : variable_list,
'season_list' : season_list,
'bookmark_list' : bookmark_list,
'figure_bookmark_list' : figure_bookmark_list,
'treefile': treeFile,
'current_bookmark': bookmark
#'treeFile' : treeFile,
'''
    
'''
package_list = ['lmwg']
    
#get the dataset_list from ESGF
dataset_list = ['tropics_warming_th_q_co2']    

#get the variable list here using Brian's code 
#variable_list = ['ACTUAL_IMMOB', 'AGNPP', 'ANN_FAREA_BURNED', 'AR', 'BCDEP', 'BGNPP', 'BIOGENCO', 'BSW', 'BTRAN', 'BUILDHEAT', 'COL_CTRUNC', 'COL_FIRE_CLOSS', 'COL_FIRE_NLOSS', 'COL_NTRUNC', 'CPOOL', 'CWDC', 'CWDC_HR', 'CWDC_LOSS', 'CWDN', 'DEADCROOTC', 'DEADCROOTN', 'DEADSTEMC', 'DEADSTEMN', 'DENIT', 'DISPVEGC', 'DISPVEGN', 'DSTDEP', 'DSTFLXT', 'DWT_CLOSS', 'DWT_CONV_CFLUX', 'DWT_CONV_NFLUX', 'DWT_NLOSS', 'DWT_PROD100C_GAIN', 'DWT_PROD100N_GAIN', 'DWT_PROD10C_GAIN', 'DWT_PROD10N_GAIN', 'DWT_SEEDC_TO_DEADSTEM', 'DWT_SEEDC_TO_LEAF', 'DWT_SEEDN_TO_DEADSTEM', 'DWT_SEEDN_TO_LEAF', 'DZSOI', 'E-T', 'EFLX_DYNBAL', 'EFLX_LH_TOT_R', 'EFLX_LH_TOT_U', 'ELAI', 'ER', 'ERRH2O', 'ERRSEB', 'ERRSOI', 'ERRSOL', 'ESAI', 'EVAPFRAC', 'FCEV', 'FCOV', 'FCTR', 'FGEV', 'FGR', 'FGR12', 'FGR_R', 'FGR_U', 'FIRA', 'FIRA_R', 'FIRA_U', 'FIRE', 'FIRESEASONL', 'FLDS', 'FLUXFM2A', 'FLUXFMLND', 'FPG', 'FPI', 'FPSN', 'FROOTC', 'FROOTC_ALLOC', 'FROOTC_LOSS', 'FROOTN', 'FSA', 'FSAT', 'FSA_R', 'FSA_U', 'FSDS', 'FSDSND', 'FSDSNDLN', 'FSDSNI', 'FSDSVD', 'FSDSVDLN', 'FSDSVI', 'FSH', 'FSH_G', 'FSH_NODYNLNDUSE', 'FSH_R', 'FSH_U', 'FSH_V', 'FSM', 'FSM_R', 'FSM_U', 'FSNO', 'FSR', 'FSRND', 'FSRNDLN', 'FSRNI', 'FSRVD', 'FSRVDLN', 'FSRVI', 'GC_HEAT1', 'GC_ICE1', 'GC_LIQ1', 'GPP', 'GR', 'GROSS_NMIN', 'H2OCAN', 'H2OSNO', 'H2OSNO_TOP', 'H2OSOI', 'HC', 'HCSOI', 'HEAT_FROM_AC', 'HKSAT', 'HR', 'HTOP', 'ISOPRENE', 'LAISHA', 'LAISUN', 'LAND_UPTAKE', 'LAND_USE_FLUX', 'LEAFC', 'LEAFC_ALLOC', 'LEAFC_LOSS', 'LEAFN', 'LHEAT', 'LITFALL', 'LITHR', 'LITR1C', 'LITR1C_TO_SOIL1C', 'LITR1N', 'LITR2C', 'LITR2C_TO_SOIL2C', 'LITR2N', 'LITR3C', 'LITR3C_TO_SOIL3C', 'LITR3N', 'LITTERC', 'LITTERC_HR', 'LITTERC_LOSS', 'LIVECROOTC', 'LIVECROOTN', 'LIVESTEMC', 'LIVESTEMN', 'MEAN_FIRE_PROB', 'MONOTERP', 'MR', 'NBP', 'NDEPLOY', 'NDEP_TO_SMINN', 'NEE', 'NEP', 'NET_NMIN', 'NFIX_TO_SMINN', 'NPP', 'OCDEP', 'ORVOC', 'OVOC', 'PBOT', 'PCO2', 'PFT_CTRUNC', 'PFT_FIRE_CLOSS', 'PFT_FIRE_NLOSS', 'PFT_NTRUNC', 'PLANT_NDEMAND', 'POTENTIAL_IMMOB', 'PREC', 'PROD100C', 'PROD100C_LOSS', 'PROD100N', 'PROD100N_LOSS', 'PROD10C', 'PROD10C_LOSS', 'PROD10N', 'PROD10N_LOSS', 'PRODUCT_CLOSS', 'PRODUCT_NLOSS', 'PSNSHA', 'PSNSHADE_TO_CPOOL', 'PSNSUN', 'PSNSUN_TO_CPOOL', 'Q2M', 'QBOT', 'QCHANR', 'QCHANR_ICE', 'QCHARGE', 'QCHOCNR', 'QCHOCNR_ICE', 'QDRAI', 'QDRIP', 'QFLX_ICE_DYNBAL', 'QFLX_LIQ_DYNBAL', 'QINFL', 'QINTR', 'QMELT', 'QOVER', 'QRGWL', 'QRUNOFF', 'QRUNOFF_NODYNLNDUSE', 'QRUNOFF_R', 'QRUNOFF_U', 'QSNWCPICE', 'QSNWCPICE_NODYNLNDUSE', 'QSOIL', 'QVEGE', 'QVEGT', 'RAIN', 'RAINATM', 'RAINFM2A', 'RETRANSN', 'RETRANSN_TO_NPOOL', 'RH2M', 'RH2M_R', 'RH2M_U', 'RR', 'SABG', 'SABV', 'SEEDC', 'SEEDN', 'SHEAT', 'SMINN', 'SMINN_LEACHED', 'SMINN_TO_NPOOL', 'SMINN_TO_PLANT', 'SNOBCMCL', 'SNOBCMSL', 'SNODSTMCL', 'SNODSTMSL', 'SNOOCMCL', 'SNOOCMSL', 'SNOW', 'SNOWATM', 'SNOWDP', 'SNOWFM2A', 'SNOWICE', 'SNOWLIQ', 'SOIL1C', 'SOIL1N', 'SOIL2C', 'SOIL2N', 'SOIL3C', 'SOIL3N', 'SOIL4C', 'SOIL4N', 'SOILC', 'SOILC_HR', 'SOILC_LOSS', 'SOILICE', 'SOILLIQ', 'SOILPSI', 'SOILWATER_10CM', 'SOMHR', 'SR', 'STORVEGC', 'STORVEGN', 'SUCSAT', 'SUPPLEMENT_TO_SMINN', 'SoilAlpha', 'SoilAlpha_U', 'TAUX', 'TAUY', 'TBOT', 'TBUILD', 'TG', 'TG_R', 'TG_U', 'THBOT', 'TLAI', 'TLAKE', 'TOTCOLC', 'TOTCOLN', 'TOTECOSYSC', 'TOTECOSYSN', 'TOTLITC', 'TOTLITN', 'TOTPFTC', 'TOTPFTN', 'TOTPRODC', 'TOTPRODN', 'TOTSOMC', 'TOTSOMN', 'TOTVEGC', 'TOTVEGN', 'TREFMNAV', 'TREFMNAV_R', 'TREFMNAV_U', 'TREFMXAV', 'TREFMXAV_R', 'TREFMXAV_U', 'TSA', 'TSAI', 'TSA_R', 'TSA_U', 'TSOI', 'TSOI_10CM', 'TV', 'U10', 'URBAN_AC', 'URBAN_HEAT', 'VOCFLXT', 'VOLR', 'WA', 'WASTEHEAT', 'WATSAT', 'WIND', 'WOODC', 'WOODC_ALLOC', 'WOODC_LOSS', 'WOOD_HARVESTC', 'WOOD_HARVESTN', 'WT', 'XSMRPOOL', 'XSMRPOOL_RECOVER', 'ZBOT', 'ZSOI', 'ZWT', 'area', 'areaatm', 'areaupsc', 'date_written', 'edgee', 'edgen', 'edges', 'edgew', 'indxupsc', 'landfrac', 'landmask', 'latixy', 'latixyatm', 'longxy', 'longxyatm', 'mcdate', 'mcsec', 'mdcur', 'mscur', 'nstep', 'pftmask', 'time_bounds', 'time_written', 'topo', 'topodnsc']
variable_list = ['GPP','NEE','HR','ER','NPP','QVEGT','QVEGE','QSOIL','GROSS_NMIN']


#get the season list here using Brian's code
season_list = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC','DJF','MAM','JJA','SON','ANN']


set_list = ['set1','set2','set3','set4','set5','set6','set7','set8','set9']

#if this is a submission for a new tree
#request.GET.get('variable')
'''




'''
#options for creating a new tree
package_list = ['lmwg']
    
#get the dataset_list from ESGF
dataset_list = ['tropics_warming_th_q_co2']    


#get the variable list here using Brian's code 
#variable_list = ['ACTUAL_IMMOB', 'AGNPP', 'ANN_FAREA_BURNED', 'AR', 'BCDEP', 'BGNPP', 'BIOGENCO', 'BSW', 'BTRAN', 'BUILDHEAT', 'COL_CTRUNC', 'COL_FIRE_CLOSS', 'COL_FIRE_NLOSS', 'COL_NTRUNC', 'CPOOL', 'CWDC', 'CWDC_HR', 'CWDC_LOSS', 'CWDN', 'DEADCROOTC', 'DEADCROOTN', 'DEADSTEMC', 'DEADSTEMN', 'DENIT', 'DISPVEGC', 'DISPVEGN', 'DSTDEP', 'DSTFLXT', 'DWT_CLOSS', 'DWT_CONV_CFLUX', 'DWT_CONV_NFLUX', 'DWT_NLOSS', 'DWT_PROD100C_GAIN', 'DWT_PROD100N_GAIN', 'DWT_PROD10C_GAIN', 'DWT_PROD10N_GAIN', 'DWT_SEEDC_TO_DEADSTEM', 'DWT_SEEDC_TO_LEAF', 'DWT_SEEDN_TO_DEADSTEM', 'DWT_SEEDN_TO_LEAF', 'DZSOI', 'E-T', 'EFLX_DYNBAL', 'EFLX_LH_TOT_R', 'EFLX_LH_TOT_U', 'ELAI', 'ER', 'ERRH2O', 'ERRSEB', 'ERRSOI', 'ERRSOL', 'ESAI', 'EVAPFRAC', 'FCEV', 'FCOV', 'FCTR', 'FGEV', 'FGR', 'FGR12', 'FGR_R', 'FGR_U', 'FIRA', 'FIRA_R', 'FIRA_U', 'FIRE', 'FIRESEASONL', 'FLDS', 'FLUXFM2A', 'FLUXFMLND', 'FPG', 'FPI', 'FPSN', 'FROOTC', 'FROOTC_ALLOC', 'FROOTC_LOSS', 'FROOTN', 'FSA', 'FSAT', 'FSA_R', 'FSA_U', 'FSDS', 'FSDSND', 'FSDSNDLN', 'FSDSNI', 'FSDSVD', 'FSDSVDLN', 'FSDSVI', 'FSH', 'FSH_G', 'FSH_NODYNLNDUSE', 'FSH_R', 'FSH_U', 'FSH_V', 'FSM', 'FSM_R', 'FSM_U', 'FSNO', 'FSR', 'FSRND', 'FSRNDLN', 'FSRNI', 'FSRVD', 'FSRVDLN', 'FSRVI', 'GC_HEAT1', 'GC_ICE1', 'GC_LIQ1', 'GPP', 'GR', 'GROSS_NMIN', 'H2OCAN', 'H2OSNO', 'H2OSNO_TOP', 'H2OSOI', 'HC', 'HCSOI', 'HEAT_FROM_AC', 'HKSAT', 'HR', 'HTOP', 'ISOPRENE', 'LAISHA', 'LAISUN', 'LAND_UPTAKE', 'LAND_USE_FLUX', 'LEAFC', 'LEAFC_ALLOC', 'LEAFC_LOSS', 'LEAFN', 'LHEAT', 'LITFALL', 'LITHR', 'LITR1C', 'LITR1C_TO_SOIL1C', 'LITR1N', 'LITR2C', 'LITR2C_TO_SOIL2C', 'LITR2N', 'LITR3C', 'LITR3C_TO_SOIL3C', 'LITR3N', 'LITTERC', 'LITTERC_HR', 'LITTERC_LOSS', 'LIVECROOTC', 'LIVECROOTN', 'LIVESTEMC', 'LIVESTEMN', 'MEAN_FIRE_PROB', 'MONOTERP', 'MR', 'NBP', 'NDEPLOY', 'NDEP_TO_SMINN', 'NEE', 'NEP', 'NET_NMIN', 'NFIX_TO_SMINN', 'NPP', 'OCDEP', 'ORVOC', 'OVOC', 'PBOT', 'PCO2', 'PFT_CTRUNC', 'PFT_FIRE_CLOSS', 'PFT_FIRE_NLOSS', 'PFT_NTRUNC', 'PLANT_NDEMAND', 'POTENTIAL_IMMOB', 'PREC', 'PROD100C', 'PROD100C_LOSS', 'PROD100N', 'PROD100N_LOSS', 'PROD10C', 'PROD10C_LOSS', 'PROD10N', 'PROD10N_LOSS', 'PRODUCT_CLOSS', 'PRODUCT_NLOSS', 'PSNSHA', 'PSNSHADE_TO_CPOOL', 'PSNSUN', 'PSNSUN_TO_CPOOL', 'Q2M', 'QBOT', 'QCHANR', 'QCHANR_ICE', 'QCHARGE', 'QCHOCNR', 'QCHOCNR_ICE', 'QDRAI', 'QDRIP', 'QFLX_ICE_DYNBAL', 'QFLX_LIQ_DYNBAL', 'QINFL', 'QINTR', 'QMELT', 'QOVER', 'QRGWL', 'QRUNOFF', 'QRUNOFF_NODYNLNDUSE', 'QRUNOFF_R', 'QRUNOFF_U', 'QSNWCPICE', 'QSNWCPICE_NODYNLNDUSE', 'QSOIL', 'QVEGE', 'QVEGT', 'RAIN', 'RAINATM', 'RAINFM2A', 'RETRANSN', 'RETRANSN_TO_NPOOL', 'RH2M', 'RH2M_R', 'RH2M_U', 'RR', 'SABG', 'SABV', 'SEEDC', 'SEEDN', 'SHEAT', 'SMINN', 'SMINN_LEACHED', 'SMINN_TO_NPOOL', 'SMINN_TO_PLANT', 'SNOBCMCL', 'SNOBCMSL', 'SNODSTMCL', 'SNODSTMSL', 'SNOOCMCL', 'SNOOCMSL', 'SNOW', 'SNOWATM', 'SNOWDP', 'SNOWFM2A', 'SNOWICE', 'SNOWLIQ', 'SOIL1C', 'SOIL1N', 'SOIL2C', 'SOIL2N', 'SOIL3C', 'SOIL3N', 'SOIL4C', 'SOIL4N', 'SOILC', 'SOILC_HR', 'SOILC_LOSS', 'SOILICE', 'SOILLIQ', 'SOILPSI', 'SOILWATER_10CM', 'SOMHR', 'SR', 'STORVEGC', 'STORVEGN', 'SUCSAT', 'SUPPLEMENT_TO_SMINN', 'SoilAlpha', 'SoilAlpha_U', 'TAUX', 'TAUY', 'TBOT', 'TBUILD', 'TG', 'TG_R', 'TG_U', 'THBOT', 'TLAI', 'TLAKE', 'TOTCOLC', 'TOTCOLN', 'TOTECOSYSC', 'TOTECOSYSN', 'TOTLITC', 'TOTLITN', 'TOTPFTC', 'TOTPFTN', 'TOTPRODC', 'TOTPRODN', 'TOTSOMC', 'TOTSOMN', 'TOTVEGC', 'TOTVEGN', 'TREFMNAV', 'TREFMNAV_R', 'TREFMNAV_U', 'TREFMXAV', 'TREFMXAV_R', 'TREFMXAV_U', 'TSA', 'TSAI', 'TSA_R', 'TSA_U', 'TSOI', 'TSOI_10CM', 'TV', 'U10', 'URBAN_AC', 'URBAN_HEAT', 'VOCFLXT', 'VOLR', 'WA', 'WASTEHEAT', 'WATSAT', 'WIND', 'WOODC', 'WOODC_ALLOC', 'WOODC_LOSS', 'WOOD_HARVESTC', 'WOOD_HARVESTN', 'WT', 'XSMRPOOL', 'XSMRPOOL_RECOVER', 'ZBOT', 'ZSOI', 'ZWT', 'area', 'areaatm', 'areaupsc', 'date_written', 'edgee', 'edgen', 'edges', 'edgew', 'indxupsc', 'landfrac', 'landmask', 'latixy', 'latixyatm', 'longxy', 'longxyatm', 'mcdate', 'mcsec', 'mdcur', 'mscur', 'nstep', 'pftmask', 'time_bounds', 'time_written', 'topo', 'topodnsc']
variable_list = ['GPP','NEE','HR','ER','NPP','QVEGT','QVEGE','QSOIL','GROSS_NMIN']

#get the season list here using Brian's code
season_list = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC','DJF','MAM','JJA','SON','ANN']


set_list = ['set1','set2','set3','set4','set5','set6','set7','set8','set9']
'''


