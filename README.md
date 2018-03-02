# Boxrec
This repository provides a very simple Python wrapper around the Boxrec.com website. The goal is to provide an easy way to access the information presented on the Boxrec website without having to go through the whole DOM-tree yourself.

# How do I use this?
The easiest way to instantiate a full representation of fights and boxers on boxrec.com is to use the `FightServiceFactory.make_service()` method in `boxrec.services`. An example is given below
```python
from boxrec.services import FightServiceFactory
fight_service = FightServiceFactory.make_service()

result = fight_service.find_by_id({event_id}, {fight_id})
```
The variable result now contains statistics of the fight, and also contains references to objects representing the two boxers involved.

As starting point, there's a list of fight URIs in /boxrec/data/.

# Some words on authentication
I've noticed that after a certain amount of requests Boxrec seems to require authentication for you to view any extra pages. Currently, this library does no facilitate this. However you can pass a `requests` Session object to the `FightServiceFactory.make_service()` method. Your service will then use this session for any communication to the Boxrec website. You should be able to authenticate in this session yourself. See the code below to give you an idea how to do this
```python
import requests
from boxrec.services import FightServiceFactory

session = requests.Session()

# Use this endpoint to login
session.post(
    'http://boxrec.com/en/login',
    data={
        '_target_path': 'http://boxrec.com/',
        '_username': '{Your user name}',
        '_password': '{Your password{',
        'login[go]': None
    },
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
)

# Create the service using the authenticated session
fight_service = FightServiceFactory.make_service(session)
```
One small exta note: I've noticed boxrec does not allow logging in on the first request. Hence, one should make a dummy request on the session before actually authenticating using the code above.
