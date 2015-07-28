from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login

from metrics.frontend.amwgmaster import *
    

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



#various variables that need to go into a config file
#esgfAuth - flag for turning on (True) or turning off (False) esgf authentication
esgfAuth = False

#the directory for the certs to be fetched
proxy_cert_dir = '/tmp'

#naAuthReq - authentication via the cookie on (True) or off (False)
authReq = True

#certNameSuffix - the suffix of the certificate file
certNameSuffix = 'x509acme'


ea_root = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer'
uvcdat_live_root = ea_root+ '/django-app-1.8/uvcdat_live/' 
img_cache_path = uvcdat_live_root + '/exploratory_analysis/static/exploratory_analysis/cache/'
staticfiles_dirs = uvcdat_live_root + "/exploratory_analysis/static/exploratory_analysis"

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




from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

#Example: curl -i -H "Accept: application/json" -X POST -d '{ "username" :  "u1" }'  http://localhost:8081/exploratory_analysis/auth/
@ensure_csrf_cookie
def auth(request):
    
    
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
    
    sets = str(request.GET.get('set',''))
    
    #sets = str(set[3:])
    varlist = 'TLAI'
    times = 't1'
    dataset = 'd1'
    options = []
    package = 'lnd'
    
    html = ''
    
    try:
        if package == 'lnd':
            html = landPageGenerator(sets, varlist, times, package, dataset, options)
        else:
            html = pageGenerator(sets, varlist, times, package, dataset, options)
    
    except:
        tb = traceback.format_exc()
        print 'tb: ' + tb
        return HttpResponse("error")
        
    print 'returning html: ' + str(html)
    
    return HttpResponse(html)




'''
Begin page generator for atm
'''



def landPageGenerator(set, varlist, times, package, dataset, options):
    
    print 'in landPageGenerator'
    
    html = ''
    
    #regions = ['Global Land','Northern Hemisphere Land', 'Southern Hemisphere Land', 'Alaskan Arctic', 'Central U.S.', 'Mediterranean and Western Asia']  
    regions = ['Global','Alaska','Alaskan_Arctic','Amazonia','Antarctica','Arabian_Peninsula','Asia','Australia','Alaskan_Arctic', 'Central_US', 'Mediterranean'] 
    set3varlist = ['hydro', 'landf', 'moistEnergyFlx', 'radf', 'reg', 'snow', 'turbf']
    set6varlist = ['cnFlx', 'frFlx', 'hydro', 'landf', 'radf', 'reg', 'snowliqIce', 'soilice', 'soilliq', 'soilliiqIce', 'tsoi', 'turbf']
    set3Headers = ['reg', 'landf','randf','turbf','cnFlx','frFlx','moistEnergyFlx','snow','albedo','hydro']
        
    if set == '1': 

            url_prefix = staticfiles_dirs + "/img/classic/" + dataset + "/" + package + "/"
            url_prefixIMAGE = "/" + dataset + "/" + package + "/set1_"
            url = url_prefix + set + ".html"

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
                if 1 in vardict[key]['sets'] and key in varlist:
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
                    html+= 'http://' + ea_hostname + generate_token_url(url_prefixIMAGE + key + '.gif')
                    html+='\''
                    html+=');" onmouseover="displayImageHover(\''
                    #file.write(url_prefixIMAGE)#Here we write gif name again
                    html+='http://' + ea_hostname + generate_token_url(url_prefixIMAGE + key + '.gif')
                    html+='\''
                    html+=');" onmouseout="nodisplayImage();">plot</A>\n'
                    html+="</TR>\n"
            

            #end for loop and end table generation-------------------------
            
            html+="</TABLE> \n"
            html+="</p>\n"
    

    

    
    return html 













'''
Begin page generator for atm
'''


def pageHeader(dataset,sets):
    # Header stuff
    html = ''
    html = '<p>'
    html += '<img src="/static/exploratory_analysis/img/classic/amwg/SET'+sets+'.gif" border=1 hspace=10 align=left alt="set '+sets+'">'
    html += '<font color=maroon size=+3><b>'
    html += dataset+'<br>and<br>OBS data'
    html += '</b></font>'
            
    html += '<p>'
    html += '<b>DIAG Set'+sets+' '+diags_collection[sets]['desc']
    html += '<hr noshade size=2 size="100%">'
        
    html += '<b>'+diags_collection[sets].get('preamble', '')

    return html
    
    

def pageGenerator(sets, varlist, times, package, dataset, options):
    
    
    print 'img_cache_path: ' + img_cache_path
    
    print 'sets: ' + sets
    
    html = ''
    try:
        img_prefix = ''
        if __name__ != '__main__':
          img_prefix = os.path.join(img_cache_path, dataset, package, 'img', '')
        else:
          img_prefix ='path'
    
    
        #sets = '3'
        #sets = '4'
        
        html = pageHeader(dataset,sets)
        
        
        obssort = 1 
   
        
    
    
        
        
        print 'DEFAULTING TO ALL VARS FOR NOW'
        print 'DEFAULTING TO EXISTING FILENAME CONVENTIONS'
        print 'DEFAULTING TO NO ABSOLUTE PATHS'
     
        # Determine number of columns
        # The default is just 'ANN', and if that is the only one or nothing is specified, we don't need a column for it.
        # ['NA'] is also something to deal with.
        seasons = diags_collection[sets].get('seasons', ['ANN'])
        # Were some specific seasons passed in? If so, limit our list.
        print 'DEFAULTING TO ALL SEASONS FOR NOW'
        #if seasons != ['NA']:
        #   seasons = list(set(times) & set(def_seasons))
        
        regions = diags_collection[sets].get('regions', ['Global'])
        
        
        # get a list of all obssets used in this collection
        varlist = list(set(diags_collection[sets].keys()) - set(collection_special_vars))
        obslist = []
        for v in varlist:
            obslist.extend(diags_collection[sets][v]['obs'])
            # unique-ify
        obslist = list(set(obslist))

        # does this set need the --combined filename?
        # Eventually this might be per-variable...
        hasCombined = diags_collection[sets].get('combined',False)

        print '\n\n\n'
        print 'regions: ' + str(regions)
        print 'varlist: ' + str(varlist)
        print 'obslist: ' + str(obslist)
        print 'hasCombined: ' + str(hasCombined)
        
        print '\n\n'
        
        specialCases = ['1', '2', '11', '12', '13', '14']
   
        ea_hostname = 'localhost'
        
        
        html += '<TABLE>'

        
        if sets not in specialCases:
            if obssort == 1:
                print 'obsort = 1'
                for o in obslist:
                    html += '<TR>'
                    html += '<TH><BR>' # the variable
                    obsname = diags_obslist[o]['desc']
                    html += '  <TH ALIGN=LEFT><font color="navy" size="+1">'+obsname+'</font>' # the obs/desc
                    
                    #print '\thtml: ' + '  <TH ALIGN=LEFT><font color="navy" size="+1">'+obsname+'</font>' # the obs/desc
                    if len(seasons) != 1:
                        for season in seasons: 
                            print '\t    <TH>'+season
                            html += '    <TH>'+season # the plot links
                    else:
                        html += '<TH>'
                    
                    for v in varlist:
                    # Is this obsset used by this variable?
                        print 'v: ' + v
                        if diags_collection[sets][v]['obs'] != None:
                            print '\tNot None'
                            if o in diags_collection[sets][v]['obs']:
                                print '\t\o: ' + str(o)
                                obsfname = diags_obslist[o]['filekey']
                                html += '<TR>'
                                html += '    <TH ALIGN=LEFT>' + v
                                html += '    <TH ALIGN=LEFT>' + diags_varlist[v]['desc']
                
                
                                '''
                                if regions == ['Global']:
                                    regionstr = '_Global'
                                    print 'regions: ' + str(regions)
                                '''
                
                                regionstr = '_Global'
                                
                                for season in seasons:
                                         if season == 'NA':
                                            seasonstr = ''
                                         else:
                                            seasonstr = '_'+season
                                         if hasCombined == True:
                                            postfix = '-combined.png'
                                         else:
                                            postfix = '-model.png'
                                         varopts = diags_collection[sets][v].get('varopts', False)
                                         if varopts == False:
                                            fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set'+sets+regionstr+seasonstr+'_'+v+'_'+obsfname+postfix)
                                         else:
                                            for varopt in varopts:
                                               fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set'+sets+regionstr+seasonstr+'_'+v+'_'+varopt+'_'+obsfname+postfix)
                                         
                                         click = 'onclick="displayImageClick(\''+fname+'\');" '
                                         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
                                         out = 'onmouseout="nodisplayImage();" '
                                         html_class = 'plot_links'
                                         
                                         html += '<TH ALIGN=LEFT><A HREF="#" class="' + html_class + '" ' +click+over+out+'">plot</a>'               
                                         print '\nadding a link\n'
                
            html += '</TABLE>'
                            
        # The special cases.
        if sets == '1':
            regions = diags_collection[sets]['regions']
        
            html += '<TR>'
            html += '<TH ALIGN=LEFT><font color="navy" size="+1">Domain</font>'
            for season in seasons:
                html += '<TH>'+season
            for r in regions:
                html +='<TR>'
                html+='<TH>'+r+'</TH>'
                for season in seasons:
                     #whenever these are paths.generated with diags use this?
                     fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set1_'+season+'_'+all_regions[r].filekey+'-table.text')
        #             print 'looking for '+fname
                     click = 'onclick="displayTable(\''+fname+'\');" '
                     over = 'onmouseover="displayTableHover(\''+fname+'\');" '
                     out = 'onmouseout="nodisplayImage();" '
                     html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'>table</a>'
            html += '</TABLE>'
        
        
        if sets == '11':
            # two subtables.
            # format for both is <var><obs><plot link>
            set1obs = { 'CERES2 March 2000-October 2005':'CERES2','CERES 2000-2003':'CERES', 'ERBE 1985-1989':'ERBE'}
            set2list = {}
            set2list['LHFLX'] = {'desc':'Latent Heat Flux', 'obslist':{'ECMWF 1979-1993':'ECMWF', 'WHOI 1958-2006':'WHOI'}}
            set2list['PRECT'] = {'desc':'Precipitation Rate', 'obslist':{'GPCP 1979-2003':'GPCP'}}
            set2list['SST'] = {'desc':'Sea Surface Temperature', 'obslist':{'HADISST 1982-2001':'HADISST'}}
            set2list['SWCF'] = {'desc':'Shortwave Cloud Forcing', 'obslist':{'ERBE 1985-1989':'ERBE'}}
            set2list['TAUX'] = {'desc':'Surface Zonal Stress', 'obslist':{'ERS 1992-2000':'ERS', 'LARGE-YEAGER 1984-2004':'LARYEA'}}
            set2list['TAUY'] = {'desc':'Surface Meridional Stress', 'obslist':{'ERS 1992-2000':'ERS', 'LARGE-YEAGER 1984-2004':'LARYEA'}}
        
            html += '<TR>'
            html += ' <TH ALIGN=LEFT>Warm Pool Scatter Plot<TH><TH>'
        
            for o in set1obs:
               html += '<TR>'
               html += '  <TH ALIGN=LEFT>SW/LW Cloud Forcing'
               html += '  <TH ALIGN=LEFT><font color="navy">'+o+'</font>'
               obsfname = set1obs[o]
               fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set11_SWCF_LWCF_'+obsfname+'.png')
               click = 'onclick="displayImageClick(\''+fname+'\');" '
               over = 'onmouseover="displayImageHover(\''+fname+'\');" '
               out = 'onmouseout="nodisplayImage();" '
               html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
        
            html += '</TABLE>'
            html += '<TABLE>'
        
            html += '<TR>'
            html += '<TH ALIGN=LEFT">Annual Cycle on the Equatorial Pacific<TH><TH>'
            for v in set2list.keys():
                for o in set2list[v]['obslist'].keys():
                    html += '<TR>'
                    html += '  <TH ALIGN=LEFT>'+set2list[v]['desc']
                    html += '  <TH ALIGN=LEFT>'+o
                    fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set11_'+v+'_'+set2list[v]['obslist'][o]+'.png')
                    click = 'onclick="displayImageClick(\''+fname+'\');" '
                    over = 'onmouseover="displayImageHover(\''+fname+'\');" '
                    out = 'onmouseout="nodisplayImage();" '
                    html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
        
              
        
      
        
        
        # These two are pretty similar at least.
        if sets == '12' or sets == '13':
        
            if sets == '12':
               cols = ['T', 'Q', 'H']
               vlist = { 'Thule Greenland':'Thule_Greenland', 'Resolute NWT Canada':'Resolute_Canada', 'Ship P Gulf of Alaska':'ShipP_GulfofAlaska', 'Midway Island (N Pacific)':'Midway_Island', 'Northern Great Plains USA':'Great_Plains_USA', 'San Francisco Calif USA':'SanFrancisco_CA', 'Western Europe':'Western_Europe', 'Miami Florida USA':'Miami_FL', 'Panama Central America':'Panama', 'Hawaii (Eq Pacific)':'Hawaii', 'Marshall Islands (Eq Pacific)':'Marshall_Islands', 'Yap Island (Eq Pacific)':'Yap_Island', 'Truk Island (Eq Pacific)':'Truk_Island', 'Diego Garcia (Eq Indian)':'Diego_Garcia', 'Ascension Island (Eq Atlantic)':'Ascension_Island', 'Easter Island (S Pacific)':'Easter_Island', 'McMurdo Antarctica':'McMurdo_Antarctica'}
               header = 'Station Name'
            else:
               cols = ['DJF', 'JJA', 'ANN']
               vlist = {'Global':'global', 'Tropics (15S-15N)':'tropics', 'NH SubTropics (15N-30N)':'nsubtrop', 'SH SubTropics (30S-15S)':'ssubtrop', 'NH Mid-Latitudes (30N-70N)':'nmidlats', 'SH Mid-Latitudes (70S-30S)':'smidlats', 'NH Polar (70N-90N)':'npole', 'SH Polar (90S-70S)':'spole', 'North Pacific Stratus':'npacstrat', 'South Pacific Stratus':'spacstrat', 'North Pacific':'npacific', 'North Atlantic':'natlantic', 'Warm Pool':'warmpool', 'Central Africa':'cafrica', 'USA':'usa'}
               header = 'Region'
        
            html += '<TR>'
            html += '<TH ALIGN=LEFT><font color=blue>'+header+'</font>'
        
            for col in cols:
               html += '<TH>' + col
            
            for var in vlist:
               html += '<TR>'
               html += '<TH ALIGN=LEFT>' + var
               # some day, we could check for all of the "derived" paths and use them if defined, otherwise derive them.
            
               for col in cols:
                  if sets == '13':
                     fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package  + 'set13_' + col + '_' + vlist[var] + '.png')
                  else:
                     fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package  + 'set12_' + vlist[var] + '_' + col + '.png')
    
                  click = 'onclick="displayImageClick(\''+fname+'\');" '
                  over = 'onmouseover="displayImageHover(\''+fname+'\');" '
                  out = 'onmouseout="nodisplayImage();" '
                  html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
    
                
            html += '</TABLE>'
    
    
        if sets == '14':
            html += '<TR>'
            html += ' <TH ALIGN=LEFT>Space and Time'
            fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14_ANN_SPACE_TIME.png')
            click = 'onclick="displayImageClick(\''+fname+'\');" '
            over = 'onmouseover="displayImageHover(\''+fname+'\');" '
            out = 'onmouseout="nodisplayImage();" '
            html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
    
            html += '<TR>'
            html += ' <TH ALIGN=LEFT>Space only'
            seasons = ['ANN', 'DJF', 'MAM', 'JJA', 'SON']
            for season in seasons:
               fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14_'+season+'_SPACE.png')
               click = 'onclick="displayImageClick(\''+fname+'\');" '
               over = 'onmouseover="displayImageHover(\''+fname+'\');" '
               out = 'onmouseout="nodisplayImage();" '
               html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+season+'</a>'
    
            html += '</TABLE>'

            html += '<TABLE>'
            html += '<TR>'
            html += '<TH ALIGN=LEFT>Bias(%), Variance (ratio), Correlation Coefficient Tables'
            html += '<TR>'
            html += '<TH ALIGN=LEFT>Space and Time'
            varl = {'Correlation':'CC', 'Variance': 'VAR', 'Bias':'BIAS'}
            for v in varl.keys():
               fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14.METRICS_'+varl[v]+'_SPACE_TIME.png')
               click = 'onclick="displayImageClick(\''+fname+'\');" '
               over = 'onmouseover="displayImageHover(\''+fname+'\');" '
               out = 'onmouseout="nodisplayImage();" '
               html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+v+'</a>'
            html += '<TR>'
            html += '<TH ALIGN=LEFT>Space only'
            for v in varl.keys():
               fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14.METRICS_'+varl[v]+'_SPACE.png')
               click = 'onclick="displayImageClick(\''+fname+'\');" '
               over = 'onmouseover="displayImageHover(\''+fname+'\');" '
               out = 'onmouseout="nodisplayImage();" '
               html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+v+'</a>'
            html += '<TR>'
            html += '<TH ALIGN=LEFT>Time only'
            fname = 'http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set14.METRICS_CC_TIME.png')
            click = 'onclick="displayImageClick(\''+fname+'\');" '
            over = 'onmouseover="displayImageHover(\''+fname+'\');" '
            out = 'onmouseout="nodisplayImage();" '
            html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">Correlation</a>'
            html += '</TABLE>'

      
      
        if sets == '2' :
          for v in varlist:
             obsname = diags_collection[sets][v]['obs']
    
          html += '<TR>'
          html += '<TH ALIGN=LEFT><font color="navy" size="+1">Annual Implied Northward Transports</font><TH>'
          for v in varlist:
             obsname = diags_collection[sets][v]['obs']
             fkey = diags_varlist[v]['filekey']
             print 'file key:', fkey
             desc = diags_varlist[v]['desc']
             if type(obsname) == list and len(obsname) != 1:
                print 'Set 2 only supports one obs set for a given "variable"'
                quit()
             if type(obsname) == list:
                obsname = obsname[0]
             obskey = diags_obslist[obsname]['filekey']
    
             html += '<TR>'
             html += ' <TH ALIGN=LEFT>'+desc
             fname ='http://' + ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set2_ANN_'+fkey+'_'+obskey+'_Global-combined.png')
    #         print 'set 2 fname: ', fname
             click = 'onclick="displayImageClick(\''+fname+'\');" '
             over = 'onmouseover="displayImageHover(\''+fname+'\');" '
             out = 'onmouseout="nodisplayImage();" '
             html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
          html += '</TABLE>'

        
        return html
    
    except:
        tb = traceback.format_exc()
        print 'tb: ' + tb
        return HttpResponse("error")
    
    
    

    return html






'''
End page generator for atm
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
        
        '''
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
        '''
    
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
        html += '<div>' + img_prefix + '</div>'
    
        
        obssort = 1 
        # Header stuff
        html = ''
        html = '<p>'
        html += '<img src="/static/exploratory_analysis/img/classic/amwg/SET'+sets+'.gif" border=1 hspace=10 align=left alt="set '+sets+'">'
        html += '<font color=maroon size=+3><b>'
        html += dataset+'<br>and<br>OBS data'
        html += '</b></font>'
                
        html += '<p>'
        html += '<b>DIAG Set'+sets+' '+diags_collection[sets]['desc']
        html += '<hr noshade size=2 size="100%">'
            
        html += '<b>'+diags_collection[sets].get('preamble', '')
'''

    
