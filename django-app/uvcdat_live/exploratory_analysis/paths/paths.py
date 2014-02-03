####related to settings.py####
databases_name = '/Users/i7j/sqlite3/mydb.db'

staticfiles_dirs = "/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis",
    
template_dirs = "/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/templates/exploratory_analysis"
####end related to settings.py####


#path to uvcmetric python code
syspath_append_uvcmetrics = '/Users/i7j/uvcmetrics/src/python'

#path to cdscan (in uvcdat)
syspath_append_cdscan = '/Users/i7j/build-uvcdat/install/Library/Frameworks/Python.framework/Versions/2.7/bin/cdscan'

#path to "cache", i.e. place to store figures and json files for d3 renderings
cache_dir = '/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/cache/'

#path for front end to access cache (can't be a local path)
front_end_cache_dir = '../../../static/cache/'

#directory holding netcdf datasets
default_sample_data_dir = '/Users/i7j/Dropbox/data/tropics_warming_th_q_clm2'



img_cache_path = '/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache/'



timeseries_cache_path = '/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/cache'

generated_img_path = '/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis/img/treeex/'