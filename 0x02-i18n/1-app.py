#!/usr/bin/env python3
"""Flask app with Babel for language support"""

from flask import Flask, render_template
from flask_babel import Babel

class Config:
    """Config class for setting app configurations."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Babel
babel = Babel(app)

@app.route('/')
def index():
    """Render the welcome page with Babel support."""
    return render_template('1-index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
