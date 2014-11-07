def generate_token_url(filename):
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