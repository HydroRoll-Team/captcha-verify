from flask import Flask, render_template
import requests
import re

app = Flask(__name__)
pattern_http = re.compile(r'(https?://)?\S+')

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route("/<path:url>")
def display_external_content(url):
    url = 'https://' + url.replace('http://', '').replace('https://', '')
    try:
        response = requests.get(url)

        if response.status_code != 200:
            return f"Failed to retrieve content from {url}. Status code: {response.status_code}"

        return render_template("display.html", content=response.text)
    except Exception as e:
        return f"An error occurred: {str(e)}"
