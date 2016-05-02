#!/bin/bash


source /etc/esg.env
export ESGINI=/esg/config/esgcet/esg.ini

mkdir -p ~/.globus

# Username from OpenID
# Path to globus cert should be placed in current users home directory
/usr/local/globus/bin/myproxy-logon -s esg.ccs.ornl.gov -l mayerbw -p 7512 -o ~/.globus/certificate-file

# Project name
# temp file (acme.txt) - TODO modify to write <project><datetime>.txt
# Project Path
esgscan_directory --project ACME -o acme.txt /data/acme/projects/ACME/


# Project name
# temp filename
esgpublish --map ./acme2.txt --project ACME --service fileservice


# Project name
# temp filename
esgpublish --map ./acme2.txt --project ACME --noscan --thredds --publish --service fileservice

