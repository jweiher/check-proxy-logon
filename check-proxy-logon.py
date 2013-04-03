#!/usr/bin/env python


class ProxyChecker(threading.Thread):
    def __init__(self, user, password, proxy, fetchurl):
        super(self, ProxyChecker).__init__()
        self.user = user
        self.password = password
        self.proxy = proxy
        self.fetchurl = fetchurl
        
    @classmethod
    def get_proxy_opener(self, proxyurl, proxyuser, proxypass, proxyscheme='http'):
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, proxyurl, proxyuser, proxypass)

        proxy_handler = urllib2.ProxyHandler({proxyscheme: proxyurl})
        proxy_auth_handler = urllib2.ProxyBasicAuthHandler(password_mgr)
        return urllib2.build_opener(proxy_handler, proxy_auth_handler)
    
    def run(self):
        #try:
        url_opener = self.get_proxy_opener(
            self.proxy, 
            self.user, 
            self.password
        )
        url_opener.open(self.fetchurl)
        #except HTTPError:
        #    print "Logon failed: %s:%s" % (self.user, self.password)