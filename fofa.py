# coding:utf-8
'''
 * @Author: w4nde3
 * @Date: 2021-02-25 15:29:24
 * @LastEditors: w4nde3
 * @LastEditTime: 2021-02-25 19:46:58
'''

import requests
import base64
import json
import time
import click


class Fofa:
    def __init__(self, email, key):
        self.email = email
        self.key = key
        self.query_api = "https://fofa.so/api/v1/search/all"
        self.userinfo_api = "https://fofa.so/api/v1/info/my"
        self.data = ()
        self.uesrinfo = self.get_user_info()  # test connection
        self.req = requests

    def get_user_info(self):
        try:
            res = self.req.get(
                self.userinfo_api +
                "?email={0}&key={1}".format(self.email, self.key))
            if res.status_code == 200:
                return json.dumps(json.loads(res.text),
                                  sort_keys=True,
                                  indent=2)
            else:
                print("[x] 身份认证出错，请检查邮箱和apikey")
                exit()
        except requests.RequestException as e:
            print("[x] 请求失败，请检查网络")
            raise e

    def query(self, query):
        try:
            query_qbase64 = base64.b64encode(query.encode()).decode()
            res = self.req.get(self.query_api +
                               "?email={0}&key={1}&qbase64={2}".format(
                                   self.email, self.key, query_qbase64))
            if res.status_code == 200:
                json_data = json.loads(res.text)
                self.data = (json_data['query'],
                             [url[0] for url in json_data['results']])
            else:
                pass
        except requests.RequestException as e:
            print("[x] 请求失败，请检查网络")
            raise e

    def show(self):
        print('[+] 查询语句：{}'.format(self.data[0]))
        print('[+] 查询结果：')
        for index, data in enumerate(self.data[1]):
            print('    [{}] {}'.format(index, data))

    def save(self, filename=None):
        if filename is None:
            filename = str(
                time.strftime('%Y-%m-%d-%H-%M', time.localtime(
                    time.time()))) + ".json"
        if self.data:
            with open(filename, "w") as outfile:
                json.dump({
                    "query": self.data[0],
                    "urls": self.data[1]
                },
                          outfile,
                          sort_keys=False,
                          indent=2)
        else:
            print("[-] 尚未查询到任何数据")

    def save_simple(self, filename=None):
        if filename is None:
            filename = str(
                time.strftime('%Y-%m-%d-%H-%M', time.localtime(
                    time.time()))) + ".txt"
        if self.data:
            with open(filename, 'w') as outfile:
                for data in self.data[1]:
                    outfile.write(data + "\n")
        else:
            print("[-] 尚未查询到任何数据")

@click.command()
@click.option("-o", "--output", help="输出文件的名称", required=False)
@click.option("-e", "--email", help='Fofa e-mail', required=True)
@click.option("-k", "--key", help='Fofa apikey', required=True)
@click.option(
    "-q",
    "--query",
    help=
    "query segment,eg: 'title=\"Apache Druid\" && country=\"CN\" && port=\"8888\"'"
)
def main(email, key, query, output=None):
    """
    [+] query指令参考:\n\n

    [-] title="beijing"	        从标题中搜索“北京”\n
    [-] header="jboss"          从http头中搜索“jboss”\n
    [-] body="Hacked by"        从html正文中搜索abc\n
    [-] domain="qq.com"	        搜索根域名带有qq.com的网站\n
    [-] host=".gov.cn"	        从url中搜索”.gov.cn”\n
    [-] port="443"              查找对应“443”端口的资产\n
    [-] ip="1.1.1.1"	        从ip中搜索包含“1.1.1.1”的网站\n
    [-] ip="220.181.111.1/24"	查询IP为“220.181.111.1”的C网段资产\n
    [-] status_code="402"       查询服务器状态为“402”的资产\n
    [-] protocol="https"        查询https协议资产\n
    [-] city="Hangzhou"	        搜索指定城市的资产\n
    [-] region="Zhejiang"       搜索指定行政区的资产\n
    [-] country="CN"	        搜索指定国家(编码)的资产\n
    [-] cert="google"	        搜索证书(https或者imaps等)中带有google的资产\n
    [-] type=service	        搜索所有协议资产,支持subdomain和service两种\n
    [-] os=windows              搜索Windows资产\n
    [-] app="HIKVISION视频"     搜索海康威视设备\n
    [-] is_domain=true	        搜索域名的资产,只接受true和false\n
    [-] ip_ports="80,161"       搜索同时开放80和161端口的ip\n
    [-] port_size="6"	        查询开放端口数量等于"6"的资产\n
    [-] port_size_gt="3"        查询开放端口数量大于"3"的资产\n
    [-] port_size_lt="12"       查询开放端口数量小于"12"的资产\n
    [-] server=="MicrosoftIIS/7.5"            搜索IIS 7.5服务器\n
    [-] after="2017" && before="2017-10-01"   时间范围段搜索\n
    [-] banner=users && protocol=ftp	      搜索FTP协议中带有users文本的资产\n
    """
    print("[#]Fofa e-namil:{}\n[#]Fofa apikey:{}\n[!]query segment:{}".format(
        email, key, query))
    fofa = Fofa(email, key)
    fofa.show()
    fofa.save_simple(output)


if __name__ == "__main__":
    main()
