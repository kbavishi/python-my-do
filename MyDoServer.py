#! /usr/bin/env python

import datetime
import json
import os
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
    if not request.json.get( "key" ):
      return "key not provided"
    if not validLogin( request.json.get( "key" ) ):
      return "Invalid login"
    if not request.json.get( "task_name" ):
       return "Task name not provided"
    text = "New task being added!\n"
    anyDoUsername = os.environ.get( "ANY_DO_USERNAME", "" )
    anyDoPassword = os.environ.get( "ANY_DO_PASSWORD", "" )
    api = AnyDoAPI( username=anyDoUsername, password=anyDoPassword )
    # Assume due date of tomorrow for now.
    tomorrow = datetime.datetime.today() + datetime.timedelta( hours=+24 )
    api.create_new_task( request.json.get( "task_name" ), due_day=tomorrow )
    return text

if __name__ == "__main__":
    port = int( os.environ.get( "PORT", 5000 ) )
    app.debug = True
    app.run( host='0.0.0.0', port=port )
