import json
import os
from googleapiclient.discovery import build




class Video:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id

        video_response = Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.video_title = video_response['items'][0]['snippet']['title']  # название
        self.view_count = video_response['items'][0]['statistics']['viewCount']  # количество просмотров
        self.like_count = video_response['items'][0]['statistics']['likeCount']  # лайки
        self.url = video_response['items'][0]['snippet']['thumbnails']["default"]['url']  # ссылка


    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __str__(self):
        return self.video_title

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute(),
                               indent=2, ensure_ascii=False))


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

        playlist_videos = Video.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()



    def info_playlist(self):

         print(json.dumps(Video.get_service().playlistItems().list(playlistId=self.playlist_id,
                                               part='contentDetails',
                                               maxResults=50,
                                               ).execute(),indent=2, ensure_ascii=False))

    @classmethod
    def get_service_playlist(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube











