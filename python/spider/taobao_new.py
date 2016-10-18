#!--*--coding:utf-8--*--


import os
import sys
import urllib2
import re
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')


class Taobao:
    '''
    get tao bao mm photo
    '''
    def __init__(self,base_url,pagenum):
        self.base_url = base_url
        self.full_url = base_url + "?page=%d" % pagenum
        self.base_dir = os.path.join(os.getcwd(),'taobaomm')
        # 这是一些配置 关闭loadimages可以加快速度 但是第二页的图片就不能获取了打开(默认)
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        self.driver = webdriver.PhantomJS(desired_capabilities=cap,service_log_path=os.path.devnull)

    def get_page(self,url,print_std=False):
        '''
        get page str
        :return: str
        '''
        _headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        _request = urllib2.Request(url, headers=_headers)
        try:
            _response = urllib2.urlopen(_request)
            _content = _response.read().decode('gbk')
            #print content
            if print_std:
                print _content
            return _content
        except Exception,e:
            print e

    def get_base_info(self,print_std=False):
        '''
        get lady base info
        :return: list [(name,infourl,imgurl),]
        '''
        page_str = self.get_page(self.full_url)
        info_compile = re.compile('<div class="list-item">.*?<img src="(.*?)".*?>.*?<a class="lady-name" href="(.*?)".*?>(.*?)</a>',re.S)
        items = re.findall(info_compile,page_str)
        if print_std:
            print "#### mm info ####"
            for item in items:
                print "name: %s" % item[2]
                print "photo: %s" % item[0]
                print "info: %s" % item[1]
                print ""
        return items

    def get_detail_info(self,detail_url,print_std=False):
        self.driver.get(detail_url)
        detail_msg = self.driver.find_elements_by_xpath('//div[@class="mm-p-info mm-p-base-info"]/ul/li')
        img = self.driver.find_elements_by_xpath('//ul[@class="mm-p-menu"]/li/span/a')
        photo_url = img[0].get_attribute('href')
        # print photo_url
        #print img_url
        msg_list = [ item.text for item in detail_msg ]
        detail_str ='\n'.join(msg_list)
        print detail_str
        return { "photo_url": photo_url,"detail_msg": detail_str }

    def get_img_info(self,photo_url):
        '''

        :return: photo info list
        '''
        self.driver.get(photo_url)
        photo_elems = self.driver.find_elements_by_xpath('//div[@class="mm-photo-cell-middle"]/h4/a')
        photo_msg = [ (photo_elem.text,photo_elem.get_attribute('href')) for photo_elem in photo_elems ]
        for photo_elem in photo_elems:
            print photo_elem.text
            print ""
            print photo_elem.get_attribute('href')
        #print photo_msg
        return photo_msg

    def get_img_url(self,img_url,print_std=False):
        '''
        get img url
        :param img_url:
        :return: img url list
        '''
        self.driver.get(img_url)
        img_elems = self.driver.find_elements_by_xpath('//div[@class="mm-photoimg-area"]/a/img')
        img_url_list = [ img_elem.get_attribute('src') for img_elem in img_elems ]
        for img in img_elems:
            if print_std:
                print img.get_attribute('src')
                print ""
        return img_url_list

    def save_info(self,infopath,info_str):
        '''

        :param info_str:
        :return:
        '''
        infofile = os.path.join(infopath,'baseinfo.txt')
        with open(infofile,'w+') as f:
            f.write(info_str)


    def save_img(self,imgfile,imgurl):
        '''
        save img
        :param img:
        :param explain:
        :return:
        '''
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        request = urllib2.Request(imgurl, headers=headers)
        response = urllib2.urlopen(request)
        with open(imgfile,'wb') as f:
            f.write(response.read())

    def makedir(self,pdir):
        '''
        make dir
        :param pdir:
        :param cdir:
        :return: bool
        '''

        if not os.path.exists(pdir):
            os.mkdir(pdir)

    def drive_quit(self):
        '''
        driver quit
        :return:
        '''
        self.driver.quit()

if __name__ == "__main__":
    taobao = Taobao('https://mm.taobao.com/json/request_top_list.htm',1)
    mm_base_info = taobao.get_base_info(print_std=False)
    taobao.makedir(taobao.base_dir)
    for base_info in mm_base_info:
        name_dir = os.path.join(taobao.base_dir, base_info[2])
        taobao.makedir(name_dir)
        full_detail_url = 'http:' + base_info[1]
        detail_info = taobao.get_detail_info(full_detail_url)
        name_dir = os.path.join(taobao.base_dir,base_info[2])
        taobao.save_info(name_dir,detail_info['detail_msg'])
        photo_url = detail_info['photo_url']
        photo_msg = taobao.get_img_info(photo_url)
        img_id = 1
        for msg in photo_msg:
            img_url = msg[1]
            img_list = taobao.get_img_url(img_url,print_std=True)
            for img_msg in img_list:
                imgfile = '%d.jpg' % img_id
                imgpath = os.path.join(name_dir,imgfile)
                img_id  = img_id + 1
                try:
                    taobao.save_img(imgpath,img_msg)
                except IOError,e :
                    print e





