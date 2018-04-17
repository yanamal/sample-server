#!/usr/bin/env python

# Import python libraries:
import logging, os
import json
import random

# Import third-party libraries:
from google.appengine.api import users
from flask import Flask,redirect,request,render_template

# Import our own files:
from profile import UserProfile
from nextpuzzle import nextPuzzle,progress

# make the flask app:
app = Flask(__name__)

# Set up debug messages, when not in "real world" production mode
production_environment = os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')
if not production_environment:
    app.debug = True
    logging.info('debugging!')

# When user goes to home page, redirect to static welcome page
@app.route('/')
def home():
  return redirect('/resources/welcome.html')

# when user goes to /next,
# figure out the next logical step for this user and redirect there.
@app.route('/next')
def nextStep():
  profile = UserProfile.get_by_user(users.get_current_user())
  return redirect(profile.current_puzzle)

# check the doc type quiz question
@app.route('/doctypeanswer')
def checkDocType():
  answer = request.args.get('struct') # get what was submitted in the struct field
  if answer == 'opt2': # compare to correct answer
    # if correct, then use the progress() function to progress from this puzzle
    return progress('resources/doctypequiz.html') # progress() takes in the name of the current puzzle, and returns a link to the next one
    # progress() also marks the current puzzle as solved for this user.
  else:
    # wrong answer - return a short snippet of HTML to send them back to the same quiz.
    return 'Sorry, that\'s wrong! <a href="/resources/doctypequiz.html">Try again?</a>'


# when user navigates to an autopass puzzle, either display the puzzle,
# or (if this is a correct solution) move on to the next puzzle
@app.route('/autopass/<puzzle>')
def render_autopass_puzzle(puzzle):
  # get passphrase that was submitted with this request, if any:
  submitted = request.args.get('pass')
  # get current user's passphrase:
  profile = UserProfile.get_by_user(users.get_current_user())
  # see if they submitted the correct one:
  if submitted and (submitted == profile.current_passphrase):
    profile.solved_puzzles.append('autopass/'+puzzle)
    profile.put()
    value = 'correct! '
    value += progress('autopass/'+puzzle)
    return value

  # fallthrough logic - incorrect or no passphrase submitted:

  # TODO: add extra output on pass submitted, but incorrect?
  # (but then it'd be outside of the manual HTML structure)

  # generate a new passphrase:
  passphrase = 'default'
  with app.open_resource('data/passphrases.json') as f:
    passphrases = json.load(f)
    passphrase = random.choice(passphrases)

  # store it in user's profile:
  profile.current_passphrase = passphrase
  profile.put()

  return render_template('autopass/'+puzzle, passphrase=passphrase)
