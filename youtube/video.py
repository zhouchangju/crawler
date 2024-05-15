'''
获取Youtube的视频信息

执行命令：python -m  youtube.video
参考文章：https://blog.csdn.net/zzz_zjz/article/details/105006921
'''

import json


from utils.config_parser import ConfigParser
from utils.proxy import ProxyHandler

parser = ConfigParser()
config_data = parser.read_config()

# 获取API密钥
API_KEY = parser.get_option('google_developer', 'api_key')

# 设置代理信息
proxy_handler = ProxyHandler()
urllib = proxy_handler.set_http_proxy('https')


def get_video_info(video_id):
    """查询指定视频的信息"""
    base_url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet,contentDetails,statistics',
        'id': video_id,
        'key': API_KEY
    }
    query_string = urllib.parse.urlencode(params)
    url = f'{base_url}?{query_string}'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read()
        return data.decode('utf-8')

# 测试
# video_id = 'Alpyf1nq6HM'
# print(get_video_info(video_id))


def get_playlist_items(playlist_id):
    """查询指定播放列表下的视频"""
    base_url = 'https://www.googleapis.com/youtube/v3/playlistItems'
    params = {
        'part': 'id,snippet',
        'playlistId': playlist_id,
        # 0-50
        'maxResults': 50,
        # 根据上一次请求的nextPageToken 和 prevPageToken 获取下一页或上一页的数据
        # 'pageToken': 'EAAajQFQVDpDR1FpRURjNE1EWXdOVUpETmpsRE5rTXlOVEFvQVVqRTZJcTlqNlNGQTFBQldrUWlRMmxLVVZSSGNFbFJNVkpRVm5wV2RtRnVTbXhaTUZKSFkydzVUbVI2V1RKWGEzQkZaVlZuZVU5VWJGUlZia1pMUldkelNYSndTM2h6UVZsUmIweDFXRVZSSWc',
        'key': API_KEY
    }
    query_string = urllib.parse.urlencode(params)
    url = f'{base_url}?{query_string}'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read()
        return data.decode('utf-8')


# VIS Full Papers - Presentations | VIS 2023
full_paper_playlist_id = 'PLjHCTOW5ojrecDFr_Mw66ZJDyH299SRqJ'

# VIS Short Papers - Presentations | VIS 2023
short_paper_playlist_id = 'PLjHCTOW5ojre6rWEl5svbw12sENBkXMrA'

# playlist_response_str = get_playlist_items(short_paper_playlist_id)
# playlist_response = json.loads(playlist_response_str)
# print(playlist_response)


def get_caption_info(video_id):
    """查询指定视频的字幕信息"""
    base_url = 'https://www.googleapis.com/youtube/v3/captions'
    params = {
        'part': 'snippet',
        'videoId': video_id,
        'key': API_KEY
    }
    query_string = urllib.parse.urlencode(params)
    url = f'{base_url}?{query_string}'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read()
        return data.decode('utf-8')


# 下载视频的字幕，并写入本地文件


'''
不能用，因为不让下载了：https://stackoverflow.com/questions/30653865/downloading-captions-always-returns-a-403
'''


def download_caption(caption_id, caption_file_path):
    """
    下载视频的字幕，并写入本地文件
    https://www.googleapis.com/youtube/v3/captions/id
    这个需要google的oauth2.0认证：https://doc.yonyoucloud.com/doc/wiki/project/google-oauth-2/overview.html

    @discard 不能用，因为不让下载了：https://stackoverflow.com/questions/30653865/downloading-captions-always-returns-a-403
    """
    base_url = 'https://www.googleapis.com/youtube/v3/captions'
    params = {
        'id': caption_id,
        'key': API_KEY
    }
    query_string = urllib.parse.urlencode(params)
    url = f'{base_url}/{caption_id}?{query_string}'
    print(url)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read()
        with open(f'{caption_file_path}', 'wb') as f:
            f.write(data)
        return data.decode('utf-8')


# caption_id = 'AUieDaYRJ2P1LGmAVxqrVvjQh1qSDE0fHyidpBwHNJ_6GvNRrDc'
# caption_file_path = f'{caption_id}.xml'
# download_caption( caption_id, caption_file_path)
