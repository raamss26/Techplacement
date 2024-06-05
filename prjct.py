from flask import Flask
from flask import Blueprint, render_template, request
import requests


def create_app():
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)

    return app


main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    quote = None
    error = None

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
                quote = quotes[0] if quotes else {'q': 'No quotes found', 'a': ''}
            except Exception as e:
                error = str(e)

    return render_template('index.html', quote=quote, error=error)
