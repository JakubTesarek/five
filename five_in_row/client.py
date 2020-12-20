from __future__ import annotations
import requests
import json
from five_in_row.model import Coord
from five_in_row import types as t


class JsonAuth(requests.auth.AuthBase):
    """Json body authentication."""
    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, req: requests.PreparedRequest) -> requests.PreparedRequest:
        """Set token to json body."""
        data = req.body
        if isinstance(data, bytes):
            data = str(data, 'utf-8')
        body = json.loads(str(data)) if req.body else {}
        body['userToken'] = self.token
        req.body = json.dumps(body).encode('utf-8')
        return req


class Client:
    """Piskvorky.jobs.cz client."""

    base_url = 'https://piskvorky.jobs.cz/api/v1'

    def __init__(self, token: str) -> None:
        self.session = self._create_session(token)

    def _create_session(self, token: str) -> requests.Session:
        """Create and configure requests session."""
        session = requests.Session()
        session.auth = JsonAuth(token)
        session.verify = True
        return session

    def connect_game(self) -> str:
        """Connect to new game."""
        req = self.session.post(f'{self.base_url}/connect')
        return req.json()['gameToken']

    def play_turn(self, game_token: str, coordinate: Coord) -> t.Any:
        """Play turn in a game."""
        req = self.session.post(f'{self.base_url}/play', json={
            'gameToken': game_token,
            'positionX': coordinate.x,
            'positionY': coordinate.y
        })
        return req.json()
