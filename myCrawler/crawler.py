# -*- coding: utf-8 -*-

import urllib2
import pdb

class Crawler:
    def __init__(self):
        self.url = 'http://manhua.dmzj.com/yinheshouhuzhe/21962.shtml'
        self.img_base_url = 'http://images.dmzj.com/y/%E9%93%B6%E6%B2%B3%E5%AE%88%E6%8A%A4%E8%80%85/1/'
        self.img_book_name = 'Guardians%20of%20the%20Galaxy'
        self.img_book_chapter_prefix = '0.1-'
        self.img_suffix = '.jpg'
        self.file_name = '21962.html'

    def getData(self):
        #res = urllib2.urlopen(self.url)
        #img_url = self.img_base_url + self.img_book_name + self.img_book_chapter_prefix #0.1
        #img_url = 'http://images.dmzj.com/y/%E9%93%B6%E6%B2%B3%E5%AE%88%E6%8A%A4%E8%80%85/%E7%AC%AC01%E5%8D%B7/Guardians%20of%20the%20Galaxy%20v3%20001-'
        #img_url = 'http://images.dmzj.com/y/%E9%93%B6%E6%B2%B3%E5%AE%88%E6%8A%A4%E8%80%85/100%E5%91%A8%E5%B9%B4/100th%20Anniversary%20Special%20-%20Guardians%20of%20the%20Galaxy%20001-'
        img_url = 'http://images.dmzj.com/y/%E9%93%B6%E6%B2%B3%E5%AE%88%E6%8A%A4%E8%80%85/%E7%AC%AC08%E5%8D%B7/Guardians%20of%20the%20Galaxy%20v3%23008-'+%s+'-FearlessCHS.jpg'
        self.img_book_chapter_prefix = '008-' 
        for i in range(100):
            part  = "%03d" %i
            print part
            #url = img_url + part + self.img_suffix
            url = img_url % str(part)
            file_name = self.img_book_chapter_prefix + part + self.img_suffix
            print url
            try:
                res = urllib2.urlopen(url)
                with open(file_name,'w') as f:
                    f.write(res.read())
            except Exception as e:
                print e
                break
        

if "__main__" == __name__:
    #pdb.set_trace()
    demo = Crawler()
    demo.getData()

