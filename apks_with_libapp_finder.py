"""
Android App Bundles have multiple APKs which may not include native libraries even when combined into one single base APK.
In this case it is necessary to find which APK does contain the Flutter's libapp.so libraries.
This script - given a directory where all APKs are stored - prints a list of all APKs in that folder that are found to contain the Flutter's libapp.so libraries.
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from pathlib import Path
import sys
import pexpect
import time

def browse_dir(dir_str):
  pathlist = Path(dir_str).rglob('*.apk')
  apks_found = []
  for path in pathlist:
     # because path is object not string
     filename = str(path)
     print('Running reflutter on {}'.format(filename))
     ret = attempt(filename)
     if ret:
       apks_found.append(ret)
  return apks_found

def attempt(filename):
    apks_found = []
    proc = pexpect.spawnu('reflutter {}'.format(filename))
    proc.sendline('2')
    time.sleep(10)
    ind = proc.expect_exact(['Is this really a Flutter app', pexpect.TIMEOUT])
    if ind == 1:
      return filename
    return ''


if __name__ == '__main__':
  if len(sys.argv) != 2:
        print('usage: {} <directory that includes all APKs>'.format(sys.argv[0]))
        sys.exit(1)
  apks_found = browse_dir(sys.argv[1])
  print('The following APKs in {} were found to contain libapp.so'.format(sys.argv[1]))
  for apk in apks_found:
    print(apk)
