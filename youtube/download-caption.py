# API client library
from googleapiclient.discovery import build
from utils.config_parser import ConfigParser
from utils.proxy import ProxyHandler

# API information
api_service_name = "youtube"
api_version = "v3"

parser = ConfigParser()
config_data = parser.read_config()
# 获取API密钥
DEVELOPER_KEY = parser.get_option('google_developer', 'api_key')


# 设置代理信息
proxy_handler = ProxyHandler()
urllib = proxy_handler.set_http_proxy('https')


def get_caption_details(video_id):
    """获取视频信息"""
    # API client
    # https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html
    youtube = build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    request = youtube.videos().list(part='id,snippet', id=video_id)
    response = request.execute()
    return response


def print_caption_details(details):
    """打印视频的标题和观看次数"""
    title = details['items'][0]['snippet']['title']
    view_count = details['items'][0]['statistics']['viewCount']
    print(f'Title: {title}')
    print(f'View count: {view_count}')


# video_id = 'xno7fqxVD40'
# details = get_caption_details(video_id)
# print_caption_details(details)
