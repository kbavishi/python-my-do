#! /usr/bin/env python

import datetime
import json
import os
import time
from flask import Flask, request
from anydo.api import AnyDoAPI

app = Flask(__name__)

def validLogin( key ):
    assert os.environ.get( "IFTTT_KEY" )
    return key == os.environ.get( "IFTTT_KEY" )

@app.route("/")
def hello():
    return "Hello world!"

@app.route( "/add_task", methods=[ 'POST' ] )
def addTask():
    assert request.method == 'POST'

    # Verify that key arguments were provided
    if not request.json.get( "key" ):
      return "Key not provided"
    if not validLogin( request.json.get( "key" ) ):
      return "Invalid login"
    if not request.json.get( "task_name" ):
       return "Task name not provided"

    text = "New task being added!\n"

    # Login with the Any.Do credentials
    anyDoUsername = os.environ.get( "ANY_DO_USERNAME", "" )
    anyDoPassword = os.environ.get( "ANY_DO_PASSWORD", "" )
    api = AnyDoAPI( username=anyDoUsername, password=anyDoPassword )

    if not request.json.get( "due_date" ):
      # Assume a default due date of tomorrow, if nothing is provided.
      due_day = datetime.datetime.today() + datetime.timedelta( hours=+24 )
    else:
      # Expected to be in a certain format. Eg: November 21, 2006 at 04:30PM
      dateFormat = "%B %d, %Y at %I:%M%p"
      # Convert to struct_time
      date_struct_time = time.strptime( request.json[ "due_date" ], dateFormat )
      # Convert from struct_time to datetime
      due_day = datetime.datetime.fromtimestamp( time.mktime( date_struct_time ) )

    # Create the task
    api.create_new_task( request.json.get( "task_name" ), due_day=due_day )

    return text

if __name__ == "__main__":
    port = int( os.environ.get( "PORT", 5000 ) )
    app.debug = True
    app.run( host='0.0.0.0', port=port )
