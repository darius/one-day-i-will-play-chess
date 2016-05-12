"""
Interact with the NGW chess server.
"""

import requests, sys, time

from chack import *

stem = 'http://52.200.188.234:3000/test/'

def main(argv):
    assert len(argv) == 3
    game = argv[1]
    color = argv[2]
    url = stem + game

    while True:
        r = requests.get(url)
        if r.status_code != 200:
            print 'oh noes', r
            time.sleep(0.5)
            continue
        js = r.json()
        print js
#        try:
#        except 
        
        break


def testme(argv):
    url = stem + '4'

    r = requests.get(url)
    print r.status_code
    print r.json()

    r = requests.post('%s?move=%s' % (url, 'e4'))
    print r.status_code
    print r.json()

if __name__ == '__main__':
    testme(sys.argv)
