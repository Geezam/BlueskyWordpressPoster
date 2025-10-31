# Bluesky Wordpress Poster

A Python bot that automatically fetches a random post from a specific category on your WordPress blog and shares it on Bluesky.

The script is designed to run on a specified schedule and post on your behalf, complete with a rich embed link card and a featured image.



## Features

* **Randomized Posting:** Selects a random post from the 100 most recent posts in a specified WordPress category.
* **Anti-Repetition:** Maintains a local history file of the last x posts to ensure the same article isn't shared too frequently.
* **Natural Timing:** Includes a random customizable startup delay to make posting times less robotic and more human-like.
* **Content-Aware:** Fetches the main post content (not the "excerpt"), cleanly strips all HTML tags, and truncates it to a specified length.
* **Guaranteed Link Card:** Generates a rich embed (link card) with a guaranteed thumbnail. It does this by downloading the post's featured image, uploading it to Bluesky as a blob, and manually attaching it to the embed.

## How it Works

1.  **Run:** The script is executed by a scheduler.
2.  **Delay:** It first waits for a random/specified amount of time.
3.  **Fetch:** It calls the WordPress REST API to get the 100 most recent posts from your chosen category, along with their embedded featured image URLs.
4.  **Read History:** It checks a recent posts file to see the links of the last X posts.
5.  **Select:** It shuffles the 100 posts and finds the first one that is *not* in the history.
6.  **Embed:** It downloads the featured image for the selected post.
7.  **Login:** It logs into Bluesky and creates the post and publishes it
8. **Write History:** Finally, it adds the new post's link to recent posts record

## License

This project is licensed under the MIT License.