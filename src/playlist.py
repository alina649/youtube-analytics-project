import json
import os
from datetime import timedelta


import isodate
from googleapiclient.discovery import build


class PlayList:

    def __init__(self,  playlist_id):

        self.playlist_id = playlist_id

        request = PlayList.get_service().playlists().list(part="snippet",id=self.playlist_id).execute()

        self.title = request['items'][0]['snippet']['title']
        self.url: str = 'https://www.youtube.com/playlist?list=' + self.playlist_id


    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(PlayList.get_service().playlists().list(part="snippet",id=self.playlist_id).execute(),
                               indent=2, ensure_ascii=False))


    def video_response(self):
        """вывод информации о видеороликов из плейлиста"""
        playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                      part='contentDetails',
                                                                      maxResults=50,
                                                                      ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(video_ids)
                                                              ).execute()
        return video_response['items']

    @property
    def total_duration(self):
        """суммарная длительность плейлиста"""
        time_line = []
        for video in PlayList.video_response(self):

            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            time_line.append(duration)
        summa_time = sum(time_line, timedelta())
        return summa_time

    def show_best_video(self):
        """Вывод сылки видео с самым большим количеством лайков"""
        line = {}
        for video in PlayList.video_response(self):
            line['https://youtu.be/'+f"{video['id']}"] = video['statistics']['likeCount']
            max_like = max(line, key=line.get)
        return  max_like








