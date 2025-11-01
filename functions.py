import requests
import os
import html
import re
from atproto import models
from engine import (BLOG_URL, CATEGORY_ID, EXCERPT_LENGTH, STATE_FILE,
                    MAX_HISTORY)


def clean_html(raw_html):
    """Strips all HTML tags from a string."""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_featured_posts(count):

    api_url = (f"{BLOG_URL}/wp-json/wp/v2/posts?"
               f"_embed&categories={CATEGORY_ID}&per_page={count}")

    response = requests.get(api_url)
    response.raise_for_status()

    posts = response.json()
    if not posts:
        print("No posts found in the 'featured' category.")
        return []

    formatted_posts = []
    print(len(posts))
    for post in posts:

        post_title = html.unescape(post['title']['rendered'])
        post_link = post['link']
        image_url = post['_embedded']['wp:featuredmedia'][0]['source_url']

        content_html = post['content']['rendered']

        post_excerpt = ""
        if content_html:
            full_content = html.unescape(clean_html(content_html)).strip()

            if len(full_content) > EXCERPT_LENGTH:
                truncate_at = full_content.rfind(' ', 0, EXCERPT_LENGTH)
                if truncate_at == -1:
                    truncate_at = EXCERPT_LENGTH
                post_excerpt = full_content[:truncate_at] + "..."
            else:
                post_excerpt = full_content

        formatted_posts.append({
            "title": post_title,
            "link": post_link,
            "excerpt": post_excerpt.strip(),
            "image_url": image_url
        })

    return formatted_posts


def post_to_bluesky(post, client):
    title = post['title']
    excerpt = post['excerpt']
    link = post['link']
    image_url = post['image_url']

    post_text = f"{title}\n\n{excerpt}"

    if len(post_text) > 300:
        post_text = f"{title}\n\n{link}"

    image_response = requests.get(image_url)
    image_data = image_response.content
    uploaded_thumb = client.upload_blob(image_data)

    embed_external = models.AppBskyEmbedExternal.Main(
        external=models.AppBskyEmbedExternal.External(
            uri=link,
            title=title,
            description=excerpt,
            thumb=uploaded_thumb.blob
        )
    )

    client.send_post(
        text=post_text,
        embed=embed_external
    )


def get_recently_posted_links():
    if not os.path.exists(STATE_FILE):
        return []
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f.readlines()]
        return links


def update_recently_posted_links(recent_links, new_link):
    recent_links.insert(0, new_link)
    links_to_save = recent_links[:MAX_HISTORY]
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(links_to_save))
