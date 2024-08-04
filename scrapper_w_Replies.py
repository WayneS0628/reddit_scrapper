import praw
import os
import requests
from urllib.parse import urlparse

reddit = praw.Reddit(
    client_id='PWz3to44L9gBAeGlmGJIyQ',
    client_secret='ldbssf_yAdcKFSzG0sKMNlvUaJ3Q8Q',
    user_agent='storyvault/1.0 by StoryVault628'
)

def get_top_posts_and_comments(subreddit, post_limit=3, comment_limit=10):
    subreddit_obj = reddit.subreddit(subreddit)
    posts = []

    for submission in subreddit_obj.top(limit=post_limit, time_filter = "week"):
        post_data = {
            'title': submission.title,
            'selftext': submission.selftext,
            'url': submission.url,
            'media_url': None,
            'comments': []
        }

        # Check if the post has media
        if submission.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
            post_data['media_url'] = submission.url
        elif submission.is_video:
            post_data['media_url'] = submission.url

        submission.comment_sort = 'top'
        submission.comments.replace_more(limit=0)  # Avoid fetching more comments

        top_comments = submission.comments.list()[:comment_limit]
        for comment in top_comments:
            post_data['comments'].append({
                'author': comment.author.name if comment.author else 'deleted',
                'text': comment.body
            })

        posts.append(post_data)
    
    return posts

def save_posts_and_comments(subreddit, posts, base_dir='/system/volumes/data/volumes/youtube/storyvault/shit'):
    # Create subreddit directory if it doesn't exist
    subreddit_dir = os.path.join(base_dir, subreddit)
    if not os.path.exists(subreddit_dir):
        os.makedirs(subreddit_dir)

    for i, post in enumerate(posts):
        post_filename = os.path.join(subreddit_dir, f'post_{i+1}.txt')
        with open(post_filename, 'w', encoding='utf-8') as file:
            file.write(f"Title: {post['title']}\n\n")
            file.write(f"Text: {post['selftext']}\n\n")
            file.write(f"URL: {post['url']}\n\n")
            if post['media_url']:
                file.write(f"Media URL: {post['media_url']}\n")
                save_media(post['media_url'], subreddit_dir, f'media_{i+1}')
            file.write("Top Comments:\n")
            for j, comment in enumerate(post['comments']):
                file.write(f"Comment {j+1} by {comment['author']}:\n")
                file.write(f"{comment['text']}\n\n")

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
subreddit = 'AskReddit'
posts = get_top_posts_and_comments(subreddit, 10, 10)
save_posts_and_comments(subreddit, posts)
