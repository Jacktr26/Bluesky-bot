from atproto import Client
from atproto_client.exceptions import NetworkError
import time

client = Client()

# 1) Login and post
login = client.login('yourhandle.bsky.social', 'YourPassword')
print(login.handle, login.display_name, login.followers_count)

post = client.send_post('Testing my Python script. Hey there, fellow football fans!')

# 2) Feed
feed = []  
try:
    data = client.get_timeline(limit=30)
    feed = data.feed
    next_page = data.cursor
    for item in feed:
        print(item.post)
except NetworkError as net_error:
    print(f"Something went wrong: {net_error}")


# 3) Generous Bot
def limit_handler(follower_bundle):
    try:
        while True and len(follower_bundle.followers) > 0:
            yield follower_bundle.followers.pop()
    except NetworkError as net_error:
        time.sleep(1000)


followers = client.get_followers(login.did)
for follower in limit_handler(followers):
    print(f"Follower: {follower}")
    if follower.display_name == "whomever":
        client.follow(follower.did)

# 4) Like Bot
search_string = 'Football'
number_of_posts = 2
count = 0

try:
    for item in feed:  # Ensure feed has been assigned before usage
        if item.post.record.text.find(search_string) > -1:
            count += 1
            client.like(item.post.uri, item.post.cid)
            if count >= number_of_posts:
                break
except NetworkError as net_error:
    print(net_error.response)
except StopIteration as stop_error:
    print(stop_error)
