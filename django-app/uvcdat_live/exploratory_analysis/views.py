#flag for toggling connection to the diags backend
isConnected = True

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
#from exploratory_analysis.models import Diags
import json
import sys 

from paths import paths


syspath_append_uvcmetrics = paths.syspath_append_uvcmetrics
syspath_append_cdscan = paths.syspath_append_cdscan

paths_cache_dir = paths.cache_dir
paths_front_end_cache_dir = paths.front_end_cache_dir

default_sample_data_dir = paths.default_sample_data_dir
img_cache_path = paths.img_cache_path

timeseries_cache_path = paths.timeseries_cache_path

# import the diags code
if isConnected:
    #sys.path.append('/Users/8xo/software/exploratory_analysis/DiagnosticsGen/uvcmetrics/src/python')
    #sys.path.append('/Users/8xo/software/exploratory_analysis/uvcdat_light/build-uvcdat/install/Library/Frameworks/Python.framework/Versions/2.7/bin/cdscan')
    sys.path.append(syspath_append_uvcmetrics)
    sys.path.append(syspath_append_cdscan)
   
    from frontend.options import Options
    from computation.reductions import *
    from fileio.filetable import *
    from fileio.findfiles import *

    from frontend.treeview import TreeView 

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




#New tree view
def treeex(request,user_id):
    
    username = 'jfharney'
    
    #grab the username
    if user_id != None:
        username = user_id
    
    
    
    #first we check if the request is in the cache or if it is the initial call
    #if it is in the cache, no need to do any back end generation
    
    bookmark = request.GET.get('bookmark')
    
    
    if bookmark == None:
        print 'it is not in the cache'
        
        #use the input from the user
        realms = ['lmwg']
        variables = ['TG']
        path = default_sample_data_dir#'/Users/8xo/sampledatalens/tropics_warming_th_q_co2'
        times = ['JAN','FEB']
        
        bookmark = "New"
        

        


    
    elif bookmark=='new':
        print 'page reached for the first time'
        #dont load anything yet
        
    else:
        print 'it is in the cache'
        
        # grab the various parameters from the db concerning this bookmark given the bookmark name
        
        #hardcoded - convert to db calls 
        if bookmark == 'Bookmark1':
            print 'Bookmark1'
            
            
            
            
        elif bookmark == 'Bookmark2':
            print 'Bookmark2'
            
            
        else:
            print 'other bookmark'
            bookmark = 'New'
        
        
        
        
    
    
    
    if isConnected:
        #use 
        print 'use the diags'
    else:
        print 'use the sample file with the hard coded data'   
     
    
    
    #diagsHelper(user_id)
    
    
    fileName = bookmark + ".json"
    
    cached_file_name = front_end_cache_dir + fileName
           
            
    template = loader.get_template('exploratory_analysis/treeex.html')
    
    
    #get the variable list here using Brian's code 
    variable_list = ['ACTUAL_IMMOB', 'AGNPP', 'ANN_FAREA_BURNED', 'AR', 'BCDEP', 'BGNPP', 'BIOGENCO', 'BSW', 'BTRAN', 'BUILDHEAT', 'COL_CTRUNC', 'COL_FIRE_CLOSS', 'COL_FIRE_NLOSS', 'COL_NTRUNC', 'CPOOL', 'CWDC', 'CWDC_HR', 'CWDC_LOSS', 'CWDN', 'DEADCROOTC', 'DEADCROOTN', 'DEADSTEMC', 'DEADSTEMN', 'DENIT', 'DISPVEGC', 'DISPVEGN', 'DSTDEP', 'DSTFLXT', 'DWT_CLOSS', 'DWT_CONV_CFLUX', 'DWT_CONV_NFLUX', 'DWT_NLOSS', 'DWT_PROD100C_GAIN', 'DWT_PROD100N_GAIN', 'DWT_PROD10C_GAIN', 'DWT_PROD10N_GAIN', 'DWT_SEEDC_TO_DEADSTEM', 'DWT_SEEDC_TO_LEAF', 'DWT_SEEDN_TO_DEADSTEM', 'DWT_SEEDN_TO_LEAF', 'DZSOI', 'E-T', 'EFLX_DYNBAL', 'EFLX_LH_TOT_R', 'EFLX_LH_TOT_U', 'ELAI', 'ER', 'ERRH2O', 'ERRSEB', 'ERRSOI', 'ERRSOL', 'ESAI', 'EVAPFRAC', 'FCEV', 'FCOV', 'FCTR', 'FGEV', 'FGR', 'FGR12', 'FGR_R', 'FGR_U', 'FIRA', 'FIRA_R', 'FIRA_U', 'FIRE', 'FIRESEASONL', 'FLDS', 'FLUXFM2A', 'FLUXFMLND', 'FPG', 'FPI', 'FPSN', 'FROOTC', 'FROOTC_ALLOC', 'FROOTC_LOSS', 'FROOTN', 'FSA', 'FSAT', 'FSA_R', 'FSA_U', 'FSDS', 'FSDSND', 'FSDSNDLN', 'FSDSNI', 'FSDSVD', 'FSDSVDLN', 'FSDSVI', 'FSH', 'FSH_G', 'FSH_NODYNLNDUSE', 'FSH_R', 'FSH_U', 'FSH_V', 'FSM', 'FSM_R', 'FSM_U', 'FSNO', 'FSR', 'FSRND', 'FSRNDLN', 'FSRNI', 'FSRVD', 'FSRVDLN', 'FSRVI', 'GC_HEAT1', 'GC_ICE1', 'GC_LIQ1', 'GPP', 'GR', 'GROSS_NMIN', 'H2OCAN', 'H2OSNO', 'H2OSNO_TOP', 'H2OSOI', 'HC', 'HCSOI', 'HEAT_FROM_AC', 'HKSAT', 'HR', 'HTOP', 'ISOPRENE', 'LAISHA', 'LAISUN', 'LAND_UPTAKE', 'LAND_USE_FLUX', 'LEAFC', 'LEAFC_ALLOC', 'LEAFC_LOSS', 'LEAFN', 'LHEAT', 'LITFALL', 'LITHR', 'LITR1C', 'LITR1C_TO_SOIL1C', 'LITR1N', 'LITR2C', 'LITR2C_TO_SOIL2C', 'LITR2N', 'LITR3C', 'LITR3C_TO_SOIL3C', 'LITR3N', 'LITTERC', 'LITTERC_HR', 'LITTERC_LOSS', 'LIVECROOTC', 'LIVECROOTN', 'LIVESTEMC', 'LIVESTEMN', 'MEAN_FIRE_PROB', 'MONOTERP', 'MR', 'NBP', 'NDEPLOY', 'NDEP_TO_SMINN', 'NEE', 'NEP', 'NET_NMIN', 'NFIX_TO_SMINN', 'NPP', 'OCDEP', 'ORVOC', 'OVOC', 'PBOT', 'PCO2', 'PFT_CTRUNC', 'PFT_FIRE_CLOSS', 'PFT_FIRE_NLOSS', 'PFT_NTRUNC', 'PLANT_NDEMAND', 'POTENTIAL_IMMOB', 'PREC', 'PROD100C', 'PROD100C_LOSS', 'PROD100N', 'PROD100N_LOSS', 'PROD10C', 'PROD10C_LOSS', 'PROD10N', 'PROD10N_LOSS', 'PRODUCT_CLOSS', 'PRODUCT_NLOSS', 'PSNSHA', 'PSNSHADE_TO_CPOOL', 'PSNSUN', 'PSNSUN_TO_CPOOL', 'Q2M', 'QBOT', 'QCHANR', 'QCHANR_ICE', 'QCHARGE', 'QCHOCNR', 'QCHOCNR_ICE', 'QDRAI', 'QDRIP', 'QFLX_ICE_DYNBAL', 'QFLX_LIQ_DYNBAL', 'QINFL', 'QINTR', 'QMELT', 'QOVER', 'QRGWL', 'QRUNOFF', 'QRUNOFF_NODYNLNDUSE', 'QRUNOFF_R', 'QRUNOFF_U', 'QSNWCPICE', 'QSNWCPICE_NODYNLNDUSE', 'QSOIL', 'QVEGE', 'QVEGT', 'RAIN', 'RAINATM', 'RAINFM2A', 'RETRANSN', 'RETRANSN_TO_NPOOL', 'RH2M', 'RH2M_R', 'RH2M_U', 'RR', 'SABG', 'SABV', 'SEEDC', 'SEEDN', 'SHEAT', 'SMINN', 'SMINN_LEACHED', 'SMINN_TO_NPOOL', 'SMINN_TO_PLANT', 'SNOBCMCL', 'SNOBCMSL', 'SNODSTMCL', 'SNODSTMSL', 'SNOOCMCL', 'SNOOCMSL', 'SNOW', 'SNOWATM', 'SNOWDP', 'SNOWFM2A', 'SNOWICE', 'SNOWLIQ', 'SOIL1C', 'SOIL1N', 'SOIL2C', 'SOIL2N', 'SOIL3C', 'SOIL3N', 'SOIL4C', 'SOIL4N', 'SOILC', 'SOILC_HR', 'SOILC_LOSS', 'SOILICE', 'SOILLIQ', 'SOILPSI', 'SOILWATER_10CM', 'SOMHR', 'SR', 'STORVEGC', 'STORVEGN', 'SUCSAT', 'SUPPLEMENT_TO_SMINN', 'SoilAlpha', 'SoilAlpha_U', 'TAUX', 'TAUY', 'TBOT', 'TBUILD', 'TG', 'TG_R', 'TG_U', 'THBOT', 'TLAI', 'TLAKE', 'TOTCOLC', 'TOTCOLN', 'TOTECOSYSC', 'TOTECOSYSN', 'TOTLITC', 'TOTLITN', 'TOTPFTC', 'TOTPFTN', 'TOTPRODC', 'TOTPRODN', 'TOTSOMC', 'TOTSOMN', 'TOTVEGC', 'TOTVEGN', 'TREFMNAV', 'TREFMNAV_R', 'TREFMNAV_U', 'TREFMXAV', 'TREFMXAV_R', 'TREFMXAV_U', 'TSA', 'TSAI', 'TSA_R', 'TSA_U', 'TSOI', 'TSOI_10CM', 'TV', 'U10', 'URBAN_AC', 'URBAN_HEAT', 'VOCFLXT', 'VOLR', 'WA', 'WASTEHEAT', 'WATSAT', 'WIND', 'WOODC', 'WOODC_ALLOC', 'WOODC_LOSS', 'WOOD_HARVESTC', 'WOOD_HARVESTN', 'WT', 'XSMRPOOL', 'XSMRPOOL_RECOVER', 'ZBOT', 'ZSOI', 'ZWT', 'area', 'areaatm', 'areaupsc', 'date_written', 'edgee', 'edgen', 'edges', 'edgew', 'indxupsc', 'landfrac', 'landmask', 'latixy', 'latixyatm', 'longxy', 'longxyatm', 'mcdate', 'mcsec', 'mdcur', 'mscur', 'nstep', 'pftmask', 'time_bounds', 'time_written', 'topo', 'topodnsc']
    
    #get the season list here using Brian's code
    season_list = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC','DJF','MAM','JJA','SON','ANN']

    '''
    #get the bookmarks of the user
    from exploratory_analysis.models import Tree_Bookmarks
    bookmark_list = Tree_Bookmarks.objects.filter(bookmark_username='jfharney')
    ''' 
    bookmark_list = None
    if bookmark_list == None:
        bookmark_list = ['bookmark1','bookmark2','bookmark3']
    
    
    print 'flag: ' + str(bookmark_list == None) + ' ' + str(bookmark_list == [])
    
    print  'str: '  + str(len(bookmark_list))
    
    #for key in bookmark_list:
    #    print 'key: ' + key + ' ' + bookmark_list[key]
    
    
    if not bookmark_list:#str(len(bookmark_list)) == 0:
        bookmark_list = ['b1','b2','b3']
    
    figure_bookmark_list = None
    '''
    #get the figure bookmarks of the user
    #query the database using username, figure bookmark name
    from exploratory_analysis.models import Figure_Bookmarks
    figure_bookmark_list = Figure_Bookmarks.objects.filter(figure_bookmark_username='jfharney')
    '''
    if figure_bookmark_list == None:
        figure_bookmark_list = ['figure1','figure2','figure3']
    
    #pass all the data back to the view
    context = RequestContext(request, {
        'username' : username,
        'cachedfile' : cached_file_name,
        'variable_list' : variable_list,
        'season_list' : season_list,
        'bookmark_list' : bookmark_list,
        'figure_bookmark_list' : figure_bookmark_list
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

  file = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/css/tree/flare3.json';
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
 


  
  #grabs the timeseries data
  #http://<host>/exploratory_analysis/timeseries
def timeseries(request):
    
    print ' ... in time series ...'
    
    from mapviewhelper import timeseries

    #timeseries_cache_path = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache'
    
    jsonData = timeseries.timeSeriesHelper1(request,timeseries_cache_path)
    
    print ' ... end in time series ...'
    
    return HttpResponse(jsonData) 
  
  
  
  
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




def diagsHelper(user_id):
    print 'in diags helper'
    
    
    treeFile = cache_dir + 'Bookmark2.json'
    
    
    #### Start diagnostics generation here...
    username = user_id
  
    print username
    
    o = Options()
    #   o.processCmdLine()
    #   o.verifyOptions()
   
   ##### SET THESE BASED ON USER INPUT FROM THE GUI
    o._opts['packages'] = ['lmwg'] 
    o._opts['vars'] = ['TLAI', 'TG']
    o._opts['path'] = [default_sample_data_dir]
    o._opts['times'] = ['MAR','APR','MAY']
    
    
    ### NOTE: 'ANN' won't work for times this way, but that shouldn't be a problem
    datafiles = []
    filetables = []
    vars = o._opts['vars']
    #   print vars

    
    index = 0
    for p in o._opts['path']:
      print '\ndirtree\n' , dirtree_datafiles(p)
      datafiles.append(dirtree_datafiles(p))
      filetables.append(basic_filetable(datafiles[index], o))
      index = index+1

    print 'Creating diags tree view JSON file...'
    
    
    
    tv = TreeView()
    dtree = tv.makeTree(o, filetables,None,user=username,ftnames=['tropics_warming_th_q_co2'])
    tv.dump(filename=treeFile)
    '''
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
    







def tree(request):
    template = loader.get_template('exploratory_analysis/treeview.html')
    #template = loader.get_template('exploratory_analysis/tree.html')
    
    context = RequestContext(request, {
        'username' : 'jfharney',
    })
    
    return HttpResponse(template.render(context))
 
  
  
 
def treedataBrian(request,user_id):
    
    username = user_id
  
    o = Options()
    #   o.processCmdLine()
    #   o.verifyOptions()
   
   ##### SET THESE BASED ON USER INPUT FROM THE GUI
    o._opts['packages'] = ['lmwg'] 
    o._opts['vars'] = ['TG']
    o._opts['path'] = [default_sample_data_dir]
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
http://
'''
def visualizationsBrian(request):
    
   print 'in visualizations Brian'
   
   o = Options()
#   o.processCmdLine()
#   o.verifyOptions()

   ##### SET THESE BASED ON USER INPUT FROM THE GUI
   o._opts['vars'] = ['PBOT'] 
  # o._opts['path'] = ['/path/to/a/dataset'] 
   o._opts['path'] = [default_sample_data_dir] 
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
    
    from exploratory_analysis.models import Tree_Bookmarks, Figure_Bookmarks
    
    tree_bookmark_name = None
    tree_bookmark_datasetname = None
    tree_bookmark_realm = None
    tree_bookmark_username = None
    tree_bookmark_variables = None
    tree_bookmark_times = None
    tree_bookmark_sets = None
    tree_bookmark_description = None
    tree_cache_url = None
    
    if request.method == 'POST':
        
        tree_bookmark_name = request.POST['tree_bookmark_name']
        tree_bookmark_datasetname = request.POST['tree_bookmark_datasetname']
        tree_bookmark_realm = request.POST['tree_bookmark_realm']
        tree_bookmark_username = request.POST['tree_bookmark_username']
        tree_bookmark_variables = request.POST['tree_bookmark_variables']
        tree_bookmark_times = request.POST['tree_bookmark_times']
        tree_bookmark_sets = request.POST['tree_bookmark_sets']
        tree_bookmark_description = request.POST['tree_bookmark_description']
        tree_cache_url = request.POST['tree_cache_url']
        
        tree_bookmark_record = Tree_Bookmarks()
        
        
        print 'POST'
        
        
        
    elif request.method == 'GET':
        print 'GET'
    elif request.method == 'DELETE':
        print 'DELETE'
    
    
    return HttpResponse()
    '''
    username = None
    bookmark_name = None
    bookmark_variables = None
    bookmark_time_periods = None
    bookmark_description = None
    
    
    print 'in tree bookmarks'
    if request.method == 'POST':
        print 'POST'
        
        #grab the user's name
        #default username: jfharney
        if username == None:
            print 'using default username'
            username = 'jfharney'
        
        #grab the bookmark name
        #default bookmark: bookmark + currentmillitime
        if bookmark_name == None:
            import time
            print 'tme ' + str(time.time())
            millis = int(round(time.time()*1000))
            print 'millis' + str(millis)
            bookmark_name = 'bookmark' + str(millis)
            print 'using default bookmark name ' + bookmark_name
        
        
        #grab the bookmark variables
        #default figure: ../../../static/exploratory_analysis/cache/carousel/set6_turbf_Global.gif
        if bookmark_variables == None:
            print 'using default bookmark_variables'
            variable_list = ['ACTUAL_IMMOB', 'AGNPP', 'ANN_FAREA_BURNED', 'AR', 'BCDEP', 'BGNPP', 'BIOGENCO', 'BSW', 'BTRAN', 'BUILDHEAT', 'COL_CTRUNC', 'COL_FIRE_CLOSS', 'COL_FIRE_NLOSS', 'COL_NTRUNC', 'CPOOL', 'CWDC', 'CWDC_HR', 'CWDC_LOSS', 'CWDN', 'DEADCROOTC', 'DEADCROOTN', 'DEADSTEMC', 'DEADSTEMN', 'DENIT', 'DISPVEGC', 'DISPVEGN', 'DSTDEP', 'DSTFLXT', 'DWT_CLOSS', 'DWT_CONV_CFLUX', 'DWT_CONV_NFLUX', 'DWT_NLOSS', 'DWT_PROD100C_GAIN', 'DWT_PROD100N_GAIN', 'DWT_PROD10C_GAIN', 'DWT_PROD10N_GAIN', 'DWT_SEEDC_TO_DEADSTEM', 'DWT_SEEDC_TO_LEAF', 'DWT_SEEDN_TO_DEADSTEM', 'DWT_SEEDN_TO_LEAF', 'DZSOI', 'E-T', 'EFLX_DYNBAL', 'EFLX_LH_TOT_R', 'EFLX_LH_TOT_U', 'ELAI', 'ER', 'ERRH2O', 'ERRSEB', 'ERRSOI', 'ERRSOL', 'ESAI', 'EVAPFRAC', 'FCEV', 'FCOV', 'FCTR', 'FGEV', 'FGR', 'FGR12', 'FGR_R', 'FGR_U', 'FIRA', 'FIRA_R', 'FIRA_U', 'FIRE', 'FIRESEASONL', 'FLDS', 'FLUXFM2A', 'FLUXFMLND', 'FPG', 'FPI', 'FPSN', 'FROOTC', 'FROOTC_ALLOC', 'FROOTC_LOSS', 'FROOTN', 'FSA', 'FSAT', 'FSA_R', 'FSA_U', 'FSDS', 'FSDSND', 'FSDSNDLN', 'FSDSNI', 'FSDSVD', 'FSDSVDLN', 'FSDSVI', 'FSH', 'FSH_G', 'FSH_NODYNLNDUSE', 'FSH_R', 'FSH_U', 'FSH_V', 'FSM', 'FSM_R', 'FSM_U', 'FSNO', 'FSR', 'FSRND', 'FSRNDLN', 'FSRNI', 'FSRVD', 'FSRVDLN', 'FSRVI', 'GC_HEAT1', 'GC_ICE1', 'GC_LIQ1', 'GPP', 'GR', 'GROSS_NMIN', 'H2OCAN', 'H2OSNO', 'H2OSNO_TOP', 'H2OSOI', 'HC', 'HCSOI', 'HEAT_FROM_AC', 'HKSAT', 'HR', 'HTOP', 'ISOPRENE', 'LAISHA', 'LAISUN', 'LAND_UPTAKE', 'LAND_USE_FLUX', 'LEAFC', 'LEAFC_ALLOC', 'LEAFC_LOSS', 'LEAFN', 'LHEAT', 'LITFALL', 'LITHR', 'LITR1C', 'LITR1C_TO_SOIL1C', 'LITR1N', 'LITR2C', 'LITR2C_TO_SOIL2C', 'LITR2N', 'LITR3C', 'LITR3C_TO_SOIL3C', 'LITR3N', 'LITTERC', 'LITTERC_HR', 'LITTERC_LOSS', 'LIVECROOTC', 'LIVECROOTN', 'LIVESTEMC', 'LIVESTEMN', 'MEAN_FIRE_PROB', 'MONOTERP', 'MR', 'NBP', 'NDEPLOY', 'NDEP_TO_SMINN', 'NEE', 'NEP', 'NET_NMIN', 'NFIX_TO_SMINN', 'NPP', 'OCDEP', 'ORVOC', 'OVOC', 'PBOT', 'PCO2', 'PFT_CTRUNC', 'PFT_FIRE_CLOSS', 'PFT_FIRE_NLOSS', 'PFT_NTRUNC', 'PLANT_NDEMAND', 'POTENTIAL_IMMOB', 'PREC', 'PROD100C', 'PROD100C_LOSS', 'PROD100N', 'PROD100N_LOSS', 'PROD10C', 'PROD10C_LOSS', 'PROD10N', 'PROD10N_LOSS', 'PRODUCT_CLOSS', 'PRODUCT_NLOSS', 'PSNSHA', 'PSNSHADE_TO_CPOOL', 'PSNSUN', 'PSNSUN_TO_CPOOL', 'Q2M', 'QBOT', 'QCHANR', 'QCHANR_ICE', 'QCHARGE', 'QCHOCNR', 'QCHOCNR_ICE', 'QDRAI', 'QDRIP', 'QFLX_ICE_DYNBAL', 'QFLX_LIQ_DYNBAL', 'QINFL', 'QINTR', 'QMELT', 'QOVER', 'QRGWL', 'QRUNOFF', 'QRUNOFF_NODYNLNDUSE', 'QRUNOFF_R', 'QRUNOFF_U', 'QSNWCPICE', 'QSNWCPICE_NODYNLNDUSE', 'QSOIL', 'QVEGE', 'QVEGT', 'RAIN', 'RAINATM', 'RAINFM2A', 'RETRANSN', 'RETRANSN_TO_NPOOL', 'RH2M', 'RH2M_R', 'RH2M_U', 'RR', 'SABG', 'SABV', 'SEEDC', 'SEEDN', 'SHEAT', 'SMINN', 'SMINN_LEACHED', 'SMINN_TO_NPOOL', 'SMINN_TO_PLANT', 'SNOBCMCL', 'SNOBCMSL', 'SNODSTMCL', 'SNODSTMSL', 'SNOOCMCL', 'SNOOCMSL', 'SNOW', 'SNOWATM', 'SNOWDP', 'SNOWFM2A', 'SNOWICE', 'SNOWLIQ', 'SOIL1C', 'SOIL1N', 'SOIL2C', 'SOIL2N', 'SOIL3C', 'SOIL3N', 'SOIL4C', 'SOIL4N', 'SOILC', 'SOILC_HR', 'SOILC_LOSS', 'SOILICE', 'SOILLIQ', 'SOILPSI', 'SOILWATER_10CM', 'SOMHR', 'SR', 'STORVEGC', 'STORVEGN', 'SUCSAT', 'SUPPLEMENT_TO_SMINN', 'SoilAlpha', 'SoilAlpha_U', 'TAUX', 'TAUY', 'TBOT', 'TBUILD', 'TG', 'TG_R', 'TG_U', 'THBOT', 'TLAI', 'TLAKE', 'TOTCOLC', 'TOTCOLN', 'TOTECOSYSC', 'TOTECOSYSN', 'TOTLITC', 'TOTLITN', 'TOTPFTC', 'TOTPFTN', 'TOTPRODC', 'TOTPRODN', 'TOTSOMC', 'TOTSOMN', 'TOTVEGC', 'TOTVEGN', 'TREFMNAV', 'TREFMNAV_R', 'TREFMNAV_U', 'TREFMXAV', 'TREFMXAV_R', 'TREFMXAV_U', 'TSA', 'TSAI', 'TSA_R', 'TSA_U', 'TSOI', 'TSOI_10CM', 'TV', 'U10', 'URBAN_AC', 'URBAN_HEAT', 'VOCFLXT', 'VOLR', 'WA', 'WASTEHEAT', 'WATSAT', 'WIND', 'WOODC', 'WOODC_ALLOC', 'WOODC_LOSS', 'WOOD_HARVESTC', 'WOOD_HARVESTN', 'WT', 'XSMRPOOL', 'XSMRPOOL_RECOVER', 'ZBOT', 'ZSOI', 'ZWT', 'area', 'areaatm', 'areaupsc', 'date_written', 'edgee', 'edgen', 'edges', 'edgew', 'indxupsc', 'landfrac', 'landmask', 'latixy', 'latixyatm', 'longxy', 'longxyatm', 'mcdate', 'mcsec', 'mdcur', 'mscur', 'nstep', 'pftmask', 'time_bounds', 'time_written', 'topo', 'topodnsc']
            variable_list_str = ', '.join(variable_list)
            bookmark_variables = variable_list_str
        
        
        #grab the bookmark time periods
        if bookmark_time_periods == None:
            print 'using default bookmark_variables'
            season_list = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC','DJF','MAM','JJA','SON','ANN']
            season_list_str = ', '.join(season_list)
            bookmark_time_periods = season_list_str
        
        #grab the bookmark description
        if bookmark_description == None:
            print 'using default bookmark_descriptions'
            bookmark_description = 'Default description'
        
        #insert into database
        print 'inserting into database'
        
        
        
        from exploratory_analysis.models import Tree_Bookmarks
        p = Tree_Bookmarks(bookmark_name=bookmark_name,
                             bookmark_username=username,
                             bookmark_variables=bookmark_variables,
                             bookmark_time_periods=bookmark_time_periods,
                             bookmark_description=bookmark_description)
        p.save()
        print Tree_Bookmarks.objects.all()
        
        return HttpResponse()
        
    elif request.method == 'GET':
        print 'In GET'
        
        #grab the user's name
        username = 'jfharney'
        
        #grab the bookmark name
        bookmark_name = 'bookmark1390373464356'
        
        #query the database using username, figure bookmark name
        from exploratory_analysis.models import Tree_Bookmarks
        bookmark_list = Tree_Bookmarks.objects.filter(bookmark_name=bookmark_name,
                                                               bookmark_username='jfharney')
        
        bookmark_obj = None
        for f in bookmark_list:
            bookmark_obj = f
            
            
        
        #put into the context
        data =  { 'bookmark_username' : username, 
                 'bookmark_name' : bookmark_name, 
                 'bookmark_variables' : bookmark_obj.bookmark_variables,
                 'bookmark_time_periods' : bookmark_obj.bookmark_time_periods,
                 'bookmark_description': bookmark_obj.bookmark_description}
        
        data_string = json.dumps(data,sort_keys=True,indent=2)
        
        return HttpResponse(data_string)
    
        
        #return HttpResponse()
    
    '''  
  
  
  
  
  
  
#Tree Figures BookmarksAPI
#http://<host>/exploratory_analysis/figure_bookmarks
#Need to store Bookmark name, bookmark variables, bookmark time periods, bookmark description
def figure_bookmarks(request):
    
    
    username = None
    figure_bookmark_name = None
    figure_location = None
    figure_bookmark_description = None
    
    
    print 'in tree figures bookmarks'
    if request.method == 'POST':
        print 'in figure bookmarks POST'
        
        '''
        username = request.POST['figure_bookmark_username']
        figure_bookmark_name = request.POST['figure_bookmark_name']
        figure_bookmark_location = request.POST['figure_bookmark_location']
        figure_bookmark_description = request.POST['figure_bookmark_description']
        '''
        
        for key in request.POST:
            print 'key ' + key + ' value: ' + request.POST[key]
        
        '''
                'figure_bookmark_name' : figure_bookmark_name.
                'figure_bookmark_username' : figure_bookmark_username,
                'figure_bookmark_location' : figure_bookmark_location,
                'figure_bookmark_description' : figure_bookmark_description
        '''
        
        #grab the user's name
        #default username: jfharney
        if username == None:
            print 'using default username'
            username = 'jfharney'
        
        #grab the figure bookmark name
        #default bookmark: bookmark + currentmillitime
        if figure_bookmark_name == None:
            import time
            print 'tme ' + str(time.time())
            millis = int(round(time.time()*1000))
            print 'millis' + str(millis)
            figure_bookmark_name = 'bookmark' + str(millis)
            print 'using default figure bookmark name ' + figure_bookmark_name
        
        #grab the figure bookmark location
        #default figure: ../../../static/exploratory_analysis/cache/carousel/set6_turbf_Global.gif
        if figure_location == None:
            print 'using default figure location'
            figure_location = '../../../static/exploratory_analysis/cache/carousel/set6_turbf_Global.gif'
        
        #grab the figure bookmark description
        if figure_bookmark_description == None:
            print 'using default figure bookmark description'
            figure_bookmark_description = ''
        
        #insert into database
        print 'inserting into database'
        
        from exploratory_analysis.models import Figure_Bookmarks
        p = Figure_Bookmarks(figure_bookmark_name=figure_bookmark_name,
                             figure_bookmark_username=username,
                             figure_bookmark_location=figure_location,
                             figure_bookmark_description=figure_bookmark_description)
        p.save()
        print Figure_Bookmarks.objects.all()
        
        return HttpResponse()
    elif request.method == 'GET':
        print 'In GET'
        #grab the user's name
        #default username: jfharney
        if username == None:
            print 'using default username'
            username = 'jfharney'
        
        #grab the figure bookmark name
        #default bookmark: bookmark + currentmillitime
        if figure_bookmark_name == None:
            import time
            print 'tme ' + str(time.time())
            millis = int(round(time.time()*1000))
            print 'millis' + str(millis)
            #figure_bookmark_name = 'bookmark' + str(millis)
            figure_bookmark_name = 'bookmark' + '1390367784718'
            print 'using default figure bookmark name ' + figure_bookmark_name
        
        
        
        
        #query the database using username, figure bookmark name
        from exploratory_analysis.models import Figure_Bookmarks
        #figure_bookmark_list = Figure_Bookmarks.objects.filter(figure_bookmark_name='bookmark1390367784718',
        #                                                       figure_bookmark_username='jfharney')
        figure_bookmark_list = Figure_Bookmarks.objects.filter(figure_bookmark_name='bookmark1390440035535',
                                                               figure_bookmark_username='jfharney')
        
        figure_bookmark_obj = None
        for f in figure_bookmark_list:
            figure_bookmark_obj = f
            
            
        
        #put into the context
        data =  { 'figure_bookmark_username' : username, 
                 'figure_bookmark_name' : figure_bookmark_name, 
                 'figure_bookmark_location' : figure_bookmark_obj.figure_bookmark_location,
                 'figure_bookmark_description': figure_bookmark_obj.figure_bookmark_description}
        data_string = json.dumps(data,sort_keys=True,indent=2)
        
        return HttpResponse(data_string)
        
        



