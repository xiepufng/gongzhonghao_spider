import requests
import json
import time
from fake_useragent import UserAgent
from lxml import etree


class GzhSpider(object):
    """公众号爬取，以<<ne0>>为例"""

    def __init__(self):
        # 从浏览器中抓取headers
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'ua_id=l9T2xgC4YbzJ7gn8AAAAAG_-z8Ik-ysfhHp7hZsTPpY=; pgv_pvi=3947182080; openid2ticket_oFpSttzKea_wI1hHFK2aCm5HNdoo=6NB9E9pCmo7sQ3mEX/bHNx9wnt0Pj03kCGiUhH07lis=; RK=d2SJgyODGN; ptcz=005816e2d395ab789de628076a038e8e0d71d382d5a82773df8e59ec71a333a4; pgv_pvid=2427007484; openid2ticket_oHwQis4KS5pm_ak4aiL-aQbXUUcc=; tvfe_boss_uuid=262b99cbf2e12563; ts_uid=6709292236; wxuin=08810458096598; mm_lang=zh_CN; _ga=GA1.2.1438886888.1612098592; pac_uid=0_31c483af721e3; ptui_loginuin=1173181700; pgv_info=ssid=s167973680; rewardsn=; wxtokenkey=777; mmad_session=78dbdd5914e2c55a0949b985e4928d7d0dfa908f2f7f016a03c1607d4f8219954964c1b234b363008a7272fe2dbb6a05c28040da667eb016d225966bbd4771a752de0e9fba23db7cf253633c2adf32afd6d46f43ae3236ef1ebbeed2bb01cca211de1c56c245721266e7088080fefde3; uuid=169aba095b7fad7a700d40f6d5def2b3; rand_info=CAESIFuK7I7jlhNOTS2Xqdkohgk6eHLlePX0fL3GDjn+6Nj2; slave_bizuin=3005350943; data_bizuin=3005350943; bizuin=3005350943; data_ticket=L563uDAsTrAG6DG5MCkrY0mtJgCendOGVoDVk1TGEF49JScba3L560ugzSsgtctZ; slave_sid=VGFUYV9sRkxGMTltYzUwd1FjdzliUV9yX0pmbXVRVzdhRTQxd1p1Uk9nR25ZVGY5Tm1lUUlVbkJtd2xJbVVIaXRDZDE4ZzIzZ25MS1JkMGFoYVVNY0taeVk3RzRoTlN4OGwyTUdwVGdQc0lqY1ZpZmlmUm0zczZEaERkdjhLd1JOaWs3aFJVM3lrdGhpUG1w; slave_user=gh_94ecceee7d5a; xid=7a8aa871b071b618ad04941ad6376017',
            'referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&createType=0&token=104373110&lang=zh_CN',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
        }
        self.url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin={}&count=5&fakeid=MzI0NjE3MTI1Mw==&type=9&query=&token=104373110&lang=zh_CN&f=json&ajax=1'
        self.ua = UserAgent()

    # 提取文章链接
    def get_one_html(self):
        for begin in range(0, 100, 5):
            url = self.url.format(begin)
            html = requests.get(url=url, headers=self.headers).text
            html = json.loads(html)
            print(html)
            data = html['app_msg_list']
            print(data)
            for i in data:
                link = i['link']
                title = i['title']
                # print(title,link)
                self.get_two_html(link, title)
            # 控制休眠时间，防止被封
            time.sleep(3)

    # 获取文章内容
    def get_two_html(self, link, title):
        html = requests.get(url=link, headers={'User-Agent': self.ua.random}).text
        self.parse_html(html, title)

    # 解析内容
    def parse_html(self, html, title):
        pattern = etree.HTML(html)
        content = pattern.xpath('//div[@id="js_content"]//p/span/text()')
        content=''.join(content)
        self.write_data(content, title)

    # 保存文件
    def write_data(self, content, title):
        with open('/home/tarena/article' + title + 'txt', 'w')as f:
            f.write(content)

    def main(self):
        self.get_one_html()


if __name__ == '__main__':
    spider = GzhSpider()
    spider.main()
