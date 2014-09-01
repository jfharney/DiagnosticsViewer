#location and name of the db being used (in settings.py)
databases_name = '/home/user/Desktop/AptanaWorkspace/db/mydb.db'
#databases_name = '/Users/i7j/sqlite3/mydb.db'

#location of the cloned project 
#${DiagnosticsViewer_home}/django-app/uvcdat-live
#uvcdat_live_root = '/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/' 
uvcdat_live_root = '/home/user/Desktop/AptanaWorkspace/DiagnosticsViewer/django-app/uvcdat_live/' 
databases_name = '/home/user/Desktop/AptanaWorkspace/db/mydb.db'

#databases_name = '/Users/bs1/uvcdat-devel/db/mydb.db'

#location of the cloned project 
#${DiagnosticsViewer_home}/django-app/uvcdat-live
#uvcdat_live_root = '/Users/bs1/uvcdat-devel/DiagnosticsViewer/django-app/uvcdat_live/' 
#uvcdat_live_root = '/Users/i7j/DiagnosticsViewer/django-app/uvcdat_live/' 
uvcdat_live_root = '/home/user/Desktop/AptanaWorkspace/DiagnosticsViewer/django-app/uvcdat_live/' 


#location of the static files directory used (in settings.py)
#staticfiles_dirs = "/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/static/exploratory_analysis",
staticfiles_dirs = uvcdat_live_root + 'exploratory_analysis/static/exploratory_analysis'
    
#location of the template directory used (in settings.py)
#template_dirs = "/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis/templates/exploratory_analysis"
template_dirs = uvcdat_live_root + 'exploratory_analysis/templates/exploratory_analysis'


message_reader_template_dirs = uvcdat_live_root + 'message_reader/templates/message_reader'




