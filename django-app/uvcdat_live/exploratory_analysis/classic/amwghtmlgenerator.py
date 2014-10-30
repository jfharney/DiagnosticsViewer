from paths import paths
from amwgmaster import *
import os


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

def pageGenerator(sets, varlist, times, package, dataset, options):

   img_prefix = os.path.join(paths.img_cache_path, dataset, package, 'img', '')

   obssort = 1 
   html = ''

   html = '<p>'
   html += '<img src="/static/exploratory_analysis/img/classic/amwg/SET'+sets+'.gif" border=1 hspace=10 align=left alt="set '+sets+'">'
   html += '<font color=maroon size=+3><b>'
   html += dataset+'<br>and<br>OBS data'
   html += '</b></font>'
        
   html += '<p>'
   html += '<b>DIAG Set'+sets+' '+amwgsets[sets]['desc']
   html += '<hr noshade size=2 size="100%">'
    
   html += '<b>'+amwgsets[sets]['preamble']

   def_seasons = ['DJF', 'JJA', 'ANN']

   # Determine number of columns

   if sets in ['2', '8', '9', '10', '11', '12', '15' 'topten']: def_seasons = ['NA']

   html += '<TABLE>'

   # get a list of all obssets
   obslist = []
   for v in varinfo.keys():
      obslist.extend(varinfo[v]['obssets'].keys())
   # unique-ify
   obslist = list(set(obslist))

   obssets = []
   for v in varinfo.keys():
      for obs in varinfo[v]['obssets'].keys():
         if sets in varinfo[v]['obssets'][obs]['usedin']:
            obssets.append(obs)

   obssets = list(set(obssets))
#   print obssets

   setXvars = []
   for v in varinfo.keys():
      if sets in varinfo[v]['sets']:
         setXvars.append(v)
   setXvars = list(set(setXvars))
   
#   print setXvars

   #### Setup paths based on dataset name and path
   #### NOTE: Filename strings need converted to documented paths
   # intersect user times and the default seasons for this dataset
   seasons = list(set(times) & set(def_seasons))

   print 'DEFAULTING TO ALL SEASONS FOR NOW'
   print 'DEFAULTING TO ALL VARS FOR NOW'
   print 'DEFAULTING TO EXISTING FILENAME CONVENTIONS'
   print 'DEFAULTING TO NO ABSOLUTE PATHS'

   seasons = def_seasons

   # special(er) cases first
   if sets == '1':
      regions = {'Global':'global', 'Tropics (20S-20N)':'tropics', 'Southern Extratropics (90S-20S)':'southern_extratropics', 'Northern Extratropics (20N-90N)':'northern_extratropics'}
      html += '<TR>'
      html += '<TH ALIGN=LEFT><font color="navy" size="+1">Domain</font>'
      for season in seasons:
         html += '<TH>'+season
      for r in regions:
         html +='<TR>'
         html+='<TH>'+r+'</TH>'
         for season in seasons:
             #whenever these are generated with diags use this?
             fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package + '/AMWG_Diagnostics_Set_1:_'+season+'_means_'+regions[r]+'.text')
             click = 'onclick="displayTable(\''+fname+'\');" '
             over = 'onmouseover="displayTableHover(\''+fname+'\');" '
             out = 'onmouseout="nodisplayImage();" '
             html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'>table</a>'
      html += '</TABLE>'
      return html

   # this one is almost entirely special
   if sets == '14':
      html += '<TR>'
      html += ' <TH ALIGN=LEFT>Space and Time'
      fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14_ANN_SPACE_TIME.png')
      click = 'onclick="displayImageClick(\''+fname+'\');" '
      over = 'onmouseover="displayImageHover(\''+fname+'\');" '
      out = 'onmouseout="nodisplayImage();" '
      html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'

      html += '<TR>'
      html += ' <TH ALIGN=LEFT>Space only'
      seasons = ['ANN', 'DJF', 'MAM', 'JJA', 'SON']
      for season in seasons:
         fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14_'+season+'_SPACE.png')
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
         fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14.METRICS_'+varl[v]+'_SPACE_TIME.png')
         click = 'onclick="displayImageClick(\''+fname+'\');" '
         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
         out = 'onmouseout="nodisplayImage();" '
         html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+v+'</a>'
      html += '<TR>'
      html += '<TH ALIGN=LEFT>Space only'
      for v in varl.keys():
         fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set14.METRICS_'+varl[v]+'_SPACE.png')
         click = 'onclick="displayImageClick(\''+fname+'\');" '
         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
         out = 'onmouseout="nodisplayImage();" '
         html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+v+'</a>'
      html += '<TR>'
      html += '<TH ALIGN=LEFT>Time only'
      fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set14.METRICS_CC_TIME.png')
      click = 'onclick="displayImageClick(\''+fname+'\');" '
      over = 'onmouseover="displayImageHover(\''+fname+'\');" '
      out = 'onmouseout="nodisplayImage();" '
      html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">Correlation</a>'
      html += '</TABLE>'

      return html
      
   if sets == '2' :
      varl = {'Ocean Heat':'OHT', 'Atmospheric Heat':'AHT', 'Ocean Freshwater':'OFT'}
      html += '<TR>'
      html += '<TH ALIGN=LEFT><font color="navy" size="+1">Annual Implied Northward Transports</font><TH>'
      for v in varl.keys():
         html += '<TR>'
         html += ' <TH ALIGN=LEFT>'+v
         fname ='http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set2_'+varl[v]+'.png')
         click = 'onclick="displayImageClick(\''+fname+'\');" '
         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
         out = 'onmouseout="nodisplayImage();" '
         html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
      html += '</TABLE>'
      return html


   if sets in ['3', '4', '4a', '5', '6', '7']:
      # some minor preliminary setup for set 7
      if sets == '7':
         northkeys = []
         southkeys = []
         for v in varinfo.keys():
            if '_NORTH' in v:
               northkeys.append(v)
            if '_SOUTH' in v:
               southkeys.append(v)
         setXvars = northkeys

      if obssort == 1:
         for o in obssets:
            html += '<TR>'
            html += '<TH><BR>' # the variable
            html += '  <TH ALIGN=LEFT><font color="navy" size="+1">'+o+'</font>' # the obs/desc
            for season in seasons: 
               html += '    <TH>'+season # the plot links

            if sets == '7':
               html += '<TR><TH><BR><TH ALIGN=LEFT><font color="maroon" size="+1">Northern Hemisphere</font><TH><BR><TH><BR><TH><BR>'

            for v in setXvars:

               # Is this obset used by this variable?
               if o in varinfo[v]['obssets'].keys():
                  obsfname = varinfo[v]['obssets'][o]['filekey']
                  html += '<TR>'
                  if sets == '7':
                     html += '    <TH ALIGN=LEFT>' + v.replace('_NORTH','')
                  else:
                     html += '    <TH ALIGN=LEFT>' + v

                  html += '    <TH ALIGN=LEFT>' + varinfo[v]['desc']
                  for season in seasons:
                     if sets == '7':
                        if '_VISIR' in v:
                           fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package + '/set'+sets+'_'+season+'_'+v.replace('_NORTH','')+'_NP.png')
                        elif 'SURF_WIND' in v:
                           fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_WIND_SURF_'+obsfname+'_NP.png')
                        else:
                           fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_'+v.replace('_NORTH','')+'_'+obsfname+'_NP.png')
                     else:
                        if '_VISIR' in v:
                           fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_'+v+'-combined.png')
                        elif '_TROP' in v:
                           fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_'+v.replace('_TROP','')+'_'+obsfname+'-combined.png')
                        elif '_LAND' in v:
                           fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_PRECT_PRECL.png')
                        elif 'TTRP' in v:
                           fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_'+v+'_'+obsfname+'_TROP-combined.png')
                        else:
                           fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_'+v+'_'+obsfname+'-combined.png')
                     fname=fname.replace('.png', '-combined.png')
                     click = 'onclick="displayImageClick(\''+fname+'\');" '
                     over = 'onmouseover="displayImageHover(\''+fname+'\');" '
                     out = 'onmouseout="nodisplayImage();" '
                     html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'

            # do southern keys. This could probably be combined with the above somehow
            if sets == '7':
               html += '<TR><TH><BR><TH ALIGN=LEFT><font color="maroon" size="+1">Southern Hemisphere</font><TH><BR><TH><BR><TH><BR>'
               for v in southkeys:
   
                  # Is this obset used by this variable?
                  if o in varinfo[v]['obssets'].keys():
                     obsfname = varinfo[v]['obssets'][o]['filekey']
                     html += '<TR>'
                     html += '    <TH ALIGN=LEFT>' + v.replace('_SOUTH','')
                     html += '    <TH ALIGN=LEFT>' + varinfo[v]['desc']
                     for season in seasons:
                        if '_VISIR' in v:
                           fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_'+v.replace('_SOUTH','')+'_SP.png')
                        elif 'SURF_WIND' in v:
                           fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_WIND_SURF_'+obsfname+'_SP.png')
                        else:
                           fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+season+'_'+v.replace('_SOUTH','')+'_'+obsfname+'_SP.png')
                        click = 'onclick="displayImageClick(\''+fname+'\');" '
                        over = 'onmouseover="displayImageHover(\''+fname+'\');" '
                        out = 'onmouseout="nodisplayImage();" '
                        html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
               
         html += '</TABLE>'
         return html
      else:
         print 'NOT IMPLEMENTED SORTING BY VAR'
         return None

   if sets in ['8', '9', '10', '15', 'topten']: # this could probably also be special cased above....
      if obssort == 1:
         for o in obssets:
            html += '<TR>'
            html += '<TH><BR>'
            html += '<TH ALIGN=LEFT><font color="navy" size="+1">'+o+'</font>'
            html += '<TH>'

            for v in setXvars:
               if o in varinfo[v]['obssets'].keys():
                  if sets in varinfo[v]['obssets'][o]['usedin']:
                     obsfname = varinfo[v]['obssets'][o]['filekey']
                     html += '<TR>'
                     html += '   <TH ALIGN=LEFT>'+v
                     html += '   <TH ALIGN=LEFT>'+varinfo[v]['desc']
                     if sets == 'topten':
                        fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_ANN_'+v+'_'+obsfname+'-combined.png')
                     elif sets == '15':
                        fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+obsfname+'_'+v+'.png')
                     elif sets == '10':
                        fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_ANN_'+v+'_'+obsfname+'.png')
                     else:
                        fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+v+'_'+obsfname+'-combined.png')
                     if '_VISIR' in v:
                        fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+v+'.png')
                     if '_NORTH' in v:
                        fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+v.replace('_NORTH','')+'_'+obsfname+'_NP.png')
                     if '_SOUTH' in v:
                        fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set'+sets+'_'+v.replace('_SOUTH','')+'_'+obsfname+'_SP.png')

                     if sets == '8' or sets == '9':
                        fname = fname.replace('.png','-combined.png')
                     click = 'onclick="displayImageClick(\''+fname+'\');" '
                     over = 'onmouseover="displayImageHover(\''+fname+'\');" '
                     out = 'onmouseout="nodisplayImage();" '
                     html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
         html += '</TABLE>'
         return html
      else:
         print 'NOT IMPLEMENTED SORTING BY VAR'
         return None

   # more special cases
   if sets == '11':
      # two subtables.
      # format for both is <var><obs><plot link>
      set1obs = { 'CERES2 March 2000-October 2005':'CERES2','CERES 2000-2003':'CERES', 'ERBE 1985-1989':'ERBE'}
      set2list = {}
      set2list['LHFLX'] = {'desc':'Latent Heat Flux', 'obssets':{'ECMWF 1979-1993':'ECMWF', 'WHOI 1958-2006':'WHOI'}}
      set2list['PRECT'] = {'desc':'Precipitation Rate', 'obssets':{'GPCP 1979-2003':'GPCP'}}
      set2list['SST'] = {'desc':'Sea Surface Temperature', 'obssets':{'HADISST 1982-2001':'HADISST'}}
      set2list['SWCF'] = {'desc':'Shortwave Cloud Forcing', 'obssets':{'ERBE 1985-1989':'ERBE'}}
      set2list['TAUX'] = {'desc':'Surface Zonal Stress', 'obssets':{'ERS 1992-2000':'ERS', 'LARGE-YEAGER 1984-2004':'LARYEA'}}
      set2list['TAUY'] = {'desc':'Surface Meridional Stress', 'obssets':{'ERS 1992-2000':'ERS', 'LARGE-YEAGER 1984-2004':'LARYEA'}}

      html += '<TR>'
      html += ' <TH ALIGN=LEFT>Warm Pool Scatter Plot<TH><TH>'

      for o in set1obs:
         html += '<TR>'
         html += '  <TH ALIGN=LEFT>SW/LW Cloud Forcing'
         html += '  <TH ALIGN=LEFT><font color="navy">'+o+'</font>'
         obsfname = set1obs[o]
         fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set11_SWCF_LWCF_'+obsfname+'.png')
         click = 'onclick="displayImageClick(\''+fname+'\');" '
         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
         out = 'onmouseout="nodisplayImage();" '
         html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'

      html += '</TABLE>'
      html += '<TABLE>'

      html += '<TR>'
      html += '<TH ALIGN=LEFT">Annual Cycle on the Equatorial Pacific<TH><TH>'
      for v in set2list.keys():
         for o in set2list[v]['obssets'].keys():
            html += '<TR>'
            html += '  <TH ALIGN=LEFT>'+set2list[v]['desc']
            html += '  <TH ALIGN=LEFT>'+o
            fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package +'/set11_'+v+'_'+set2list[v]['obssets'][o]+'.png')
            click = 'onclick="displayImageClick(\''+fname+'\');" '
            over = 'onmouseover="displayImageHover(\''+fname+'\');" '
            out = 'onmouseout="nodisplayImage();" '
            html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'

      return html


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
               fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package  + 'set13_' + col + '_' + vlist[var] + '.png')
            else:
               fname = 'http://' + paths.ea_hostname + generate_token_url('/' + dataset + '/' + package  + 'set12_' + vlist[var] + '_' + col + '.png')

            click = 'onclick="displayImageClick(\''+fname+'\');" '
            over = 'onmouseover="displayImageHover(\''+fname+'\');" '
            out = 'onmouseout="nodisplayImage();" '
            html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'

            
      html += '</TABLE>'
    
      return html


if __name__ == '__main__':
   sets = ['1', '2', '3', '4', '4a', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', 'topten']
   times = ['DJF', 'ANN', 'JJA']

   for s in sets:
      html = pageGenerator(s, None, times, None, 'datasetname', None)
      fname = 'set'+s+'.html'
      f = open(fname, "w")
      f.write(html)
      f.close()
#      print html
   
   
