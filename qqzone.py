#-*-coding:utf-8-*-
"""
@ author: Msky
@ QQ: 690126048
@ github: https://github.com/zhangmingming-chb

"""
import re
import json
import requests
import time
import base64
import random
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Base(object):

    def __init__(self, cookie=None):
        if cookie is not None:
            # QQ空间登录后生成的cookie
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400",
                # "cookie":"uin=o0643659318; skey=@qPVhxpWou; RK=lVx5oKuWer; ptcz=d370dec5e7976d538a5f17560dbbd0e5d72ddeb36fc2dc5f5364bb6e28b89cbb; p_uin=o0643659318; Loading=Yes; qz_screen=1280x720; pgv_pvid=7423879328; pgv_info=ssid=s6984390762; QZ_FE_WEBP_SUPPORT=1; __Q_w_s__QZN_TodoMsgCnt=1; pt4_token=ny*7Gvepiy7KDFnS94jcZ-zU1SnLCEDFD1xjGl9qBd8_; p_skey=EtLZnra*GdslIRDl*4nn47TOJRRRniYwtshyHvmWUm0_; cpu_performance_v8=7",
            }
            self.s_cookie = cookie
            self.d_cookie = self.s_d_cookie(cookie)
            self.login_cookie = self.d_cookie
            self.uin = re.findall("uin=(.*?);", cookie)[0]
            self.skey = re.findall("skey=(.*?);", cookie)[0]
            self.p_uin = re.findall("p_uin=(.*?);", cookie)[0]
            self.p_skey = re.findall("p_skey=(.*?);", cookie)[0]
            self.pt4_token = re.findall("pt4_token=(.*?);", cookie)[0]
            # self.uin:o0690126048
            self.qq = self.uin[2:]
        else:
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
            }
            self.scan_login()
            self.d_cookie = self.login_cookie
            self.s_cookie = self.d_s_cookie(self.d_cookie)
            self.uin = self.login_cookie['uin']
            self.skey = self.login_cookie['skey']
            self.p_uin = self.login_cookie['p_uin']
            self.p_skey = self.login_cookie['p_skey']
            self.pt4_token = self.login_cookie['pt4_token']
            # self.uin:o0690126048
            self.qq = self.uin[2:]
            # print(self.s_cookie)
            save_cookie = {
                self.qq: self.s_cookie
            }
            with open("cookie.json", "w") as f:
                json.dump(save_cookie, f)

    # 字典cookie转为字符串cookie
    def d_s_cookie(self, d_cookie):
        s_cookie = str()
        for k, v in d_cookie.items():
            s_cookie += f"{k}={v}; "
        return s_cookie

    # 字符串cookie转为字典cookie
    def s_d_cookie(self, s_cookie):
        # cookie去除前后可能存在的空字符
        s_cookie = s_cookie.strip()
        d_cookie = dict()
        # cookie最后的一对键值后面不存在“;”时
        if s_cookie[-1] != ';':
            cookie_item = s_cookie.replace(' ', '').split(';')
            a = list(map(lambda x: x.split('='), cookie_item))
            for i in a:
                d_cookie[i[0]] = i[1]
            return d_cookie
        # cookie最后的一对键值后面存在“;”时
        else:
            cookie_item = s_cookie.replace(' ', '').split(';')
            cookie_item.remove('')
            a = list(map(lambda x: x.split('='), cookie_item))
            for i in a:
                d_cookie[i[0]] = i[1]
            return d_cookie

    # 生成检测接口需要的cookie
    def _make_cookie_param(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Referer": "https://i.qq.com/?rd=1",
            "Cookie": "_qz_referrer=user.qzone.qq.com"
        }
        r = requests.get(
            "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html&pt_no_auth=1",
            headers=headers)
        # 客户端IP记录
        self.pt_clientip = dict(r.cookies)['pt_clientip']
        self.pt_guid_sig = dict(r.cookies)['pt_guid_sig']
        self.pt_local_token = dict(r.cookies)['pt_local_token']
        # 登录标记
        self.pt_login_sig = dict(r.cookies)['pt_login_sig']
        # 服务端IP记录
        self.pt_serverip = dict(r.cookies)['pt_serverip']
        # 参数uikey
        self.uikey = dict(r.cookies)['uikey']

    # 获取登录二维码，生成qrsign
    def _make_qrsig(self):
        r = requests.get(
            f"https://ssl.ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t={random.random()}&daid=5&pt_3rd_aid=0")
        # 保存登录二维码
        with open("login.png", "wb") as f:
            f.write(r.content)
        qrsig = dict(r.cookies)['qrsig']
        # 返回qrsig的值
        return qrsig

    # 扫码登录所需参数ptqrtoken
    def _make_ptqrtoken(self, qrsign):
        n = 0
        for s in qrsign:
            n += (n << 5) + ord(s)
        ptqrtoken = n & 2147483647
        return ptqrtoken

    # 生成ptdrvs
    def _make_ptdrvs(self, login_sig):
        r = requests.get(
            f"https://ssl.ptlogin2.qq.com/check?regmaster=&pt_tea=2&pt_vcode=1&uin=123456789&appid=549000912&js_ver=20021917&js_type=1&login_sig={login_sig}&u1=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&r={random.random()}&pt_uistyle=40")
        ptdrvs = dict(r.cookies)['ptdrvs']
        return ptdrvs

    # 生成bkn(ldw)
    def _make_ldw_bkn(self):
        n = 5381
        for s in self.skey:
            n += (n << 5) + ord(s)
        bkn = (n & 2147483647)
        return bkn

    # 生成g_tk
    def _make_g_tk(self):
        n = 5381
        for s in self.p_skey:
            n += (n << 5) + ord(s)
        g_tk = (n & 0x7fffffff)
        return g_tk

    # 生成qzonetoken
    def _make_qzonetoken(self):
        r = requests.get(f"https://user.qzone.qq.com/{self.qq}/infocenter", headers=self.headers,
                         cookies=self.login_cookie)
        try:
            qzonetoken = re.findall('window.g_qzonetoken = \(function\(\){ try{return "(.*?)";', r.text)[0]
        except IndexError:
            raise Exception("cookie已失效！")
        return qzonetoken

    # 获取login_sig
    def _make_login_sig(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Cookie": "_qz_referrer=user.qzone.qq.com"
        }
        r = requests.get(
            "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html&pt_no_auth=1",
            headers=headers, verify=False)
        self.pt_guid_sig = dict(r.cookies)['pt_guid_sig']
        self.pt_local_token = dict(r.cookies)['pt_local_token']
        self.pt_login_sig = dict(r.cookies)['pt_login_sig']
        self.pt_serverip = dict(r.cookies)['pt_serverip']
        self.uikey = dict(r.cookies)['uikey']

        return self.pt_login_sig

    # 检测是否扫码登录，成功则返回记录登录信息cookie
    def scan_login(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Referer": "https://xui.ptlogin2.qq.com/cgi-bin/xlogin?proxy_url=https%3A//qzs.qq.com/qzone/v6/portal/proxy.html&daid=5&&hide_title_bar=1&low_login=0&qlogin_auto_login=1&no_verifyimg=1&link_target=blank&appid=549000912&style=22&target=self&s_url=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&pt_qr_app=%E6%89%8B%E6%9C%BAQQ%E7%A9%BA%E9%97%B4&pt_qr_link=http%3A//z.qzone.com/download.html&self_regurl=https%3A//qzs.qq.com/qzone/v6/reg/index.html&pt_qr_help_link=http%3A//z.qzone.com/download.html&pt_no_auth=1"
        }
        self._make_cookie_param()
        self.qrsig = self._make_qrsig()
        ptqrtoken = self._make_ptqrtoken(self.qrsig)
        ptdrvs = self._make_ptdrvs(self.pt_login_sig)
        while True:
            cookies = {
                # # 非必须参数
                # "pgv_pvi":"4591200256",
                # # 非必须参数
                # "pgv_si":"s6751861760",
                # 必须参数，缺少则无法正常检测是否已扫码
                "pt_login_sig": self.pt_login_sig,
                # 必须参数，缺少则手机端扫码将出现请求超时
                "pt_clientip": self.pt_clientip,
                # 必须参数，缺少则手机端扫码将出现请求超时
                "pt_serverip": self.pt_serverip,
                # # 非必须参数
                # "pt_local_token":self.pt_local_token,
                # # 非必须参数
                # "uikey":self.uikey,
                # 必须参数，缺少则无法正常检测是否已扫码
                "pt_guid_sig": self.pt_guid_sig,
                # # 非必须参数
                # "_qpsvr_localtk":"0.22297357405196694",
                # # 非必须参数
                # "pgv_pvid":"6277748174",
                # # 非必须参数
                # "pgv_info":"ssid=s9005615745",
                # # 非必须参数
                # "_qz_referrer":"user.qzone.qq.com",
                # 必须参数，缺少则接口无响应
                "qrsig": self.qrsig
            }
            # 扫码接口检测间隔时间
            time.sleep(1)
            check_api = f"https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.html%3Fpara%3Dizone&ptqrtoken={ptqrtoken}&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0-{random.random()}&js_ver=20021917&js_type=1&login_sig=UOEcV0kZH1ulM8Dz1bRwWlZbiYKxvD5-hKGtEPFUl365I*Rwla-odqub*2Q0AJa*&pt_uistyle=40&aid=549000912&daid=5&ptdrvs={ptdrvs}&"
            r = requests.get(check_api, headers=headers, cookies=cookies, allow_redirects=False, verify=False)
            data = r.text
            # 判断二维码状态
            if "二维码已失效" in data:
                self.qrsig = self._make_qrsig()
                ptqrtoken = self._make_ptqrtoken(self.qrsig)
                ptdrvs = self._make_ptdrvs(self.pt_login_sig)
                continue
            elif "二维码未失效" in data:
                print("二维码已生成等待扫码中...")
                continue
            elif "二维码认证中" in data:
                print("二维码认证中...")
            elif "登录成功" in data:
                # 获取扫码成功后的cookie
                confirm_ok_cookie = r.cookies
                # 获取QQ空间跳转链接
                dump_url = re.findall("ptuiCB\('0','0','(.*?)','0','登录成功！', '.*?'\)", data, re.S)[0]
                # 加载扫码成功后的cookie，必须禁止重定向，不然无法获取QQ空间登录凭证的cookie
                r = requests.get(dump_url, cookies=confirm_ok_cookie, allow_redirects=False)
                # QQ空间登录凭证转换为字典
                self.login_cookie = dict(r.cookies)
                print("客户端已确认登录！")
                break

class QQZone(Base):
    def __init__(self, cookie=None):
        super().__init__(cookie)

    # 获取QQ空间的此QQ的头像
    def profile_pic(self, pic_size: int = 100) -> str:
        """获取QQ空间的此QQ的头像

        :param pic_size: 图片的尺寸(50,100)
        :return: QQ空间头像的链接
        """
        return "https://qlogo3.store.qq.com/qzone/{}/{}/{}".format(self.qq, self.qq, pic_size)

    # QQ空间获取头像
    def profile_pic_search(self, qq: int, pic_size: int = 100) -> str:
        """QQ空间获取头像

        :param qq: QQ号
        :param pic_size: 图片的尺寸(50,100)
        :return: QQ空间头像的链接
        """
        return "https://qlogo3.store.qq.com/qzone/{}/{}/{}".format(qq, qq, pic_size)

    # 获取QQ空间信息
    def info(self) -> dict:
        """获取QQ空间信息

        :return: QQ空间相关信息
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
        }
        r = requests.get("https://user.qzone.qq.com/{}/".format(self.qq), headers=headers, cookies=self.login_cookie)
        name = re.findall('<title>(.*?) \[', r.text)[0]
        level = re.findall('title="当前空间等级：(.*?)级；积分：.*?分"', r.text)[0]
        cent = re.findall('title="当前空间等级：.*?级；积分：(.*?)分"', r.text)[0]
        sign = re.findall('<span class="description-text" id="QZ_Space_Desc">(.*?)</span>', r.text)[0]
        growth = re.findall('<span class="txt-value">成长值<b class="count">(.*?)</b></span>', r.text)[0]
        growth_speed = re.findall('<span class="txt-speed">成长速度<b class="count">(.*?)点/天</b></span>', r.text)[0]
        back_ground_top = "http:" + re.findall('background-image:url\((.*?)\);', r.text)[0]
        back_ground_buttom = "http:" + re.findall('background-image:url\((.*?)\);', r.text)[1]
        data = {
            "name": name,
            "sign": sign,
            "level": level,
            "cent": cent,
            "growth": growth,
            "growth_speed": growth_speed,
            "background_top": back_ground_top,
            "background_buttom": back_ground_buttom,
        }
        """
        {
        'name': 'M.'           # QQ空间昵称
        'sign': 'QQ空间已认证', # QQ空间签名
        'level': '47',         # QQ空间等级
        'cent': '16047',       # QQ空间积分
        'growth': '1',         # QQ空间成长值
        'growth_speed': '-10', # QQ空间成长速度
        'background_top': 'http://i.gtimg.cn/qzone/space_item/orig/3/72019_top.jpg',
        'background_buttom': 'http://i.gtimg.cn/qzone/space_item/orig/3/72019_bg.jpg'
        }
        """
        return data

    # QQ空间访客数量信息
    def visitor_num(self) -> dict:
        """QQ空间访客数量信息

        :return: QQ空间访客信息
        """
        r = requests.get(
            f"https://user.qzone.qq.com/proxy/domain/g.qzone.qq.com/cgi-bin/friendshow/cgi_get_visitor_simple?uin={self.qq}&mask=1&g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
            cookies=self.login_cookie)
        data = re.findall("_Callback\((.*?)\);", r.text, re.S)[0]
        d = json.loads(data)
        visit_data = {
            # 黄钻用户 0：普通用户 1：黄钻
            "vip": d['data']['qzone_vip'],
            # 今日访问量
            "today_view": d['data']['modvisitcount'][0]['todaycount'],
            # 总访问量
            "total_view": d['data']['modvisitcount'][0]['totalcount'],
            # 今日被挡访客数
            "today_ban_view": d['data']['modvisitcount'][2]['todaycount'],
            # 总被挡访客数
            "total_ban_view": d['data']['modvisitcount'][3]['totalcount'],
            # 今日空间访问量
            "todaty_qqzone_view": d['data']['calvisitcount'][0],
            # 空间总访客数
            "totla_visitor": d['data']['modvisitcount'][1]['totalcount'],
            # 近期访问量
            "recent_view": d['data']['calvisitcount']
        }

        return visit_data

    # QQ空间我在意谁
    def care_friend(self) -> dict:
        """QQ空间我在意谁

        :return: 相关好友信息
        """
        r = requests.get(
            f"https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin={self.qq}&do=1&rd=0.19273544996596104&fupdate=1&clean=1&g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
            cookies=self.login_cookie)
        data = re.findall("_Callback\((.*?)\);", r.text, re.S)[0]
        d = json.loads(data)['data']['items_list']
        return d

    # QQ空间谁在意我
    def care_me(self) -> dict:
        """QQ空间谁在意我

        :return: 相关好友信息
        """
        r = requests.get(
            f"https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin={self.qq}&do=2&rd=0.19273544996596104&fupdate=1&clean=1&g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
            cookies=self.login_cookie)
        data = re.findall("_Callback\((.*?)\);", r.text, re.S)[0]
        d = json.loads(data)['data']
        return d

    # QQ空间最近添加的好友
    def recent_add(self) -> dict:
        """QQ空间最近添加的好友

        :return: 最近添加的好友
        """
        r = requests.get(
            f"https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/getfriendmsglist.cgi?uin={self.qq}&fupdate=1&rd=1584108276&version=8&g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
            cookies=self.login_cookie)
        print(r.text)
        data = re.findall("_Callback\((.*?)\);", r.text, re.S)[0]
        d = json.loads(data)['data']
        return d

    # QQ空间发表说说
    def publish_talk(self, talk_content: str, img_urls: list = None, update_sign: bool = False,
                     visual_range: int = None, friends: list = None) -> tuple:
        """QQ空间发表说说

        :param talk_content: 说说的内容
        :param img_urls: 要上传的图片链接或本地地址
        :param update_sign: 是否同步到个性签名，True为同步，False为不同步
        :param visual_range: 说说查看权限设置
        :param friends: 设置了部分好友可见或部分好友不可见时的好友QQ号
        :return: True为说说发表成功，False则发表失败
        """
        allow_uins = str()
        # 是否同步到签名
        if update_sign == True:
            sign = "qm"
        else:
            sign = ""
        # 所有人可见
        if visual_range == None:
            v_range = 1
        # 仅QQ好友可见
        elif visual_range == "friend":
            v_range = 4
        # 仅自己可见
        elif visual_range == "me":
            v_range = 64
        # 部分好友不可见
        elif visual_range == "exclude":
            v_range = 128
            for f in friends:
                allow_uins = str(f) + "|"
        # 部分好友可见
        elif visual_range == "part":
            v_range = 16
            for f in friends:
                allow_uins = str(f) + "|"
        # 有不符合的参数时默认为所有人可见
        else:
            v_range = 1
        # 发送文字说说
        if img_urls is None:
            # 表单数据
            form_data = {
                "syn_tweet_verson": " 1",
                "paramstr": " 1",
                "pic_template": "",
                "richtype": "",
                "richval": "",
                "special_url": "",
                "subrichtype": "",
                "con": sign + talk_content,
                "feedversion": "1",
                "ver": "1",
                "ugc_right": v_range,
                "allow_uins": allow_uins,
                "to_sign": "0",
                "hostuin": self.qq,
                "code_version": "1",
                "format": "fs",
                "qzreferrer": "https:// user.qzone.qq.com/{}/infocenter".format(self.qq)
            }
            # 请求接口
            r = requests.post(
                f"https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_publish_v6?qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
                headers=self.headers, data=form_data, cookies=self.login_cookie)
            if r.ok:
                result = re.findall("frameElement.callback\((.*?)\);", r.text)[0]
                result = json.loads(result)
                feedskey = result['t1_tid']
                feedstime = result['t1_ntime']
                return feedskey, feedstime
            else:
                return 0, 0
        # 发送带图说说
        else:
            # 上传图片
            pic_num = len(img_urls)
            pic_bo = str()
            richval = str()
            if pic_num > 1:
                bo_symbol = ','
                richval_symbol = '	'
            else:
                bo_symbol = ''
                richval_symbol = ''
            for img_url in img_urls:
                # 图片base64编码
                img_base64 = base64.b64encode(requests.get(img_url).content).decode()
                # 表单数据
                data = {
                    "filename": "filename",
                    "uin": self.qq,
                    "skey": self.skey,
                    "zzpaneluin": self.qq,
                    "zzpanelkey": "",
                    "p_uin": self.qq,
                    "p_skey": self.p_skey,
                    "qzonetoken": self._make_qzonetoken(),
                    "uploadtype": "1",
                    "albumtype": "7",
                    "exttype": "0",
                    "refer": "shuoshuo",
                    "output_type": "jsonhtml",
                    "charset": "utf-8",
                    "output_charset": "utf-8",
                    "upload_hd": "1",
                    "hd_width": "2048",
                    "hd_height": "10000",
                    "hd_quality": "96",
                    "backUrls": "http://upbak.photo.qzone.qq.com/cgi-bin/upload/cgi_upload_image,http://119.147.64.75/cgi-bin/upload/cgi_upload_image",
                    "url": "https://up.qzone.qq.com/cgi-bin/upload/cgi_upload_image?g_tk={}".format(self._make_g_tk()),
                    "base64": "1",
                    "jsonhtml_callback": "callback",
                    "picfile": img_base64,
                }
                up_url = f'https://up.qzone.qq.com/cgi-bin/upload/cgi_upload_image?g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}'
                up_result = requests.post(up_url, data=data)
                bo = re.findall('bo=(.*?)"', up_result.text)[0]
                up_result = re.findall("frameElement.callback\((.*?)\)", up_result.text)[0]
                up_result = json.loads(up_result)
                lloc = up_result['data']['lloc']
                sloc = up_result['data']['sloc']
                img_type = up_result['data']['type']
                img_width = up_result['data']['width']
                img_height = up_result['data']['height']
                albumid = up_result['data']['albumid']
                richval += ',%s,%s,%s,%s,%s,%s,,%s,%s' % (
                    albumid, lloc, sloc, img_type, img_height, img_width, img_height, img_width) + richval_symbol
                pic_bo += bo + bo_symbol
            # 去掉最后的“,”
            pic_bo = pic_bo[:-1]
            # 去掉最后的“    ”
            richval = richval.strip()
            # 发表
            data = {
                "syn_tweet_verson": "1",
                "paramstr": "1",
                "pic_template": "tpl-{}-1".format(pic_num),
                "richtype": "1",
                "richval": richval,
                "special_url": "",
                "subrichtype": "1",
                "pic_bo": pic_bo + "    " + pic_bo,
                "who": "1",
                "con": sign + talk_content,
                "feedversion": "1",
                "ver": "1",
                "ugc_right": v_range,
                "to_sign": sign,
                "hostuin": "{}".format(self.qq),
                "code_version": "1",
                "format": "fs",
                "qzreferrer": "https://user.qzone.qq.com/{}/infocenter".format(self.qq)
            }
            r = requests.post(
                f"https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_publish_v6?qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
                data=data, cookies=self.login_cookie)
            if r.ok:
                result = re.findall("frameElement.callback\((.*?)\); </script></body></html>", r.text)[0]
                result = json.loads(result)
                feedskey = result['tid']
                feedstime = result['now']
                return feedskey, feedstime
            else:
                return 0, 0

    # QQ空间删除说说
    def delete_talk(self, feeds: str) -> bool:
        """QQ空间删除说说

        :param feeds: 说说的ID号
        :return: 返回True为删除成功，False则为删除失败
        """
        feedskey = feeds[0]
        feedstime = feeds[-1]
        data = {
            "uin": "{}".format(self.qq),
            "topicId": "{}_{}__1".format(self.qq, feedskey),
            "feedsType": "0",
            "feedsFlag": "0",
            "feedsKey": "{}".format(feedskey),
            "feedsAppid": "311",
            "feedsTime": "{}".format(feedstime),
            "fupdate": "1",
            "ref": "feeds",
            "qzreferrer": "https://user.qzone.qq.com/{}/infocenter".format(self.qq),
        }
        r = requests.post(
            f"https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_delete_v6?qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
            data=data, cookies=self.login_cookie)
        if r.status_code == 200:
            return True
        else:
            return False

    # QQ空间更新QQ个性签名
    def update_sign(self, sign_content: str) -> bool:
        """QQ空间更新QQ个性签名

        :param sign_content: 个性签名的内容
        :return: True为QQ个性签名更新成功，False为QQ个性签名更新失败
        """
        return self.delete_talk(self.publish_talk(sign_content, update_sign=True)[0])

    # QQ空间群列表
    def get_group_list(self) -> list:
        """QQ空间群列表

        :return: 群相关信息
        """
        group_info = []
        try:
            r = requests.get(
                f"https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/qqgroupfriend_extend.cgi?uin={self.qq}&rd=0.1384018394129476&cntperpage=0&fupdate=1&g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
                cookies=self.login_cookie)
            data = re.findall("_Callback\((.*?)\);", r.text, re.S)[0]
            groups = json.loads(data)['data']['group']
            for g in groups:
                group_info.append(
                    {'group_id': g['groupcode'], 'group_name': g['groupname'], 'total_member': g['total_member']})
            return group_info
        except IndexError:
            print("QQ空间群列表接口请求失败！请重新请求。")

    # QQ空间获取好友列表
    def get_friend_list(self) -> tuple:
        """QQ空间获取好友列表

        :return: 好友相关信息
        """
        r = requests.get(
            f"https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_show_qqfriends.cgi?uin={self.qq}&follow_flag=1&groupface_flag=0&fupdate=1&g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
            cookies=self.login_cookie)
        result = re.findall("_Callback\((.*?)\);", r.text, re.S)[0]
        result = json.loads(result)
        group_list = result['data']['gpnames']
        friend_list = result['data']['items']
        return group_list, friend_list

    # QQ空间我的说说
    def talk(self) -> tuple:
        """

        :return: 我的说说信息
        """
        r = requests.get(
            f"https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={self.qq}&ftype=0&sort=0&pos=0&num=20&replynum=100&g_tk={self._make_g_tk()}&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
            cookies=self.login_cookie)
        result = re.findall("_preloadCallback\((.*?)\);", r.text)[0]
        fid = re.findall('"tid":"(.*?)"', result)
        ftime = re.findall('"created_time":(.*?),', result)
        content = list(filter(lambda x: x != " ", re.findall('"con":"(.*?)"', result)))
        return dict(zip(fid, ftime)), content

    # QQ空间说说动态
    def talk_dynamic(self) -> dict:
        """

        :return: 说说的ID号和所属QQ号
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400",
            "Referer": "https://user.qzone.qq.com/{}/infocenter".format(self.qq)
        }
        r = requests.get(
            f"https://user.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds3_html_more?uin={self.qq}&scope=0&view=1&daylist=&uinlist=&gid=&flag=1&filter=all&applist=all&refresh=0&aisortEndTime=0&aisortOffset=0&getAisort=0&aisortBeginTime={time.time()}&pagenum=1&externparam=undefined&firstGetGroup=0&icServerTime=0&mixnocache=0&scene=0&begintime=undefined&count=20&dayspac=undefined&sidomain=qzonestyle.gtimg.cn&useutf8=1&outputhtmlfeed=1&rd=0.995029480889664&usertime={time.time()}&windowId=0.11643100420349328&g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
            headers=headers, cookies=self.login_cookie)
        # 网络繁忙则再次请求接口
        while "network busy" in r.text:
            r = requests.get(
                f"https://user.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds3_html_more?uin={self.qq}&scope=0&view=1&daylist=&uinlist=&gid=&flag=1&filter=all&applist=all&refresh=0&aisortEndTime=0&aisortOffset=0&getAisort=0&aisortBeginTime={time.time()}&pagenum=1&externparam=undefined&firstGetGroup=0&icServerTime=0&mixnocache=0&scene=0&begintime=undefined&count=20&dayspac=undefined&sidomain=qzonestyle.gtimg.cn&useutf8=1&outputhtmlfeed=1&rd=0.995029480889664&usertime={time.time()}&windowId=0.11643100420349328&g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
                headers=headers, cookies=self.login_cookie)
        r.encoding = "utf-8"
        data = r.text.replace(r"\x22", '"').replace(r"\x3C", "<").replace(r"\/", "/").replace("/\\", '/').replace(
            "<br>", "").replace("<br/>", "")
        print(data)
        qq = re.findall('data-curkey="http://user.qzone.qq.com/(.*?)/mood/.*?"', data)
        fid = re.findall('data-curkey="http://user.qzone.qq.com/.*?/mood/(.*?)"', data)
        return dict(zip(fid, qq))

    # QQ空间获取说说动态详细信息
    def get_talk_detail(self) -> list:
        """

        :return: 说说动态详细信息
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400",
            "Referer": "https://user.qzone.qq.com/{}/infocenter".format(self.qq)
        }
        r = requests.get(
            f"https://user.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds3_html_more?uin={self.qq}&scope=0&view=1&daylist=&uinlist=&gid=&flag=1&filter=all&applist=all&refresh=0&aisortEndTime=0&aisortOffset=0&getAisort=0&aisortBeginTime={time.time()}&pagenum=1&externparam=undefined&firstGetGroup=0&icServerTime=0&mixnocache=0&scene=0&begintime=undefined&count=20&dayspac=undefined&sidomain=qzonestyle.gtimg.cn&useutf8=1&outputhtmlfeed=1&rd=0.995029480889664&usertime={time.time()}&windowId=0.11643100420349328&g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
            headers=headers, cookies=self.login_cookie)
        # 网络繁忙则再次请求接口
        while "network busy" in r.text:
            r = requests.get(
                f"https://user.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds3_html_more?uin={self.qq}&scope=0&view=1&daylist=&uinlist=&gid=&flag=1&filter=all&applist=all&refresh=0&aisortEndTime=0&aisortOffset=0&getAisort=0&aisortBeginTime={time.time()}&pagenum=1&externparam=undefined&firstGetGroup=0&icServerTime=0&mixnocache=0&scene=0&begintime=undefined&count=20&dayspac=undefined&sidomain=qzonestyle.gtimg.cn&useutf8=1&outputhtmlfeed=1&rd=0.995029480889664&usertime={time.time()}&windowId=0.11643100420349328&g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
                headers=headers, cookies=self.login_cookie)
        r.encoding = "utf-8"
        data = r.text.replace(r"\x22", '"').replace(r"\x3C", "<").replace(r"\/", "/").replace("/\\", '/').replace(
            "<br>", "").replace("<br/>", "")
        print(data)
        app_ids = re.findall("appid:'(.*?)'", data)
        nick_names = re.findall("nickname:'(.*?)'", data)
        qqs = re.findall("opuin:'(.*?)'", data)
        profile_imgs = re.findall("logimg:'(.*?)'", data)
        abstimes = re.findall("abstime:'(.*?)'", data)
        feedstimes = re.findall("feedstime:' (.*?)'", data)
        keys = re.findall(",key:'(.*?)'", data)
        user_hosts = re.findall("userHome:'(.*?)'", data)
        view_sums = re.findall("浏览(.*?)次", data)
        like_sums = re.findall('class="f-like-cnt">(.*?)</span>人觉得很赞</div>', data)
        feed_infos = re.findall('<div class="f-info">(.*?)</div>', data)
        view_sums.append('null')
        like_sums.append('null')
        talk_data = list()
        for app_id, nick_name, qq, profile_img, abstime, feedstime, key, user_host, view_sum, like_sum, feed_info in zip(
                app_ids, nick_names, qqs, profile_imgs, abstimes, feedstimes, keys, user_hosts, view_sums, like_sums,
                feed_infos):
            talk_data.append(
                {
                    'app_id': app_id,
                    'nick_name': nick_name,
                    'qq': qq,
                    'profile_img': profile_img,
                    'abstime': abstime,
                    'feedstime': feedstime,
                    'key': key,
                    'user_host': user_host,
                    'view_sum': view_sum,
                    'like': like_sum,
                    'feed_info': feed_info
                }
            )

        return talk_data

    # QQ空间说说点赞
    def talk_like(self, fid: str, qq: str) -> bool:
        """QQ空间说说点赞

        :param fid: 说说ID号
        :param qq: QQ号
        :return: True为点赞成功，False则为点赞失败
        """
        data = {
            "qzreferrer": "https://user.qzone.qq.com/{}".format(qq),
            "opuin": "{}".format(qq),
            "unikey": "http://user.qzone.qq.com/{}/mood/{}".format(qq, fid),
            "curkey": "http://user.qzone.qq.com/{}/mood/{}".format(qq, fid),
            "from": "1",
            "appid": "311",
            "typeid": "0",
            "abstime": time.time(),
            "fid": "{}".format(fid),
            "active": "0",
            "fupdate": "1"
        }
        r = requests.post(
            f"https://user.qzone.qq.com/proxy/domain/w.qzone.qq.com/cgi-bin/likes/internal_dolike_app?g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}",
            data=data, cookies=self.login_cookie)
        if r.ok:
            return True
        else:
            return False

    # 说说自动点赞
    def auto_talk_like(self):
        for fid, qq in self.talk_dynamic().items():
            print(self.talk_like(fid, qq))

    # QQ空间说说评论
    def talk_comment(self, fid: str, qq: str, comment: str) -> bool:
        """QQ空间说说评论

        :param fid: 说说ID号
        :param qq: QQ号
        :param comment: 评论的内容
        :return: True为评论成功，False则为评论失败
        """
        talk_comment_api = 'https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_re_feeds'
        params = {
            'qzonetoken': self._make_qzonetoken(),
            'g_tk': self._make_g_tk()
        }

        data = {
            "topicId": "{}_{}__1".format(qq, fid),
            "feedsType": "100",
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "plat": "qzone",
            "source": "ic",
            "hostUin": "{}".format(qq),
            "isSignIn": "",
            "platformid": "50",
            "uin": "{}".format(qq),
            "format": "fs",
            "ref": " feeds",
            "content": comment,
            "richval": "",
            "richtype": "",
            "private": "0",
            "paramstr": "1",
            "qzreferrer": "https://user.qzone.qq.com/{}".format(qq),
        }
        r = requests.post(talk_comment_api, params=params, data=data, cookies=self.login_cookie)
        if comment in r.text:
            return True
        else:
            return False

    # QQ空间寻找好友
    def find_friend(self) -> list:
        """QQ空间寻找好友

        :return: 好友相关信息
        """
        find_friend_api = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/potential/potentialpy_lookingforfriend.cgi'
        r = requests.get(
            find_friend_api + f"?uin={self.qq}&page=1&num=100&rd=0.5585130912437413&fupdate=1&g_tk={self._make_g_tk()}&qzonetoken={self._make_qzonetoken()}&g_tk={self._make_g_tk()}",
            cookies=self.login_cookie)
        data = re.findall('_Callback\((.*?)\);', r.text, re.S)[0]
        d = json.loads(data)
        friends = d['data']['potentialfriends']
        fs = list()
        print(data)
        for friend in friends:
            f = dict()
            f['qq'] = friend['uin']
            f['nick'] = friend['nick']
            f['gender'] = friend['gender']
            f['friends'] = friend['commonfriends']
            fs.append(f)
        return fs
