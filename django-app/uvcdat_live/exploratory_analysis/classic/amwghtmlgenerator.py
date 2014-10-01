#from paths import paths
from amwgmaster import *

def pageGenerator(sets, varlist, times, package, dataset, options):
   obssort = 1 
   html = ''

   html = '<p>'
   html += '<img src="../images/SET'+sets+'.gif" border=1 hspace=10 align=left alt="set '+sets+'">'
   html += '<font color=maroon size=+3><b>'
   html += dataset+'<br>and<br>OBS data'
   html += '</b></font>'
        
   html += '<p>'
   html += '<b>DIAG Set'+sets+' '+amwgsets[sets]['desc']
   html += '<hr noshade size=2 size="100%">'
    
   html += '<b>'+amwgsets[sets]['preamble']

   maxcols = 0

   def_seasons = ['DJF', 'JJA', 'ANN']

   # Determine number of columns

   if sets in ['2', '8', '9', '10', '11', '12', '15']: def_seasons = ['NA']

   html += '<TABLE>'

   obssets = []
   setXvars = []
   for v in varinfo.keys():
      if sets in varinfo[v]['sets']:
         obssets.extend(varinfo[v]['obssets'].keys())
         setXvars.append(v)
   # unique-ify
   obssets = list(set(obssets))
   # This shouldn't be necessary but do it anyway
   setXvars = list(set(setXvars))
   

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
      regions = {'global':'GLBL', 'tropics (20S-20N)':'TROP', 'southern extratropics (90S-20S)':'SEXT', 'northen extratropics (20N-90N)':'NEXT'}
      html += '<TR>'
      html += '<TH ALIGN=LEFT><font color="navy" size="+1">Domain</font>'
      for season in seasons:
         html += '<TH>'+season
      for r in regions:
         html +='<TR>'
         for season in seasons:
            html +='   <TH ALIGN=LEFT><A HREF="table_'+regions[r]+'_'+season+'_obs.asc">table<\/a>'
      html += '</TABLE>'
      return html

   # this one is almost entirely special
   if sets == '14':
      html += '<TR>'
      html += ' <TH ALIGN=LEFT>Space and Time'
      fname = 'set14_ANN_SPACE_TIME_obsc.png'
      click = 'onclick="displayImageClick(\''+fname+'\');" '
      over = 'onmouseover="displayImageHover(\''+fname+'\');" '
      out = 'onmouseout="nodisplayImage();" '
      html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'

      html += '<TR>'
      html += ' <TH ALIGN=LEFT>Space only'
      seasons = ['ANN', 'DJF', 'MAM', 'JJA', 'SON']
      for season in seasons:
         fname = 'set14_'+season+'_SPACE_obsc.png'
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
         fname = 'set14.METRICS_'+varl[v]+'_SPACE_TIME_obsc.png'
         click = 'onclick="displayImageClick(\''+fname+'\');" '
         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
         out = 'onmouseout="nodisplayImage();" '
         html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+v+'</a>'
      html += '<TR>'
      html += '<TH ALIGN=LEFT>Space only'
      for v in varl.keys():
         fname = 'set14.METRICS_'+varl[v]+'_SPACE.png'
         click = 'onclick="displayImageClick(\''+fname+'\');" '
         over = 'onmouseover="displayImageHover(\''+fname+'\');" '
         out = 'onmouseout="nodisplayImage();" '
         html += ' <TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">'+v+'</a>'
      html += '<TR>'
      html += '<TH ALIGN=LEFT>Time only'
      fname = 'set14.METRICS_CC_TIME_obsc.png'
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
         fname ='set2_'+varl[v]+'_obs.png'
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
                     html += '    <TH ALIGN=LEFT>' + v.split('_')[0]
                  else:
                     html += '    <TH ALIGN=LEFT>' + v
                  html += '    <TH ALIGN=LEFT>' + varinfo[v]['desc']
                  for season in seasons:
                     if sets == '7':
                        fname = 'set'+sets+'_'+season+'_'+v.split('_')[0]+'_'+obsfname+'_NP_obsc.png'
                     else:
                        fname = 'set'+sets+'_'+season+'_'+v+'_'+obsfname+'_obsc.png'
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
                     html += '    <TH ALIGN=LEFT>' + v.split('_')[0]
                     html += '    <TH ALIGN=LEFT>' + varinfo[v]['desc']
                     for season in seasons:
                        fname = 'set'+sets+'_'+season+'_'+v.split('_')[0]+'_'+obsfname+'_SP_obsc.png'
                        click = 'onclick="displayImageClick(\''+fname+'\');" '
                        over = 'onmouseover="displayImageHover(\''+fname+'\');" '
                        out = 'onmouseout="nodisplayImage();" '
                        html += '<TH ALIGN=LEFT><A HREF="#" '+click+over+out+'">plot</a>'
               
         html += '</TABLE>'
         return html
      else:
         print 'NOT IMPLEMENTED SORTING BY VAR'
         return None

   if sets in ['8', '9', '10', '15']: # this could probably also be special cased above....
      if obssort == 1:
         for o in obssets:
            html += '<TR>'
            html += '<TH><BR>'
            html += '<TH ALIGN=LEFT><font color="navy" size="+1">'+o+'</font>'
            html += '<TH>'

            for v in setXvars:
               if o in varinfo[v]['obssets'].keys():
                  obsfname = varinfo[v]['obssets'][o]['filekey']
                  html += '<TR>'
                  html += '   <TH ALIGN=LEFT>'+v
                  html += '   <TH ALIGN=LEFT>'+varinfo[v]['desc']
                  fname = 'set'+sets+'_'+v+'_'+obsfname+'_obsc.png'
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
         fname = 'set11_SWCF_LWCF_'+obsfname+'_obs.png'
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
            fname = 'set11_'+v+'_'+set2list[v]['obssets'][o]+'_obsc.png'
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
#            img_prefix = paths.img_cache_path
            img_prefix='tst/'
            img_link = img_prefix + sets + '_' + col + '_' + var + '.png'

            mouseover = 'onmouseover=displayImageHover("' + img_link + '")'
            onmouseout = 'onmouseout="nodisplayImage();"'
            onclick = 'onclick=displayImageClick("' + img_link + '")'
            html += '<TH ALIGN=LEFT><A HREF="#" ' + onclick + ' ' + mouseover + ' ' + onmouseout + '>plot</a>'
            
      html += '</TABLE>'
    
      return html


if __name__ == '__main__':
   sets = ['1', '2', '3', '4', '4a', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
   times = ['DJF', 'ANN', 'JJA']

   for s in sets:
      html = pageGenerator(s, None, times, None, 'datasetname', None)
      fname = 'set'+s+'.html'
      f = open(fname, "w")
      f.write(html)
      f.close()
#      print html
   
   
