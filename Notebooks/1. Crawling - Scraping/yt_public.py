import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from iteration_utilities import unique_everseen

from utils.comments import process_comments, make_csv

load_dotenv()
API_KEY = os.getenv("API_KEY")

youtube = build("youtube", "v3", developerKey=API_KEY)

def comment_threads(channelID, to_csv=True):
    
    comments_list = []
    
    request = youtube.commentThreads().list(
        part='id,replies,snippet',
        videoId=channelID,
    )
    response = request.execute()
    comments_list.extend(process_comments(response['items']))

    # if there is nextPageToken, then keep calling the API
    while response.get('nextPageToken', None):
        request = youtube.commentThreads().list(
            part='id,replies,snippet',
            videoId=channelID,
            pageToken=response['nextPageToken']
        )
        response = request.execute()
        comments_list.extend(process_comments(response['items']))

    comments_list = list(unique_everseen(comments_list))

    print(f"Finished fetching comments for {channelID}. {len(comments_list)} comments found.")
    
    if to_csv:
        make_csv(comments_list, channelID)
    
    return comments_list


if __name__ == '__main__':
    channelId = 'yiffzzl7EFY'

    response = comment_threads(channelId)

    print(response)