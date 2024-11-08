#!/usr/bin/env python3
"""Flask app with prioritized timezone selection."""
from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError

app = Flask(__name__)

# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

class Config:
    """Config for Babel."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)
babel = Babel(app)

def get_user():
    """Retrieve a user dictionary based on the 'login_as' URL parameter."""
    try:
        user_id = int(request.args.get("login_as"))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None

@app.before_request
def before_request():
    """Set the user in flask.g if logged in."""
    g.user = get_user()

@babel.localeselector
def get_locale():
    """Determine the best match for supported languages."""
    locale = request.args.get("locale")
    if locale in app.config['LANGUAGES']:
        return locale
    if g.user and g.user.get("locale") in app.config['LANGUAGES']:
        return g.user.get("locale")
    return request.accept_languages.best_match(app.config["LANGUAGES"])

@babel.timezoneselector
def get_timezone():
    """Determine the best match for time zones."""
    timezone = request.args.get("timezone")
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except UnknownTimeZoneError:
            pass

    if g.user:
        user_timezone = g.user.get("timezone")
        if user_timezone:
            try:
                return pytz.timezone(user_timezone).zone
            except UnknownTimeZoneError:
                pass

    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route("/")
def index():
    return render_template("7-index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
