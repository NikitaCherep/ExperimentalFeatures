#!/usr/bin/python

import sys

from googleplay import GooglePlayAPI
from helpers import sizeof_fmt

# separator used by search.py, categories.py, ...
SEPARATOR = ";"

LANG = "en_US"  # can be en_US, fr_FR, ...
ANDROID_ID = None  # "xxxxxxxxxxxxxxxx" adb shell 'settings get secure android_id'
GOOGLE_LOGIN = None  # "username@gmail.com"
GOOGLE_PASSWORD = None
AUTH_TOKEN = None  # "yyyyyyyyy"


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0


# force the user to edit this file
if any([each == None for each in [ANDROID_ID, GOOGLE_LOGIN, GOOGLE_PASSWORD]]):
    raise Exception("config.py not updated")

if (len(sys.argv) < 2):
    print("Usage: %s packagename [filename]")
    print("Download an app.")
    print("If filename is not present, will write to packagename.apk.")
    sys.exit(0)

packagename = sys.argv[1]

if (len(sys.argv) == 3):
    filename = sys.argv[2]
else:
    filename = packagename + ".apk"

# Connect
api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

# Get the version code and the offer type from the app details
m = api.details(packagename)
doc = m.docV2
vc = doc.details.appDetails.versionCode
ot = doc.offer[0].offerType

# Download
print("Downloading %s..." % sizeof_fmt(doc.details.appDetails.installationSize))
data = api.download(packagename, vc, ot)
open(filename, "wb").write(data)
print("Done")
