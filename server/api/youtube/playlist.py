import os
from pprint import pprint
from dotenv import load_dotenv
from googleapiclient.discovery import build
import helpers.custom_exceptions as ce
from services.logging_config import root_logger as logger

load_dotenv()


def get_single_video_url(video_id):
    """Fetches the URL of a single YouTube video given its ID"""
    return f"https://www.youtube.com/watch?v={video_id}"


def get_playlist_videos(playlist_ids, api_key, single_video_ids=[]):
    """Fetches all video URLs from YouTube playlists and single videos."""
    all_video_urls = []
    youtube = build("youtube", "v3", developerKey=api_key)

    # Process playlist videos
    for playlist_id in playlist_ids:
        try:
            video_urls = []
            next_page_token = None
            while True:
                pl_request = youtube.playlistItems().list(
                    part="contentDetails",
                    playlistId=playlist_id,
                    maxResults=50,
                    pageToken=next_page_token,
                )
                pl_response = pl_request.execute()
                video_ids = [
                    item["contentDetails"]["videoId"] for item in pl_response["items"]
                ]
                video_urls.extend(
                    [
                        f"https://www.youtube.com/watch?v={video_id}"
                        for video_id in video_ids
                    ]
                )
                next_page_token = pl_response.get("nextPageToken")
                if not next_page_token:
                    break
            all_video_urls.extend(video_urls)
        except Exception as e:
            logger.error(f"Error fetching videos for playlist {playlist_id}: {e}")

    # Process individual videos
    for video_id in single_video_ids:
        video_url = get_single_video_url(video_id)
        all_video_urls.append(video_url)

    return all_video_urls


if __name__ == "__main__":
    get_playlist_videos()
