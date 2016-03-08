


def generate_token_url(filename):
    import os, time, hashlib
    
    secret = "secret string"#config.get("options","secret_key")
    protectedPath = "/acme-data/"#config.get("options", "protectedPath")
    
    
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


#Belongs in a common utils package
def isLoggedIn(request,user_id):
    print '\n\n\nIN isLoggedIn'
    print 'user: ' + str(request.user)
    print 'user_id: ' + user_id
    loggedIn = False
    
    if (str(request.user) == str(user_id)):
        loggedIn = True
        
    
    #take out when putting security back in
    #loggedIn = True
    
    
    return loggedIn
