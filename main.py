# -*- coding: utf-8 -*-
"""
# Talk is cheap,show me the codes!

@Author billie
@Time 2020/6/24 9:59 下午
@Describe 

下载dynamicwallpaper.club网站的全部动态壁纸

"""

import requests,re,os,time
from lxml import etree

class Dynamicwallpaper():
    def __init__(self):
        self.session = requests.Session()
        self.base_url = 'https://dynamicwallpaper.club'
        self.headers = {
            # ':authority': 'firebasestorage.googleapis.com',
            # ':method': 'GET',
            # ':path': '/v0/b/dynamic-wallpapers-6a7ab.appspot.com/o/wallpapers%2Fdgvrihxpu2h%2FBig%20Sur.heic?alt=media&token=38f034ba-5ebb-4891-b483-35f0a82476cd',
            # ':scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
            'if-none-match': '"49f2189cda443d359fece82b4e718585"',
            'origin': 'https://dynamicwallpaper.club',
            'referer': 'https://dynamicwallpaper.club/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'x-client-version': 'Chrome/JsCore/5.11.0/FirebaseUI-web',
            'x-firebase-locale': 'en'
        }
        self.page=1

    #登陆账号
    def Login(self):
        #访问一下主页，避免出错
        self.session.get(self.base_url,headers=self.headers)#
        login_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyCUkVhGO7AAD4iob6WzX8JX2El2Nh1f02o'
        login_data={
            'email': "2380540710@qq.com",
            'password': "a1222222222", #别客气，拿去用
            'returnSecureToken': 'true'
            }
        #发送登录请求
        r=self.session.post(url=login_url,data=login_data,headers=self.headers)
        print(r.text)
        #处理一下返回的信息，并保存到self.key变量
        self.key=eval(r.text.replace('true','"true"'))


    #获取必要参数id
    def get_ids(self,page_url):
        r=self.session.get(url=page_url,headers=self.headers.update(self.key))
        ids=re.findall('/wallpaper/(.+)" class="link" data-v-4cc897c2>',r.text)
        return ids

    #获取壁纸的名字
    def get_names(self,page_url):
        r = self.session.get(url=page_url, headers=self.headers.update(self.key))

        html = etree.HTML(r.text)
        names = html.xpath('//*[@id="app"]/div[2]/div[2]/div/div/div[1]/div/div/div[2]/p/a')

        # 稍微把名字字段处理一下
        names = [i.text.replace('\n', '').strip(' ').replace(' ', '%20') for i in names]
        return names

    #获取必要参数token
    def get_token(self,id,name):
        try:
            url='https://firebasestorage.googleapis.com/v0/b/dynamic-wallpapers-6a7ab.appspot.com/o/wallpapers%2F{}%2F{}.heic'.format(id,name)
            r=self.session.get(url=url,headers=self.headers)
            token=r.json()['downloadTokens']
        except:
            url='https://firebasestorage.googleapis.com/v0/b/dynamic-wallpapers-6a7ab.appspot.com/o/wallpapers%2F{}%2F{}%20.heic'.format(id,name)
            r=self.session.get(url=url,headers=self.headers)
            token = r.json()['downloadTokens']
        return token

    # 获取真实的动态壁纸下载链接true_heic_url
    def get_true_heic_url(self,page_url):
        #三个必要参数
        ids = self.get_ids(page_url) #参数1、id
        self.names = self.get_names(page_url) #参数2、name
        true_heic_urls=list()

        for i in range(len(self.names)):
            token = self.get_token(ids[i], self.names[i]) #参数3、token
            true_heic_urls.append('https://firebasestorage.googleapis.com/v0/b/dynamic-wallpapers-6a7ab.appspot.com/o/wallpapers%2F{}%2F{}.heic?alt=media&token={}'.format(ids[i],
                                                                                                                                                                           self.names[i],
                                                                                                                                                                           token))
        return true_heic_urls

    # 这是专门负责下载的模块，「支持显示下载进度条」
    def download(self, path, name, type, href):  #
        if not os.path.exists(path): os.mkdir(path)
        print("\n[正在下载]：{}".format(name))

        # 发送请求
        r = requests.get(href, stream=True, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'})

        size = 0
        chunk_size = 1024  # 每次下载的数据大小
        try:
            content_size = int(r.headers['content-length'])  # 总大小
        except:
            content_size = int(r.headers['x-goog-stored-content-length'])  # 总大小
        # print(content_size,r.status_code,r.content,r.text)
        # if r.status_code == 200:
        print("[文件大小]：{:.2f} MB".format(content_size / chunk_size / 1024))  # 换算单位
        with open(path + '/' + name + '.' + type, "wb")as f:
            for data in r.iter_content(chunk_size=chunk_size):
                f.write(data)
                size += len(data)  # 已下载文件大小
                print('\r' + '[下载进度]：{} {:.1f}%'.format('>' * int(size * 50 / content_size),
                                                        float(size / content_size * 100)), end='')

    #开始下载当前页面的所有heic文件
    def download_one_page(self,page_url='https://dynamicwallpaper.club/gallery?section=new'):
        print('[{}]正在下载第「{}」页:'.format(time.strftime('%H:%M:%S'),self.page),page_url)
        true_heic_urls = self.get_true_heic_url(page_url=page_url)

        #开始下载
        f = open('true_heic_urls.txt','w',encoding='utf-8')
        for i,url in enumerate(true_heic_urls):
            #方式1、直接下载，需连接vpn下载
            # self.download('./heics',self.names[i],'heic',url)j

            #方式2、把下载链接保存到本地，之后读取下载链接进行下载，同样需要连接vpn
            f.write(self.names[i].replace('%20',' ')+'#'+url+'\n')

        #获取页面信息
        r = requests.get(url = page_url,headers = self.headers.update(self.key))
        html = etree.HTML(r.text)

        #看看还有没有下一页
        try:
            next_page_url = self.base_url\
                        +\
                        html.xpath('//a[@class="link bright featured"]/@href')[0]
            self.page+=1
            self.download_one_page(page_url=next_page_url)
        except:
            print('finish')

    #从本地保存的txt文件读取下载连接，并下载
    def DL_from_txt(self):
        for i in open('./true_heic_urls.txt', 'r', encoding='utf-8').readlines():
            name, url = i.split('#')
            if os.path.exists('./heics/{}.heic'.format(name)):continue
            self.download('./heics', name, 'heic', url)

    #把下载链接保存为html文件
    def deal_with_txt(self):
        with open('./true_heic_urls.html','w',encoding='utf-8') as f:
            f.write('<html><head><title>请科学上网！</title><meta charset="utf-8"></head>\n<body>\n')
            f.write('<p>壁纸名称&nbsp|&nbsp下载链接</p>\n')
            for i in open('./true_heic_urls.txt', 'r', encoding='utf-8').readlines():
                print(i)
                name, url = i.split('#')
                f.write('<p>'+name+':  <a href="{}">'.format(url)+'{}...</a>'.format(url[:20])+'</p>\n')
            f.write('\n</body>\n</html>')

if __name__ == '__main__':
    billie = Dynamicwallpaper()
    # billie.Login()
    # billie.download_one_page()
    # billie.DL_from_txt()
    billie.deal_with_txt()
