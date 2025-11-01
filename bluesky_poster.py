from atproto import Client
import random
import time
from engine import (FETCH_POST_COUNT, BSKY_HANDLE, BSKY_APP_PASSWORD,
                    MAX_DELAY_SECONDS)
from functions import (get_featured_posts, post_to_bluesky,
                       get_recently_posted_links, update_recently_posted_links)

random_delay = random.randint(0, MAX_DELAY_SECONDS)

print(f"--- Bot started. Sleeping for {random_delay // 60} minutes"
      f"and {random_delay % 60} seconds. ---")

#time.sleep(random_delay)

recent_links = get_recently_posted_links()

candidate_posts = get_featured_posts(count=FETCH_POST_COUNT)

random.shuffle(candidate_posts)
post_to_share = None

for post in candidate_posts:
    if post['link'] not in recent_links:
        post_to_share = post
        break
print("Picked: " + post['title'])

client = Client()
client.login(BSKY_HANDLE, BSKY_APP_PASSWORD)

#post_to_bluesky(post_to_share, client)

update_recently_posted_links(recent_links, post_to_share['link'])
