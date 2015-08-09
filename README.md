# python-my-do

## Introduction

A simple Flask server which can handle POST requests and create tasks in your [Any.do](http://www.any.do) account. 

My main intention here was to have an interface between my [IFTTT](http://www.ifttt.com) recipes and my Any.do account. IFTTT doesn't have the Any.do channel yet, and I needed a way to add tasks based on certain triggers. Eg: Add a task to bring an umbrella if there is rain in the weather forecast for tomorrow.

## Example Usecases

Add IFTTT recipes to:

1. Add task to bring an umbrella if there is rain forecasted for tomorrow.
2. Add task to your Any.do when a task is added to your Trello board (Trello to Any.do sync essentially)

## Requirements

Run ```setup.py``` before trying to deploy the server. It will ask for your Any.do credentials and a key to help identify your IFTTT recipe. The IFTTT key is needed so that your server is not exposed to unauthorized requests.

## Setup instructions

1. Run ```setup.py``` and enter your IFTTT key, and Any.do credentials.
```
kbavishi:my-do karan$ python setup.py
Enter the key to be used to authenticate the IFTTT recipe:
Enter your Any.do username: someone@gmail.com
Enter your Any.do password:
```
2. Install dependencies.
```
kbavishi:my-do karan$pip install -r requirements.txt
```
3. Deploy your server on Heroku.
```
kbavishi:my-do karan$heroku create
kbavishi:my-do karan$git push heroku master
kbavishi:my-do karan$heroku ps:scale web=1
```
4. Verify that the server is running correctly by looking at logs
```
kbavishi:my-do karan$heroku open
```

## Testing

You should run ```foreman start web``` and then run ```python ServerTest.py``` to verify that your changes are working locally.
