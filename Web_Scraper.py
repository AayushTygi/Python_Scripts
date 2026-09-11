import requests
from bs4 import BeautifulSoup
import json
import time

blog_link = "reycdxyc24gf7jrnwutzdn3smmweizedy7uojsa7ols6sflwu25ijoyd.onion"
rss_feed = f"https://{blog_link}/atom.xml"
filename = '0ut3r Space Scrape.txt'


def get_tor_session():
    session = requests.session()
    session.proxies = {'http': 'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Host": blog_link,
    })
    return session
    
def main():
    session = get_tor_session()
    r = session.get(rss_feed, timeout=60)
    if r.status_code == 200:
        # Get a list of posts from the RSS feed.
        posts_meta = get_posts_list(r.content)
        print(f"0ut3r Space Blog currently has {len(posts_meta.keys())} posts.")
    else:
        print('NOT OK.')
        exit()

    time.sleep(10)
    
    
        for post_id, post_dict in posts_meta.items():
        post_link = post_dict.get('post_link')
        if post_link:
            try:
                r = session.get(post_link, timeout=60)
            except requests.exceptions.ConnectionError as e:
                time.sleep(90)
                print(e)
                continue
            if r.status_code == 200:
                post_content = get_post_content(r.content)
                # Printing a snippet of the post content, as a way to ensure everything is going smoothly.
                print(post_content[0:100])
                posts_meta[post_id].update({"post_content": post_content})
        time.sleep(30)
        
            write_output(posts_meta)

# This function parses the XML content from the RSS feed, and creates a dictionary of all post metadata, for us to then iterate through and get the post content.

def get_posts_list(content):
    posts_meta = {}
    soup = BeautifulSoup(content, 'xml')
    for entry in soup.find_all("entry"):
        post_id = entry.id.string
        post_title = entry.title.string
        publication_date = entry.published.string
        post_link = entry.link.get('href')
        # The RSS feed has links to the clearweb version of the blog, however, in the context of this exercise, we want to be scraping the Tor version, so we'll replace all mentions of the clearweb website with our hidden service onion link.
        post_link = post_link.replace('http://0ut3r.space', f'https://{blog_link}')
        posts_meta[post_id] = {
            "post_title": post_title,
            "publication_date": publication_date,
            "post_link": post_link,
        }
    return posts_meta

# This function receives an HTML dump of the blog post's page, which we then parse with Beautiful Soup.
# As previously established, we want the content of the blog post, which is saved in a "div" with an "itemprop" attribute set to "articleBody".
# We'll extact all the paragraphs, and concatenate them into a single string for all the text found in the blog post.

def get_post_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    post_content = soup.find("div", attrs={"itemprop": "articleBody"})
    if post_content:
        texts = post_content.findAll(text=True)
        visibile_texts = [text.strip() for text in texts if text.strip()]
        return " ".join(text.strip() for text in visibile_texts)

# Easily enough, we can simply write our python dictionary as a json output using the built-in library.

def write_output(posts_meta):
    with open(filename, 'w') as output:
        json.dump(posts_meta, output)
        
def read_scrape():
    with open(filename, 'r') as file:
        data = file.read()
        json_data = json.loads(data)
        print(json.dumps(json_data, indent=4))


if __name__ == '__main__':
    main()
    print('Done Scraping!')
    read_scrape()