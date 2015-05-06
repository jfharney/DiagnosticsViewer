from __future__ import absolute_import

from exploratory_analysis.celery import app


def issue_publish(request,x,y,user_id):
    
    import urllib2
    import urllib
    
    import sys
    print 'sys.path: ' + str(sys.path)
    
    
    sys.path.append('/Users/8xo/software/exploratory_analysis/DiagnosticsViewer/django-app/uvcdat_live/exploratory_analysis')
    
    from paths import paths
    
    
    esgf_hostname = paths.esgf_hostname
    esgf_port = paths.esgf_port

    print 'esgf_hostname: ' + esgf_hostname
    print 'esgf_port: ' + esgf_port
    
    print 'call the esgf publishing service here'
    
    payload = {'project': 'ACME', 
               'data_type': 'climo',
               'regridding' : 'bilinear',
               'realm' : 'atm',
               'experiment' : 'B1850C5e1_ne30',
               'range' : 'all',
               'versionnum' : 'v0_1' }
    
    
    
    
    username = user_id
    
    
    url = 'http://' + esgf_hostname + ':' + esgf_port + '/acme_services/publishing/publish_data/' + username #+ '/'
    
    print 'sending to url: ' + str(url) 
    
    # This urlencodes your data (that's why we need to import urllib at the top)
    data = urllib.urlencode(payload)

    # Send HTTP POST request
    request = urllib2.Request(url, data)

    response = urllib2.urlopen(request)
 
    html = response.read()
    
    

@app.task
def add(request,x, y,user_id):
    
    import time
    
    print 'starting task'
    #time.sleep(300)
    time.sleep(3)
    
    issue_publish(request,x,y,user_id)
    
    print 'ending task'
    
    
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)