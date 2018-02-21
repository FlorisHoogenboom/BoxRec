import requests
from boxrec.services import FightServiceFactory

session = requests.Session()

# Dummy request to trick boxrec
session.post('http://boxrec.com')

# Use this endpoint to login
session.post(
    'http://boxrec.com/en/login',
    data={
        '_target_path': 'http://boxrec.com/',
        '_username': '{your username}',
        '_password': '{your password}',
        'login[go]': None
    },
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
)

# Make the service using the authenticated session
service = FightServiceFactory.make_service(session)

fight = service.find_by_id('763171', '2218493')
print(fight)

fights = service.find_by_date('2018-02-01')
print(fights)