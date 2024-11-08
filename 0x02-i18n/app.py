from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from datetime import datetime

app = Flask(__name__)

# Configure Babel and available languages
class Config:
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app.config.from_object(Config)
babel = Babel(app)

# Mock user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user():
    """Fetch the user if login_as parameter is provided"""
    user_id = request.args.get("login_as", type=int)
    return users.get(user_id)

@app.before_request
def before_request():
    """Set up the user for the request"""
    g.user = get_user()

@babel.localeselector
def get_locale():
    """Determine the best match with supported languages"""
    # Check for locale in URL parameters
    locale = request.args.get("locale")
    if locale and locale in app.config['LANGUAGES']:
        return locale
    # Check user settings
    user = g.get("user", None)
    if user and user.get("locale") in app.config['LANGUAGES']:
        return user.get("locale")
    # Fallback to request headers
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    """Determine the best timezone setting"""
    # Check for timezone in URL parameters
    timezone = request.args.get("timezone")
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except pytz.UnknownTimeZoneError:
            pass
    # Check user settings
    user = g.get("user", None)
    if user:
        try:
            return pytz.timezone(user.get("timezone")).zone
        except pytz.UnknownTimeZoneError:
            pass
    # Fallback to default
    return app.config['BABEL_DEFAULT_TIMEZONE']

@app.route('/')
def index():
    """Main route for the app displaying the current time"""
    user_timezone = get_timezone()
    try:
        tz = pytz.timezone(user_timezone)
    except pytz.UnknownTimeZoneError:
        tz = pytz.UTC

    # Get the current time in the user's timezone and format it
    current_time = datetime.now(tz)
    formatted_time = babel.dates.format_datetime(current_time, locale=get_locale())
    return render_template('index.html', current_time=formatted_time)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
