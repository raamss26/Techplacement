# app/routes.py
from flask import Blueprint, render_template, request
import requests
import os

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    quote = None
    error = None

    print("Current working directory:", os.getcwd())
    print("Templates folder should be located at:", os.path.join(os.getcwd(), 'templates'))

    if request.method == 'POST':
        if 'random' in request.form:
            try:
                response = requests.get('https://zenquotes.io/api/random')
                quote = response.json()[0]
            except Exception as e:
                error = str(e)
        elif 'author' in request.form:
            author = request.form['author']
            try:
                response = requests.get('https://zenquotes.io/api/quotes', params={'author': author})
                quotes = response.json()
                if quotes:
                    quote = quotes[0]
                else:
                    quote = {'q': 'No quotes found', 'a': ''}
            except Exception as e:
                error = str(e)

    print("Rendering template with quote:", quote, "and error:", error)
    return render_template('index.html', quote=quote, error=error)
