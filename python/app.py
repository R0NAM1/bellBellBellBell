import cryptocode, av, websockets, time, ast, logging, cv2, sys, io, os, argparse, asyncio, json, logging, ssl, uuid, base64, queue, signal, threading # Have to import for just firstRun because of global weirdness
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session, flash, send_from_directory, Markup, make_response, jsonify, send_file, Response
from flask_sock import Sock
from flask_login import LoginManager, UserMixin, login_user, current_user
from functools import wraps
from bs4 import BeautifulSoup
from io import BytesIO
from threading import Thread, active_count
from git import Repo
from waitress import serve # Production server
from sqlescapy import sqlescape
# Worry about imports later, will trim out fat!

# In program imports
from userManagement import verifyUserPassword
from database import checkIfDatabaseExists, doDatabaseQuery

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.init_app(app)

app.secret_key = 'IShouldBeUnique!' # Change this, as it's just good practice, generate some random hash string.

# app.config.update(
#     SESSION_COOKIE_SECURE=True,
#     SESSION_COOKIE_SAMESITE='None',
# )

# Customer User object that Flask_login requires, just takes a string and returns it as self.username (User(username))
# Also returns other flaskio funnies, is_active True, is_anon False, I handle all that logic.
class User(UserMixin):
    def __init__(self, username):
        self.username = username
    # All users can login
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    # Return username as ID
    def get_id(self):
        return self.username

global sigint;

# WELCOME TO bellBellBellBell!
# This is partially templated from zemond as I don't want to rewrite this all from scratch, but should be easy to create.


release_id = 'Alpha 0.1.0'

commit_id = ''

def sigint_handler(signum ,frame):
    print("SIGINT Received, exiting...")
    
    global sigint;
    sigint = True
    
    sys.exit(0)

def setCommitID():
    global commit_id
    repo = Repo("./")
    commit_id = repo.head.commit.hexsha
    commit_id = commit_id[:10] + "..."

# If not logged_in, make em!
# If there is no request.url, redirect to dashboard
# Else, redirect to request.url
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            session['wants_url'] = request.url
            return redirect(url_for('login'))
    return wrap

# Required Flaskio Decorator, calls my required User object that Flaskio likes
@login_manager.user_loader
def load_user(username):
    return User(username)

# Redirect to the dashboard if at root index
@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route('/favicon.ico')
def returnIcon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Route for handling the login page logic
@app.route('/login/', methods=['GET', 'POST'])
def login():
    session.pop('_flashes', None)
    error = None
    # POST REQUEST
    if request.method == 'POST':
        # Get inputted username and password, sanitize
        inputtedUsername = request.form['username']
        inputtedPassword = request.form['password']
        
        # Sanitize inputs with sqlescapy sqlescape object
        santizedUsername = sqlescape(inputtedUsername)
        santizedPassword = sqlescape(inputtedPassword)
        
        # Check if user actually exists in database
        # DO HERE incase somebody is bruteforcing logins with different names, real or not.
        if verifyUserPassword(santizedUsername, santizedPassword):
            # Verified password, permit login (Eventually integrate 2FA with FIDO or U2F)
            # Set user object for flask to santizedUsername
            # Register user with flask session by passing in username as string, and it makes it a user object same character set as string
            # "user" --> user (as instance of User())
            localUserObject = User(santizedUsername)
            # Login user to flask with flaskUser object
            login_user(localUserObject)
            # Set client session cookie logged_in to true so can access any page
            session['logged_in'] = True
            session.pop('_flashes', None)
            # Debug for finding issues with cookies
            # print(session)
            # Log in code should be finished
            flash('Your logged in!')
            print("Login!")
            # Redirect to dashboard when finished if requestedUrl is None, else redirect to requestedUrl
            if session['wants_url'] is None:
                return redirect(url_for('dashboard'))
            else:
                return redirect(session['wants_url'])
        else:
            # Could not verify password, give generic message
            session.pop('_flashes', None)
            flash('Username or Password is incorrect!')
        ## END POST

    # GET REQUEST
    return render_template('login.html', error=error, commit_id=commit_id, release_id=release_id)

@app.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None) # Pop goes the user session!
    flash('You were logged out for the following reason:')
    return redirect(url_for('index'))

@app.route('/zones/')
# @login_required
def zones():
    session.pop('_flashes', None)
    # Permission Check Dashboard
    return render_template('zones.html', commit_id=commit_id, release_id=release_id)

@app.route('/zones/<zone_label>')
# @login_required
def zone_examine(zone_label):
    session.pop('_flashes', None)
    
    # Query DB to check is string 'zone_label' exists in zones table
    # If query excepts then does not exist
    try:
        dbReturn = doDatabaseQuery("Select * from zones WHERE zone_label='{0}'".format(zone_label))[0]
        # Does exist, continue.
        return render_template('zone_schedule_show.html', commit_id=commit_id, release_id=release_id)
    
    except:
        # Does not exist, 
        return("Zone does not exist.")
        

def stopPyVoipDebug():
    # Copied from ChatGPT, I have no shame.
    class FilteredOutput:
        def __init__(self, unwanted_substring):
            self.unwanted_substring = unwanted_substring
            self._stdout = sys.stdout  # Store original stdout
            self.buffer = io.StringIO()  # Create an in-memory stream to capture stdout

        def write(self, message):
            if self.unwanted_substring not in message:
                self._stdout.write(message)  # Forward the message to original stdout

        def flush(self):
            self._stdout.flush()  # Make sure to propagate the flush to the original stdout

    # Example usage
    unwanted_substring = "TODO: Add 500 Error on Receiving SIP Response"

    # Redirect stdout to our custom FilteredOutput
    sys.stdout = FilteredOutput(unwanted_substring)

def startWebClient():
    # Testing Web Server
    # app.run(host='0.0.0.0')

    # Production web server
    print("Web Client Started.")
    serve(app, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    # For when needed
    # tracemalloc.start()
    
    checkIfDatabaseExists()
            
    setCommitID()
    stopPyVoipDebug()
    
    # Start bell watcher thread to check every second
    # bellWatchThreaden = Thread(target=bellWatchThread)
    # bellWatchThreaden.start()

    print("===== bellBellBellBell started! =====")

    print("Start Web Interface in 5 seconds...")
    
    # Register SIGINT Handler
    signal.signal(signal.SIGINT, sigint_handler)
    
    # Wait 5 seconds
    time.sleep(5)
    startWebClient()