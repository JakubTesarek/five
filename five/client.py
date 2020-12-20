import requests
import json


class JsonAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, req):
        body = json.loads(req.body.decode('utf-8')) if req.body else {}
        body['userToken'] = self.token
        req.body = json.dumps(body).encode('utf-8')
        print(req.body)
        return req


class Client:
    base_url = 'https://piskvorky.jobs.cz/api/v1'

    def __init__(self, token):
        self.session = self._create_session(token)

    def _create_session(self, token):
        session = requests.Session()
        session.auth = JsonAuth(token)
        session.verify = True
        return session

    def connect_game(self):
        req = self.session.post(f'{self.base_url}/connect')
        return req.json()['gameToken']

    def play_turn(self, game_token, coordinate):
        req = self.session.post(f'{self.base_url}/play', json={
          'gameToken': game_token,
          'positionX': coordinate.x,
          'positionY': coordinate.y
        })
        return req.json()

