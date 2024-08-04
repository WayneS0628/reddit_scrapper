import praw
import os
import requests
from urllib.parse import urlparse

reddit = praw.Reddit(
    client_id='PWz3to44L9gBAeGlmGJIyQ',
    client_secret='ldbssf_yAdcKFSzG0sKMNlvUaJ3Q8Q',
    user_agent='storyvault/1.0 by StoryVault628'
)

def get_top_stories(subreddit, limit=10):
    subreddit_obj = reddit.subreddit(subreddit)
    stories = []
    for submission in subreddit_obj.top(limit=limit, time_filter = "day"):
        story = {
            'title': submission.title,
            'selftext': submission.selftext,
            'url': submission.url,
            'is_video': submission.is_video,
            'post_hint': getattr(submission, 'post_hint', None)
        }
        stories.append(story)
    return stories

def save_stories_to_files(subreddit, stories, base_dir='/system/volumes/data/volumes/youtube/storyvault/shit'):
    # Create subreddit directory if it doesn't exist
    subreddit_dir = os.path.join(base_dir, subreddit)
    if not os.path.exists(subreddit_dir):
        os.makedirs(subreddit_dir)

    for i, story in enumerate(stories):
        story_filename = os.path.join(subreddit_dir, f'story_{i+1}.txt')
        with open(story_filename, 'w', encoding='utf-8') as file:
            file.write(f"Title: {story['title']}\n\n")
            file.write(f"Text: {story['selftext']}\n\n")
            file.write(f"URL: {story['url']}\n")

        # Save image or video if available
        if story['post_hint'] == 'image':
            save_media(story['url'], subreddit_dir, f'image_{i+1}')
        elif story['is_video']:
            save_media(story['url'], subreddit_dir, f'video_{i+1}')

def save_media(url, directory, filename):
    # Extract file extension
    parsed_url = urlparse(url)
    ext = os.path.splitext(parsed_url.path)[-1]
    if ext:
        media_filename = os.path.join(directory, f"{filename}{ext}")
        response = requests.get(url)
        if response.status_code == 200:
            with open(media_filename, 'wb') as file:
                file.write(response.content)

# Example usage
# subreddits = ['AmItheAsshole', 'relationships', 'tifu', 'nosleep', 'confessions']
# for subreddit in subreddits:

difsubs = {'ass': 'AmItheAsshole', 'relation': 'relationships', 'today': 'tifu', 'no': 'nosleep', 'confessions': 'confessions', 'mildly': 'mildlyinfuriating', 'odd': 'oddlyspecific', 'shower': 'Showerthoughts'}
sub = difsubs[input('Enter first word of subreddit: ')]
stories = get_top_stories(sub, int(input('Enter number of posts you want to be pulled: ')))  # Replace 5 with the desired number of stories
save_stories_to_files(sub, stories)
