# Quick and dirty python 3 script that syncs the linked zips of PGN files from the 
# the week in chess website http://theweekinchess.com/twic into the current
# folder.
# Optional argument: 
#     check -- compares file sizes of all existing files and eventually downloads again.

import sys
import urllib
import urllib.request
import re
import os.path

# Download helpers

def readUrl( url ):
  """ Return url contents"""
  with urllib.request.urlopen( url ) as response:
    return response.read()

def dlUrl( url , to = False ):
  """ Downloads url contents to file with the same name in current folder"""
  if not to:
    to = url.split("?")[0].split("/")[-1]
  with open( to , 'b+w' ) as f:
    f.write( readUrl( url ) )

def urlFilename (url):
  """ Gets filename of url """
  return url.split("?")[0].split("/")[-1]

def getUrlSize(url):
  """ Gets file size of url"""
  with urllib.request.urlopen(url) as response:
    return response.info()["Content-Length"]



# Website with linked files
twic = "http://theweekinchess.com/twic"
# Checks existing zips for same file size with server
# Quite a slow down (with my connection)
check = 'check' in sys.argv

twicindex = str(readUrl(twic))
# Filters all zip files of the pgn.
twicpgn = re.findall('href="?\'?([^"\'>]*zip)[>"\']*PGN', twicindex)
# Downloads 
for pgn in twicpgn:
  if not os.path.exists(urlFilename(pgn)) or ( check and not int(getUrlSize(pgn))==os.stat(urlFilename(pgn)).st_size):
    print(urlFilename(pgn)+" dowloading.")
    if os.path.exists(urlFilename(pgn)): 
        print("File sizes did not agree: twic: "+str(getUrlSize(pgn))+" local: "+ str(os.stat(urlFilename(pgn)).st_size))
    dlUrl(pgn)
  else:
    print(urlFilename(pgn)+" exists. Skipping")


