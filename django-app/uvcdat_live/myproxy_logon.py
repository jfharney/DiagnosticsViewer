import os
import socket
from OpenSSL import crypto, SSL

class GetException(Exception): pass
class RetrieveProxyException(Exception): pass

debug = 0
def debuglevel(level):
    global debug
    return debug >= level

def create_cert_req(keyType = crypto.TYPE_RSA,
                    bits = 1024,
                    messageDigest = "md5"):
    
    print 'in create cert'
    """
    Create certificate request.
    Returns: certificate request PEM text, private key PEM text
    """
    # Create certificate request
    req = crypto.X509Req()
    # Generate private key
    pkey = crypto.PKey()
    pkey.generate_key(keyType, bits)
    req.set_pubkey(pkey)
    req.sign(pkey, messageDigest)
    return (crypto.dump_certificate_request(crypto.FILETYPE_ASN1,req),
            crypto.dump_privatekey(crypto.FILETYPE_PEM,pkey))

def myproxy_logon_py(hostname,username,passphrase,outfile,lifetime=43200,port=7512):
    
    print 'hostname: ' + hostname
    print 'username: ' + username
    print 'passphrase: ' + passphrase
    print 'outfile: ' + outfile
    print 'lifetime: ' + str(lifetime)
    print 'port: ' + str(port)
    
    context = SSL.Context(SSL.SSLv3_METHOD)

    # disable for compatibility with myproxy server (er, globus)
    # globus doesn't handle this case, apparently, and instead
    # chokes in proxy delegation code
    context.set_options(0x00000800L)

    # connect to myproxy server
    if debuglevel(1): print "debug: connect to myproxy server"
    conn = SSL.Connection(context,socket.socket())
    conn.connect((hostname,port))

    # send globus compatibility stuff
    if debuglevel(1): print "debug: send globus compat byte"
    conn.write('0')
    
    # process server response
    
    if debuglevel(1): print "debug: get server response"
    print 'am i here 1'
    dat = conn.recv(8192)
    print 'am i here 2'
    if debuglevel(1): print dat
    response,errortext = deserialize_response(dat)
    print 'am i here 3'
    if response:
        raise GetException(errortext)
    else:
        if debuglevel(1): print "debug: server response ok"
    
        
    
    
    # generate and send certificate request
    # - The client will generate a public/private key pair and send a
    # NULL-terminated PKCS#10 certificate request to the server.
    if debuglevel(1): print "debug: send cert request"
    certreq,privatekey = create_cert_req()
    conn.send(certreq)
    
    # process certificates
    # - 1 byte , number of certs
    dat = conn.recv(1)
    numcerts = ord(dat[0])
    
    
    # - n certs
    if debuglevel(1): print "debug: receive certs"
    dat = conn.recv(8192)
    if debuglevel(2):
        print "debug: dumping cert data to myproxy.dump"
        f = file('myproxy.dump','w')
        f.write(dat)
        f.close()
    

myproxy_logon = myproxy_logon_py    

if __name__ == '__main__':
    import sys
    import optparse
    import getpass
    
    print 'hello'
    
    parser = optparse.OptionParser()
    
    parser.add_option("-s", "--pshost", dest="host",
                      help="The hostname of the MyProxy server to contact")
    parser.add_option("-p", "--psport", dest="port", default=7512,
                      help="The port of the MyProxy server to contact")
    parser.add_option("-l", "--username", dest="username",
                      help="The username with which the credential is stored on the MyProxy server")
    parser.add_option("-o", "--out", dest="outfile",
                      help="The username with which the credential is stored on the MyProxy server")
    parser.add_option("-t", "--proxy-lifetime", dest="lifetime", default=43200,
                      help="The username with which the credential is stored on the MyProxy server")
    parser.add_option("-d", "--debug", dest="debug", default=0,
                      help="Debug mode: 1=print debug info ; 2=print as in (1), and dump data to myproxy.dump")

    (options,args) = parser.parse_args()
    
    debug = options.debug

    # process options
    '''
    host = options.host
    if not host:
        print "Error: MyProxy host not specified"
        sys.exit(1)
    print 'host: ' + host
    '''
    host = 'esg.ccs.ornl.gov'
    
    '''
    port = int(options.port)
    username = options.username
    if not username:
        if sys.platform == 'win32':
            username = os.environ["USERNAME"]
        else:
            import pwd
            username = pwd.getpwuid(os.geteuid())[0]
    lifetime = int(options.lifetime)
    '''
    port = 7512
    username = 'jfharney'
    lifetime = 43200
    
    '''
    outfile = options.outfile
    if not outfile:
        if sys.platform == 'win32':
            outfile = 'proxy'
        elif sys.platform in ['linux2','darwin']:
            outfile = '/tmp/x509up_u%s' % (os.getuid())
    elif outfile.lower()=="stdout":
        outfile = sys.stdout
        
    '''   
    
    outfile = '/tmp/x509up_u%s' % (os.getuid())
    
    # Get MyProxy password
    #passphrase = getpass.getpass()

    passphrase = 'Mattryan12'
    
    
    # Retrieve proxy cert
    try:
        ret = myproxy_logon(host,username,passphrase,outfile,lifetime=lifetime,port=port)
        print "A proxy has been received for user %s in %s." % (username,outfile)
    except Exception,e:
        if debuglevel(1):
            import traceback
            traceback.print_exc()
        else:
            print "Error:", e
    
    
    
    
    
    
    