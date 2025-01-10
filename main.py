
"""
This is the main loop file for our AutoTube Bot!

Quick notes!
- Currently it's set to try and post a video then sleep for a day.
- You can change the size of the video currently it's set to post shorts.
    * Do this by adding a parameter of scale to the image_save function.
    * scale=(width,height)
"""


from datetime import date
import os 
import shutil
import time
import random
from utils.CreateMovie import CreateMovie, GetDaySuffix

from utils.RedditBot import RedditBot
from utils.upload_video import upload_video



def delete_folders_in_directory(directory_path='AutoTube/data'):
    try:
        # Check if the given path is valid
        if not os.path.isdir(directory_path):
            print(f"Error: {directory_path} is not a valid directory.")
            return
        
        # List all items in the directory
        items = os.listdir(directory_path)
        for item in items:
            if item.endswith('.json'):
                items.remove(item)
        
        # Iterate through items and delete folders
        for item in items:
            item_path = os.path.join(directory_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"Deleted folder: {item_path}")
            else:
                print(f"Skipped non-folder item: {item_path}")
        
        print("All folders inside the specified directory have been deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

#Create Reddit Data Bot
redditbot = RedditBot()
# Leave if you want to run it 24/7
while True:
    i = 1
    # Gets our new posts pass if image related subs. Default is memes
    memes = ['dankmemes','memes','funny','HistoryMemes']
    val = random.randint(0,len(memes)-1)
    
    posts = redditbot.get_posts(memes[2])

    # Create folder if it doesn't exist
    redditbot.create_data_folder()

    # Go through posts and find 5 that will work for us.
    for post in posts:
        redditbot.save_image(post)

    # Wanted a date in my titles so added this helper
    DAY = date.today().strftime("%d")
    DAY = str(int(DAY)) + GetDaySuffix(int(DAY))
    dt_string = date.today().strftime("%A %B") + f" {DAY}"

    # Create the movie itself!
    CreateMovie.CreateMP4(redditbot.post_data)

    # Video info for YouTube.
    # This example uses the first post title.
    video_data = {
            "file": "video.mp4",
            "title":'memes for today  #memes #funnymemesthatwillmakeyourday #funny ##anime #mememondays',
            "description": "#shorts\nGiving you the hottest memes of the day with funny comments!",
            "keywords":"meme,reddit,Dankestmemes,funny,happy,new_year_meme,trending_meme",
            "privacyStatus":"public"
    }

    print(video_data["title"])
    print("Posting Video in 5 minutes...")
    upload_video(video_data)
    delete_folders_in_directory()

    # Sleep until ready to post another video!
    time.sleep(60 * 60)
    i += 1
    if i == 3:
        break