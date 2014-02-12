#location and name of the db being used (in settings.py)
databases_name = '/Users/8xo/sqlite3/11-3/mydb.db'

#location of the cloned project 
#${DiagnosticsViewer_home}/django-app/uvcdat-live
uvcdat_live_root = '/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/' 

#location of the static files directory used (in settings.py)
#staticfiles_dirs = "/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis",
staticfiles_dirs = uvcdat_live_root + 'exploratory_analysis/static/exploratory_analysis'
    
#location of the template directory used (in settings.py)
#template_dirs = "/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/templates/exploratory_analysis"
template_dirs = uvcdat_live_root + 'exploratory_analysis/templates/exploratory_analysis'


message_reader_template_dirs = uvcdat_live_root + 'message_reader/templates/message_reader'