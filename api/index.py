from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin

app = Flask(__name__)
pattern_http = re.compile(r'(https?://)?\S+')

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

def fetch_external_content(url):
    try:
        response = requests.get(url)

        if response.status_code != 200:
            return None

        return response.text
    except Exception as e:
        return None

def extract_and_modify_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')

    # Modify resource URLs to be absolute
    for tag in soup.find_all(['link', 'script', 'img'], href=True, src=True):
        tag['href'] = urljoin(base_url, tag.get('href'))
        tag['src'] = urljoin(base_url, tag.get('src'))

    return str(soup)

@app.route("/<path:url>")
def display_external_content(url):
    url = 'https://' + url.replace('http://', '').replace('https://', '')
    content = fetch_external_content(url)

    if content is not None:
        base_url = url + '/'
        modified_content = extract_and_modify_html(content, base_url)
        return render_template("display.html", content=modified_content)

    return f"Failed to retrieve content from {url}."
    