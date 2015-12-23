# -*- coding: utf-8 -*-

"""
This script is used to get imags from newsmth site in MyPhoto board
"""

import re
import urllib2
import os
import base64
import time
import random

class myPhoto():
    def __init__(self,stored_path):
        self.domain = 'http://www.newsmth.net'
        self.catalog_url = 'http://www.newsmth.net/nForum/board/MyPhoto?ajax&p=2'
        self.keywords = ['nForum','article','MyPhoto','\d{7}']
        self.stored_path = stored_path
    
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
            #re_str = r'<a.*?href="(/.*?' + self.keywords[0] + '.*html)".*?<\/a>'
            re_str = r'<a target="_blank" href="(/' + '/'.join(self.keywords) + ')".*?</a>'
            print re_str
            sub_urls = re.findall(re_str,catalog,re.I)
            for i in sub_urls:
                print i
            else:
                print '----------this is over------------'
        return sub_urls

    def getImgUrlsFromUrl(self,url):
        sub_urls = []        
        res = self.getDataFromUrl(url)
        img_domain = 'http://att.newsmth.net/nForum/att/MyPhoto'
        article_id = url.split('/')[-1]
        if res:
            catalog = res.read()
            re_str = r'<a target="_blank" href="(' +img_domain +'/'+ article_id +'/\d{6})".*?<\/a>'
            print re_str
            sub_urls = re.findall(re_str,catalog,re.I)
            for i in sub_urls:
                print i
            else:
                print '----------this is over------------'
        return sub_urls

        

    def getImgsFromUrl(self,url):
        img_sub_urls = self.getImgUrlsFromUrl(url)
        print img_sub_urls
        for img_sub_url in img_sub_urls:
            try:
                # img_dir_name = url.split('/')[-1].partition('.shtml')[0]
                # if not os.path.isdir(img_dir_name):
                #     os.mkdir(img_dir_name)
                img_name = img_sub_url.split('/')[-1] + '.jpg'
                img_path = os.path.join(self.stored_path,img_name)
                if not os.path.exists(img_path):                   
                    #img_url = self.urlConcat(self.img_host,img_sub_url)
                    res = urllib2.urlopen(img_sub_url)
                    with open(img_path,'wb') as f:
                        f.write(res.read())
                    res.close()
            except Exception as e:
                print e
                return None
        else:
            print '--Job done!--Dir:%s , %s pics' %(self.stored_path,len(img_sub_urls))

    def getAllImgs(self):
        sub_url_list = self.getUrlList()
        for sub_url in sub_url_list:
            self.getImgsFromUrl(self.urlConcat(demo.domain,sub_url))
            time.sleep(random.randint(1,5))



if "__main__" == __name__:
    demo = myPhoto('C:\Users\wangwei2\Pictures\desktopBg')
    demo.getAllImgs()
