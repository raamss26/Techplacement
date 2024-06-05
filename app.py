from flask import Flask, Blueprint, render_template, request
import requests
import os

# Create a Blueprint object for main routes
main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    # Initialize variables
    quote = None
    error_message = None

    # Handle POST request
    if request.method == 'POST':
        try:
            # Check if 'random' button is clicked
            if 'random' in request.form:
                # Fetch a random quote
                response = requests.get('https://zenquotes.io/api/random')
                response.raise_for_status()  # Raise an exception if request fails
                quote = response.json()[0]  # Extract the first quote from the response
            # Check if 'author' search button is clicked
            elif 'author' in request.form:
                # Get the author name from the form
                author = request.form['author']
                # Fetch quotes by the specified author
                response = requests.get('https://zenquotes.io/api/quotes', params={'author': author})
                response.raise_for_status()  # Raise an exception if request fails
                quotes = response.json()
                # Select the first quote if available, otherwise, provide a default message
                quote = quotes[0] if quotes else {'q': 'No quotes found', 'a': ''}
        # Handle exceptions raised during the API request
        except requests.exceptions.RequestException as e:
            error_message = f"Error fetching quote: {str(e)}"

    # If there's an error, render the error template; otherwise, render the index template
    template = 'error.html' if error_message else 'index.html'
    return render_template(template, quote=quote, error_message=error_message)

# Create the Flask application instance
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# Register the main Blueprint
app.register_blueprint(main)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
