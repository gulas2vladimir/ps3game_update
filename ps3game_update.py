# -*- coding: utf-8 -*-

import os
import sys
import urllib2
import socket
import platform
import re
from xml.dom.minidom import parse

socket.setdefaulttimeout(5.0)

mac = (platform.system() == 'Darwin')

def help():
    print sys.argv[0] + " --scan <dir>, or --id titleid titleid ..."
    sys.exit(1)

def get_url(titleid):
    url = "https://a0.ww.np.dl.playstation.net/tpl/np/%s/%s-ver.xml" % (titleid, titleid)
    try:
        dom = parse(urllib2.urlopen(url))
        for elements in dom.getElementsByTagName('package'):
            for element in elements.toxml().split():
                if 'url' in element:
                    return element.split("\"")[1]
    except:
        return False

def get_pkg(downurl):
    if mac:
        os.system("/usr/bin/curl -O '%s'" % (downurl))
    else:
        os.system("/usr/bin/wget '%s'" % (downurl))

def main(argv):
    if argv[0] == "--id":
        for title in range(1, len(argv)):
            titleid = argv[int(title)]
            downurl = get_url(titleid)
            if downurl:
                print("%s - Downloading" % (titleid))
                get_pkg(downurl)
            else:
                print("%s - No update available" % (titleid))

    if argv[0] == "--scan":
        for title in os.listdir('%s' % argv[1]):
            titleid = re.search('^BL[0-9A-Z]{7}', title)
            if titleid:
                downurl = get_url(titleid.group())
                if downurl:
                    print("%s - Downloading" % (titleid.group()))
                    get_pkg(downurl)
                else:
                    print("%s - No update available" % (titleid.group()))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        help()
        sys.exit(2)
    else:
        main(sys.argv[1:])

sys.exit(0)
