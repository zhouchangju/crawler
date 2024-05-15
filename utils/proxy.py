"""设置代理"""
import os
import urllib.parse
import urllib.request


class ProxyHandler:
    """设置网络代理的类"""
    PROXY_IP = '127.0.0.1'
    PROXY_PORT = 10809

    def set_system_proxy(self):
        """
        设置系统代理
        有的第三方包无法修改代理的协议类型(比如httplib2，不支持指定https类型)，就可以使用这个方法
        """
        proxy_address = f'http://{self.PROXY_IP}:{self.PROXY_PORT}'

        os.environ['http_proxy'] = proxy_address
        os.environ['https_proxy'] = proxy_address

    def set_http_proxy(self, http_type='http'):
        """
        设置HTTP代理
        注意，http_type可以是http或https，需要和实际请求的网址的协议一致
        TODO:是不是可以同时设置http和https代理？

        该方法返回的是urllib对象，后续可以这样使用：
            query_string = urllib.parse.urlencode(params)
            url = f'{base_url}?{query_string}'
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read()
                return data.decode('utf-8')
        """
        proxy = urllib.request.ProxyHandler(
            {http_type: f'http://{self.PROXY_IP}:{self.PROXY_PORT}'})
        opener = urllib.request.build_opener(proxy)
        urllib.request.install_opener(opener)
        return urllib
