This program runs a server that listens to two different crypto exchanges websockets and displays the data in real time on a basic webpage.

# How to run

Clone the project.

Setup a python3 virtual environment. This was developed against Python 3.7, but should be compatible back to 3.5.3.

You will need python3, pip and virtualenv installed.

Setup virtualenv

`python3 -m venv {env}`

{env} can be anything you like. Even just env.

Start the virtualenv

`. {env}/bin/activate`

{env} being the same as above.

Next, install dependencies. 

`pip install -r requirements.txt`

Now create a file named `.env` and it's only contents need to be `SECRET="secret!"` You could assign any value you like actually.

To run the server,

`python3 server.py`

Now the page will be hosted at `localhost:5000`

If everything went as planned, once you navigate to `localhost:5000` you will see a basic page which will start blank. But after a few seconds should begin populating data in real time. 

# The Problem

`Display a running list of the time (in UTC), best bid, best ask, and the last traded price on any pair on two different crypto exchanges.`

The problem as I approached it was to listen to two different websocket streams and also update the information in real time on a basic web page. I created a base class ExchangeListener and extended a child class for each exchange. This is because each exchange has different requirements and it makes it easier to expand functionality and add additional exchanges.

Alternatively I could have setup an event loop with asyncio and polled the RESTapi. 

For the front end I chose to keep it simple and use a basic flask application. This uses socketIO to pass data back and forth from the server to the page. I tossed in bootstrap to make it slightly better on the eyes with minimal effort. But it is otherwise overkill for this simple project at it's current state. 

### Enhancements

Navigating to the page initially shows a black page. This could be mitigated by either storing the collected data in a database or making calls to the rest API to back fill the data if desired.

For the front end, adding d3 would have been a fairly simple next step to better display and organize the data.
