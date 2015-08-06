#! /usr/bin/env python

import json
import os
import requests
import DisplayStrings
from anydo.api import AnyDoAPI

headers = { 'Content-Type': 'application/json' }

ideal_payload = { 'key': os.environ.get( 'IFTTT_KEY' ),
                  'task_name': 'Trial task',
                  'due_date': "August 6, 2015 at 09:00AM" }

def cleanupDummyTask():
    # Login with the Any.Do credentials
    anyDoUsername = os.environ.get( 'ANY_DO_USERNAME', '' )
    anyDoPassword = os.environ.get( 'ANY_DO_PASSWORD', '' )
    api = AnyDoAPI( username=anyDoUsername, password=anyDoPassword )

    # Cycle through all tasks and find the dummy task
    task_id = None
    for task in api.get_all_tasks():
        if task[ 'title' ] == ideal_payload[ 'task_name' ]:
            task_id = task[ 'id' ]
            break

    if task_id:
        api.delete_task_by_id( task_id )

def verifyTaskAdded():
    # Login with the Any.Do credentials
    anyDoUsername = os.environ.get( 'ANY_DO_USERNAME', '' )
    anyDoPassword = os.environ.get( 'ANY_DO_PASSWORD', '' )
    api = AnyDoAPI( username=anyDoUsername, password=anyDoPassword )

    # Cycle through all tasks and verify that the required task exists
    for task in api.get_all_tasks():
        if task[ 'title' ] == ideal_payload[ 'task_name' ]:
            return True
    return False

def requestPassTest():
    """
    Verifies that a task was successfully added, if a request with a due date
    is POSTed.
    """
    payload = ideal_payload.copy()
    r = requests.post( "http://localhost:5000/add_task",
                       data=json.dumps(payload), headers=headers )
    assert r.ok
    assert DisplayStrings.TASK_ADD_SUCCESSFUL in r.content
    assert verifyTaskAdded()
    cleanupDummyTask()

def requestWithoutDueDatePassTest():
    """
    Verifies that a task was successfully added, if a request without a due
    date is POSTed.
    """
    payload = ideal_payload.copy()
    del payload[ 'due_date' ]
    r = requests.post( "http://localhost:5000/add_task",
                       data=json.dumps(payload), headers=headers )
    assert DisplayStrings.TASK_ADD_SUCCESSFUL in r.content
    assert verifyTaskAdded()
    cleanupDummyTask()

def keyNotProvidedTest():
    """
    Verifies that if a key is not provided, the server returns an error.
    """
    payload = ideal_payload.copy()
    del payload[ 'key' ]
    r = requests.post( "http://localhost:5000/add_task",
                       data=json.dumps(payload), headers=headers )
    assert DisplayStrings.KEY_NOT_PROVIDED_ERROR in r.content

def invalidKeyProvidedTest():
    """
    Verifies that if an invalid key is provided, the server returns an error.
    """
    payload = ideal_payload.copy()
    payload[ 'key' ] = '42'
    r = requests.post( "http://localhost:5000/add_task",
                       data=json.dumps(payload), headers=headers )
    assert DisplayStrings.INVALID_KEY_ERROR in r.content

def noTaskNameProvidedError():
    """
    Verifies that if no task name is provided, the server returns an error.
    """
    payload = ideal_payload.copy()
    del payload[ 'task_name' ]
    r = requests.post( "http://localhost:5000/add_task",
                       data=json.dumps(payload), headers=headers )
    assert DisplayStrings.NO_TASK_NAME_ERROR in r.content

def invalidDueDateProvidedTest():
    """
    Verifies that if due date is provided in an invalid format, the server
    returns an error.
    """
    payload = ideal_payload.copy()
    payload[ 'due_date' ] = 'Random unparsable date'
    r = requests.post( "http://localhost:5000/add_task",
                       data=json.dumps(payload), headers=headers )
    assert DisplayStrings.INVALID_DATE_FORMAT_ERROR in r.content

def setupEnv():
    """Reads from .env file and sets up environment"""
    if not os.path.exists( ".env" ):
        return

    lines = open( ".env", "r" ).readlines()
    for line in lines:
        key, val = line.strip().split( '=' )
        os.environ[ key ] = val

    # Need to replace stored key
    ideal_payload[ 'key' ] = os.environ.get( 'IFTTT_KEY' )

if __name__ == '__main__':
    setupEnv()
    cleanupDummyTask()
    # Assumes that 'foreman start web' was run before running test
    keyNotProvidedTest()
    invalidKeyProvidedTest()
    noTaskNameProvidedError()
    invalidDueDateProvidedTest()
    requestPassTest()
    cleanupDummyTask()
