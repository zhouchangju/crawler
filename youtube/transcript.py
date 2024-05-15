'''
根据YouTube视频ID，获取字幕
'''
# https://github.com/jdepoix/youtube-transcript-api
import time
from youtube_transcript_api import YouTubeTranscriptApi


def get_caption(video_id):
    """获取字幕"""
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    transcript = transcript_list.find_transcript(['en'])
    sentences = transcript.fetch()
    content = []
    for sentence in sentences:
        content.append(sentence['text'])

    return ' '.join(content)


if __name__ == "__main__":
    # TODO:从文件中读取视频ID
    videos = []

    for video in videos:
        # 添加异常捕获，保证报错不会中断循环
        try:
            # 将内容写入本地文件，并且文件名为视频ID；如果文件不存在则自动创建

            with open(f'youtube/data/subtitle/{video}.txt', 'w', encoding='utf-8') as f:
                f.write(get_caption(video))
            # 暂停100秒，防止频繁请求
            time.sleep(1)

        except (youtube_transcript_api.CouldNotRetrieveTranscript, youtube_transcript_api.NoTranscriptFound) as e:
            print(f'Error: {e}')
            continue
