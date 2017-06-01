import os
import sys

from dropbox.client import DropboxClient

# get an access token, local (from) directory, and Dropbox (to) directory
# from the command-line
local_path = '/home/nikhil/data_zipped.zip'
dropbox_path = 'data'
access_token = '<put it here>'

client = DropboxClient(access_token)

# enumerate local files recursively
with open(local_path, 'rb') as f:
    client.put_file(dropbox_path, f)
