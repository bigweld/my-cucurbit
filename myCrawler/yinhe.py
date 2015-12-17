# -*- coding: utf-8 -*-
import re
import urllib2
import os
import base64
import time
import random

class Yinhe:

    def __init__(self):
        self.domain = 'http://manhua.dmzj.com'
        self.img_host = 'http://images.dmzj.com'
        self.catalog_url = self.domain + '/yinheshouhuzhe/'
        self.keywords = ['yinheshouhuzhe']

    def getDataFromUrl(self,url):
        """get data(file like object) from url """
        #cache_name = url.replace('/','|') + '.cache'
        print url
        cache_name = base64.b64encode(url) + '.cache'
        if os.path.exists(cache_name):
            print 'date is from cache：%s' %cache_name 
        else:
            print 'data is from url'
            try:
                res = urllib2.urlopen(url)
                #print res
                with open(cache_name,'w') as f:
                    f.write(res.read())
            except Exception as e:
                print e
                return None
        return open(cache_name)

    def urlConcat(self,url1,url2):
        """concat two url as one with '/'"""
        return url1.rstrip('/') + '/' + url2.lstrip('/')
        
    def getUrlList(self):
        """get url list of each volume"""
        sub_urls = []
        res = self.getDataFromUrl(self.catalog_url)
        if res:
            catalog = res.read()
            catalog = catalog.replace(' ','')
            re_str = r'<a.*?href="(/.*?' + self.keywords[0] + '.*html)".*?<\/a>'
            print re_str
            sub_urls = re.findall(re_str,catalog,re.I)
            # for i in sub_urls:
            #     print i
            # else:
            #     print '----------this is over------------'
        return sub_urls

    def getImgsFromUrl(self,url):
        jses = self.getJsFromUrl(url)
        js = self.reformJs(jses[0])
        jsRes = self.executeJs(js)
        img_sub_urls = jsRes.split(',')
        print img_sub_urls
        for img_sub_url in img_sub_urls:
            try:
                img_dir_name = url.split('/')[-1].partition('.shtml')[0]
                if not os.path.isdir(img_dir_name):
                    os.mkdir(img_dir_name)
                img_name = img_sub_url.split('/')[-1]
                img_path = os.path.join(img_dir_name,img_name)
                if not os.path.exists(img_path):                   
                    img_url = self.urlConcat(self.img_host,img_sub_url)
                    res = urllib2.urlopen(img_url)
                    with open(os.path.join(img_dir_name,img_name),'wb') as f:
                        f.write(res.read())
                    res.close()
            except Exception as e:
                print e
                return None
        else:
            print '--Job done!--Dir:%s , %s pics' %(img_dir_name,len(img_sub_urls))
            

    def getJsFromUrl(self,url):
        res = self.getDataFromUrl(url)
        html = res.read()
        #html = html.replace(' ','')
        re_str = r'<script type="text/javascript">([\s\S]*?)</script>'
        js = re.findall(re_str,html,re.I)
        # for i in js:
        #     print i
        # else:
        #     print '-------this is over ------------'
        return js
        
    def executeJs(self,js):
        import PyV8
        #print js
        class MockDocument(object):

            def __init__(self):
                self.value = ''

            def write(self, *args):
                self.value += ''.join(str(i) for i in args)


        class Global(PyV8.JSClass):
            def __init__(self):
                self.document = MockDocument()


        scope = Global() # define a compatible javascript class
        ctx = PyV8.JSContext(scope) # create an context with the global object
        ctx.enter()
        ctx.eval(js)
        return scope.document.value
        # ctxt = PyV8.JSContext()          # create a context with an implicit global object
        # ctxt.enter()                     # enter the context (also support with statement)
        # ctxt.eval(js)                 # evalute the javascript expression
        
    def reformJs(self,js):
        rt = os.linesep + "document.write(arr_pages)"
        js = unicode(js + rt,'utf-8')
        return js
        
    def getAllImgs(self):
        sub_url_list = self.getUrlList()
        for sub_url in sub_url_list:
            self.getImgsFromUrl(self.urlConcat(demo.domain,sub_url))
            time.sleep(random.randint(1,5))

if "__main__" == __name__:
    demo = Yinhe()
    demo.getAllImgs()
    #sublist = demo.getUrlList()
    #last_url = sublist[0]
    #demo.getImgsFromUrl(demo.domain+last_url)
    #demo.getJsFromUrl(demo.domain+last_url)

