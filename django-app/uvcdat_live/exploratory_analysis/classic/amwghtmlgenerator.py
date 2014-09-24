

def set4(set,vars,times,package,dataset,options):
    
    html = ''
    
    html += '<p>'
    html += '<img src="../images/SET4.gif" border=1 hspace=10 align=left alt="set 4">'
    html += '<font color=maroon size=+3><b>'
    html += 't85f09.B1850 <br>and<br> OBS data'
    html += '</b></font>'
    html += '<p>'
    html += '<a href="../sets.htm">'
    html += '<font color=red><b>Back to diagnostic sets</b></font></a>'
    html += '<br clear=left>'
    html += '<p>'
    html += '<b>DIAG Set 4 - Vertical contour plots of DJF, JJA and ANN zonal means</b>'
    html += '<hr noshade size=2 size="100%">'
    
    #need to replace these with the python dictionary
    od = ['AIRS IR Sounder 2002-06', 'CERES 2000-2003', 'CERES2 March 2000-October 2005', 'CLOUDSAT (Radar+Lidar) Sep2006-Nov2008', 'CMAP (Xie-Arkin) 1979-98', 'ECMWF Reanalysis 1979-93', 'ERA40 Reanalysis 1980-2001', 'ERBE Feb1985-Apr1989', 'GPCP 1979-2003', 'IPCC/CRU climatology 1961-90', 'ISCCP D2 1983-2001', 'ISCCP FD Jul1983-Dec2000', 'JRA25 Reanalysis 1979-2004', 'Large-Yeager 1984-2004', 'Legates and Willmott 1920-80', 'MODIS 2000-2004', 'NCEP Reanalysis 1979-98', 'NVAP 1988-1999', 'SSM/I (Wentz) 1987-2000', 'TRMM (3B43) 1998-Feb2004', 'Warren Cloud Surface OBS', 'Willmott and Matsuura 1950-99', 'Woods Hole OAFLUX 1958-2006']
    vd = ['CLDHGH', 'CLDHGH_VISIR', 'CLDLOW', 'CLDLOW_VISIR', 'CLDMED', 'CLDMED_VISIR', 'CLDTOT', 'CLDTOT_VISIR', 'FLDS', 'FLDSC', 'FLNS', 'FLNSC', 'FLUT', 'FLUTC', 'FSDS', 'FSDSC', 'FSNS', 'FSNSC', 'FSNTOA', 'FSNTOAC', 'LHFLX', 'LWCF', 'LWCFSRF', 'PRECT', 'PREH2O', 'PSL', 'QFLX', 'SHFLX', 'SWCF', 'SWCFSRF', 'TGCLDLWP', 'TREFHT', 'TS']
    
    seasons = times
    seasons = ['DJF', 'ANN', 'JJA']
    
    html += '<TABLE>'
    html += '<TR>'
    html += '<TH><BR>'
    html += '<TH ALIGN=LEFT><font color=navy size=+1>NCEP Reanalysis 1979-98</font>'
    for season in seasons:
        html += '<TH>' + season


    html += '<TR>'
    html += '<TH ALIGN=LEFT>OMEGA *'
    html += '<TH ALIGN=LEFT>Pressure vertical velocity'
    for season in seasons:
        html += '<TH ALIGN=LEFT><A HREF="set4_' + season + '_OMEGA_NCEP_obsc.png">plot</a>' 
    
    
    html += '<TR>'
    html += '<TH><BR>'
    html += '<TH ALIGN=LEFT><font color=navy size=+1>ERA40 Reanalysis 1980-2001</font>'
    html += '<TH>DJF'
    html += '<TH>JJA'
    html += '<TH>ANN'
    html += '<TR>'
    html += '<TH ALIGN=LEFT>OMEGA *'
    html += '<TH ALIGN=LEFT>Pressure vertical velocity'
    html += '<TH ALIGN=LEFT><A HREF="set4_DJF_OMEGA_ERA40_obsc.png">plot</a>'
    html += '<TH ALIGN=LEFT><A HREF="set4_JJA_OMEGA_ERA40_obsc.png">plot</a>'
    html += '<TH ALIGN=LEFT><A HREF="set4_ANN_OMEGA_ERA40_obsc.png">plot</a>'
    
    
    return html

def set4a(set,vars,times,package,dataset,options):
    
    html = ''
    
    
    
    return html
    
def set3(set,vars,times,package,dataset,options):
    
    # set 3

    obsprefix={'GPCP 1979-2003':'GPCP', 'NVAP 1988-1999':'NVAP', 'MODIS 2000-2004':'MODIS', 'CERES 2000-2003':'CERES', 'ISCCP D2 1983-2001':'ISCCP', 'ERA40 Reanalysis 1980-2001':'ERA40', 'ECMWF Reanalysis 1979-93':'ECMWF', 'SSM/I (Wentz) 1987-2000':'SSMI', 'Large-Yeager 1984-2004':'LARYEA', 'IPCC/CRU climatology 1961-90':'CRU', 'CMAP (Xie-Arkin) 1979-98':'XA', 'NCEP Reanalysis 1979-98':'NCEP', 'TRMM (3B43) 1998-Feb2004':'TRMM', 'Legates and Willmott 1920-80':'LEGATES', 'ERBE Feb1985-Apr1989':'ERBE', 'Willmott and Matsuura 1950-99':'WILLMOTT', 'CERES2 March 2000-October 2005':'CERES2', 'Woods Hole OAFLUX 1958-2006':'WHOI', 'ISCCP FD Jul1983-Dec2000':'ISCCP', 'CLOUDSAT (Radar+Lidar) Sep2006-Nov2008':'CLOUDSAT', 'JRA25 Reanalysis 1979-2004':'JRA25', 'AIRS IR Sounder 2002-06':'AIRS', 'Warren Cloud Surface OBS':'WARREN'}
    vardict = {}
    vardict['TREFHT'] = {'desc':'2-meter air temperature (land)', 'obssets': [ 'IPCC/CRU climatology 1961-90', 'Willmott and Matsuura 1950-99', 'Legates and Willmott 1920-80', 'JRA25 Reanalysis 1979-2004'], 'sets':[3]}
    vardict['PRECT'] = {'desc':'Precipitation rate', 'obssets': [ 'Legates and Willmott 1920-80', 'GPCP 1979-2003', 'CMAP (Xie-Arkin) 1979-98', 'SSM/I (Wentz) 1987-2000', 'TRMM (3B43) 1998-Feb2004'], 'sets':[3]}
    vardict['PREH2O'] = {'desc':'Total precipitable water', 'obssets': [ 'JRA25 Reanalysis 1979-2004', 'NCEP Reanalysis 1979-98', 'ECMWF Reanalysis 1979-93', 'ERA40 Reanalysis 1980-2001', 'MODIS 2000-2004', 'NVAP 1988-1999', 'AIRS IR Sounder 2002-06', 'SSM/I (Wentz) 1987-2000'], 'sets':[3]}
    vardict['PSL'] = {'desc':'Sea level pressure', 'obssets': ['JRA25 Reanalysis 1979-2004', 'NCEP Reanalysis 1979-98'], 'sets':[3]}
    vardict['SHFLX'] = {'desc':'Surface sensible heat flux', 'obssets': ['JRA25 Reanalysis 1979-2004', 'NCEP Reanalysis 1979-98', 'Large-Yeager 1984-2004'], 'sets':[3]}
    vardict['LHFLX'] = {'desc':'Surface latent heat flux', 'obssets':[ 'JRA25 Reanalysis 1979-2004', 'ECMWF Reanalysis 1979-93', 'ERA40 Reanalysis 1980-2001', 'Woods Hole OAFLUX 1958-2006'],'sets':[3]}
    vardict['TS'] = {'desc':'Surface temperatuer', 'obssets': ['NCEP Reanalysis 1979-98'],'sets':[3]}
    vardict['QFLX'] = {'desc':'Surface water flux', 'obssets':[ 'ECMWF Reanalysis 1979-93', 'Woods Hole OAFLUX 1958-2006', 'Large-Yeager 1984-2004'], 'sets':[3]}
    vardict['TGCLDLWP'] = {'desc':'Cloud Liquid Water', 'obssets': ['MODIS 2000-2004', 'NVAP 1988-1999', 'SSM/I (Wentz) 1987-2000'], 'sets':[3]}
    vardict['FLNS'] = {'desc':'Surf Net LW Flux', 'obssets':[ 'Large-Yeager 1984-2004', 'ISCCP FD Jul1983-Dec2000'], 'sets':[3]}
    vardict['FSNS'] = {'desc':'Surf Net SW Flux', 'obssets':[ 'Large-Yeager 1984-2004', 'ISCCP FD Jul1983-Dec2000'], 'sets':[3]}
    vardict['FLUT'] = {'desc':'TOA Upward LW Flux', 'obssets':[ 'CERES2 March 2000-October 2005', 'CERES 2000-2003', 'ERBE Feb1985-Apr1989'], 'sets':[3]}
    vardict['FLUTC'] = {'desc':'TOA clearsky upward LW flux', 'obssets':[ 'CERES2 March 2000-October 2005', 'CERES 2000-2003', 'ERBE Feb1985-Apr1989'], 'sets':[3]}
    vardict['FSNTOA'] = {'desc':'TOA net SW Flux', 'obssets':[ 'CERES2 March 2000-October 2005', 'CERES 2000-2003', 'ERBE Feb1985-Apr1989'], 'sets':[3]}
    vardict['FSNTOAC'] = {'desc':'TOA clearsky net SW flux', 'obssets':[ 'CERES2 March 2000-October 2005', 'CERES 2000-2003', 'ERBE Feb1985-Apr1989'], 'sets':[3]}
    vardict['LWCF'] = {'desc':'TOA longwave cloud forcing', 'obssets':[ 'CERES2 March 2000-October 2005', 'CERES 2000-2003', 'ERBE Feb1985-Apr1989'], 'sets':[3]}
    vardict['SWCF'] = {'desc':'TOA shortwave cloud forcing', 'obssets':[ 'CERES2 March 2000-October 2005', 'CERES 2000-2003', 'ERBE Feb1985-Apr1989'], 'sets':[3]}
    vardict['FLDS'] = {'desc':'Surf LW downwelling flux', 'obssets':[ 'ISCCP FD Jul1983-Dec2000'], 'sets':[3]}
    vardict['FLDSC'] = {'desc':'Clearsky Surf LW downwelling flux', 'obssets':[ 'ISCCP FD Jul1983-Dec2000'], 'sets':[3]}
    vardict['FLNSC'] = {'desc':'Clearsky Surf Net LW Flux', 'obssets':[ 'ISCCP FD Jul1983-Dec2000'], 'sets':[3]}
    vardict['FSDS'] = {'desc':'Surf SW downwelling flux', 'obssets':[ 'ISCCP FD Jul1983-Dec2000'], 'sets':[3]}
    vardict['FSDSC'] = {'desc':'Clearsky Surf SW downwelling flux', 'obssets':[ 'ISCCP FD Jul1983-Dec2000'], 'sets':[3]}
    vardict['FSNSC'] = {'desc':'Clearsky Surf Net SW flux', 'obssets':[ 'ISCCP FD Jul1983-Dec2000'], 'sets':[3]}
    vardict['LWCFSRF'] = {'desc': 'Surf LW cloud forcing', 'obssets':[ 'ISCCP FD Jul1983-Dec2000'], 'sets':[3]}
    vardict['SWCFSRF'] = {'desc':'Surf SW Cloud Forcing', 'obssets':[ 'ISCCP FD Jul1983-Dec2000'], 'sets':[3]}
    vardict['CLDHGH'] = {'desc':'High cloud amount (IR clouds)', 'obssets':[ 'ISCCP D2 1983-2001', 'CLOUDSAT (Radar+Lidar) Sep2006-Nov2008'],'sets':[3]}
    vardict['CLDHGH_VISIR'] = {'desc':'High cloud amount (VIS/IR/NIR clouds)', 'obssets':[ 'ISCCP D2 1983-2001'],'sets':[3]}
    vardict['CLDLOW'] = {'desc':'Low cloud amount (IR clouds)', 'obssets':[ 'ISCCP D2 1983-2001', 'Warren Cloud Surface OBS', 'CLOUDSAT (Radar+Lidar) Sep2006-Nov2008'],'sets':[3]}
    vardict['CLDLOW_VISIR'] = {'desc':'Low cloud amount (VIS/IR/NIR clouds)', 'obssets':[ 'ISCCP D2 1983-2001'],'sets':[3]} 
    vardict['CLDMED'] = {'desc':'Mid cloud amount (IR clouds)', 'obssets': [ 'ISCCP D2 1983-2001', 'CLOUDSAT (Radar+Lidar) Sep2006-Nov2008'],'sets':[3]}
    vardict['CLDMED_VISIR'] = {'desc':'Mid cloud amount (VIS/IR/NIR)', 'obssets': [ 'ISCCP D2 1983-2001'],'sets':[3]}
    vardict['CLDTOT'] = {'desc':'Total cloud amount (IR clouds)','obssets': [ 'ISCCP D2 1983-2001', 'Warren Cloud Surface OBS'],'sets':[3]}
    vardict['CLDTOT_VISIR'] = {'desc':'Total cloud amount (VIS/IR/NIR clouds)','obssets': [ 'ISCCP D2 1983-2001'],'sets':[3]}


    
    
    
    html = '<p>'
    
    html += '<img src="../images/SET3.gif" border=1 hspace=10 align=left alt="set 3">'
    html += '<font color=maroon size=+3><b>'
    html += 't85f09.B1850 <br>and<br> OBS data'
    html += '</b></font>'
    '''
    html += '<p>'
    html += '<a href="../sets.htm">'
    html += '<font color=red><b>Back to diagnostic sets</b></font></a>'
    html += '<br clear=left>'
    '''
    html += '<p>'
    html += '<b>DIAG Set 3 - Line plots of DJF, JJA and ANN zonal means</b>'
    html += '<hr noshade size=2 size="100%">'
    
    html += '<TABLE>'
    
    vd = vardict.keys()
    vd.sort()
    od = obsprefix.keys()
    od.sort()
    
    
    seasons = times
    seasons = ['DJF', 'ANN', 'JJA']
    
    print 'vd: ' + str(vd)
    
    for o in od:
        
        html += '<TR>'
        html += '    <TH><BR>'
        html += '    <TH ALIGN=LEFT><font color=navy size=+1>' + o + '</font>'
        
        for season in seasons:
            html += '    <TH>' + season
    
        
        for v in vd:
            #if given that variable
            #if o is in vardict[v]['obssets']
            
            html += '<TR>'
            html += '    <TH ALIGN=LEFT>' + v
            html += '    <TH ALIGN=LEFT>' + vardict[v]['desc'] 
            
            for season in seasons:
                html += '    <TH ALIGN=LEFT><A href="#" onmouseover="set3_' + season + '_' + v + '_CRU_obsc\.png);" onmouseout="nodisplayImage();" onclick="set3_' + season + '_' + v + '_CRU_obsc\.png">plot</a>'
     #onclick="displayImageClick('set1_TOTRUNOFF\.gif');" onmouseover="displayImageHover('set1_TOTRUNOFF\.gif');" onmouseout="nodisplayImage();"
    
    
    
    return html


def set2(set,vars,times,package,dataset):
    
    html = ''

    html += '<p>'
    html += '<img src="../images/SET2.gif" border=1 hspace=10 align=left alt="set 2">'
    html += '<font color=maroon size=+3><b>'
    html += 't85f09.B1850 <br>and<br> OBS data'
    html += '</b></font>'
    html += '<p>'
    html += '<a href="../sets.htm">'
    html += '<font color=red><b>Back to diagnostic sets</b></font></a>'
    html += '<br clear=left>'
    html += '<p>'
    html += '<b>DIAG Set 2 - Line plots of annual implied transports<br> '
    html += '<hr noshade size=2 size="100%">'
    html += '<p>' 
    html += 'The computation of the implied northward transports follows the conventions described<br>'
    html += 'in the paper by <A HREF="http://www.cgd.ucar.edu/cas/papers/jclim2001a/transpts.html">Trenberth and Caron (2001)</A>. Their corrections applied to the southern<br>'
    html += 'oceans poleward of 30S are not used in the calculations, and the NCEP derived values<br>'
    html += 'plotted here are their unadjusted values. <A HREF="http://www.cgd.ucar.edu/cas/catalog/ohts/index.html">Webpage</A> about the NCEP derived data.<br>'
    html += 'A <A HREF="../images/ocean_masks.jpg">plot</A> of the ocean basins used in the calculations.'
    html += '</b>'
    
    html += '<p>'
    
    html += '<TABLE>'
    
    html += '<TR>'
    html += '    <TH ALIGN=LEFT>Annual Implied Northward Transports'
    html += '    <TH><BR>'
    
    html += '<TR>'
    html += '    <TH ALIGN=LEFT>Ocean Heat'
    html += '    <TH ALIGN=LEFT><A HREF="set2_OHT_obsc.png">plot</A>'
    
    html += '<TR>'
    html += '    <TH ALIGN=LEFT>Atmospheric Heat'
    html += '    <TH ALIGN=LEFT><A HREF="set2_AHT_obsc.png">plot</A>'
    
    html += '<TR>'
    html += '    <TH ALIGN=LEFT>Ocean Freshwater'
    html += '    <TH ALIGN=LEFT><A HREF="set2_OFT_obsc.png">plot</A>'
    
    html += '</TABLE>'

    return html



def set1(set,vars,times,package,dataset):
    
    html = ''
    
    html += '<img src="../images/3Dglobe.gif" hspace=10 align=left alt="3D globe">\n'
    html += '<p>\n'
    html += '<font color=maroon size=+3><b>\n'
    html += 't85f09.B1850 <br>and<br> OBS data\n'
    html += '</b></font>\n'
    html += '<p>\n'
    html += '<a href="../sets.htm">\n'
    html += '<font color=red><b>Back to diagnostic sets</b></font></a>\n'
    html += '<br clear=left>\n'
    html += '<p>\n'
    html += '<b>DIAG Set 1 - Tables of global, tropical, and extratropical<br>\n'
    html += 'DJF, JJA, ANN means and RMSE</b><br>\n'
    html += '<hr noshade size=2 size="100%">\n'
    
    html += '<TABLE>\n'
    
    html += '<TR>\n'
    html += '  <TH ALIGN=LEFT><font color=blue>Domain</font>\n'
    #print 'DJF: ' + str(('DJF' in times))
    for time in times:
        html += '  <TH>' + time + '\n'
    
    
    html += '<TR>\n'
    html += '  <TH ALIGN=LEFT>global'
    # GLOBAL OBS TABLE
    for time in times:
        html += '  <TH ALIGN=LEFT><A HREF="table_GLBL_' + time + '_obs.asc">table</a>\n'
    
    
    html += '<TR>\n'
    html += '  <TH ALIGN=LEFT>tropics (20S-20N)'
    # GLOBAL OBS TABLE
    for time in times:
        html += '  <TH ALIGN=LEFT><A HREF="table_TROP_' + time + '_obs.asc">table</a>\n'
        
    html += '<TR>\n'
    html += '  <TH ALIGN=LEFT>southern extratropics (90S-20S)'
    # 
    for time in times:
        html += '  <TH ALIGN=LEFT><A HREF="table_SEXT_' + time + '_obs.asc">table</a>'
        
    html += '<TR>\n'
    html += '  <TH ALIGN=LEFT>northern extratropics (20N-90N)'
    for time in times:
        html += '  <TH ALIGN=LEFT><A HREF="table_NEXT_' + time + '_obs.asc">table</a>'
    
    
    html += '</TABLE>'
    html += '\n'
                
    return html