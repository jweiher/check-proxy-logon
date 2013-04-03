#!/usr/bin/env python
from Queue import Empty
from urllib2 import HTTPError
import Queue
import csv
import sys
import threading
import urllib2

accounts = Queue.Queue()


class ProxyChecker(threading.Thread):
    @classmethod
    def get_proxy_opener(self, proxyurl, proxyuser, proxypass, proxyscheme='http'):
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, proxyurl, proxyuser, proxypass)

        proxy_handler = urllib2.ProxyHandler({proxyscheme: proxyurl})
        proxy_auth_handler = urllib2.ProxyBasicAuthHandler(password_mgr)
        return urllib2.build_opener(proxy_handler, proxy_auth_handler)

    def run(self):
        while True:
            try:
                proxy, user, password, url = accounts.get(True, 1)
                url_opener = self.get_proxy_opener(
                    proxy,
                    user,
                    password
                )
                try:
                    url_opener.open(url)
                except HTTPError as e:
                        if e.code == 407:
                            print "Logon not working: %s:%s" % (user, password)
                        else:
                            print "Unknown Error: %s" % (e.msg)
                accounts.task_done()
            except Empty:
                break


def main():
    if len(sys.argv) != 4:
        print "Usage: %s proxy url file" % (sys.argv[0])
        sys.exit(1)
    for x in range(5):
        ProxyChecker().start()
    with open(sys.argv[3], 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 3:
                item = (sys.argv[1], row[1], row[2], sys.argv[2])
                accounts.put(item)
    accounts.join()


if __name__ == '__main__':
    main()
