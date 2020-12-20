import pytest
from five.client import Client
from five.model import Coord


@pytest.mark.unit
class TestClient:
    def test_connect_game(self, requests_mock):
        requests_mock.post('https://piskvorky.jobs.cz/api/v1/connect', text='''{
            "statusCode": 201,
            "gameToken": "3824239b-0b7c-4690-84dd-5eed7d527f14",
            "gameId": "3f50b79f-0fad-404f-b44c-1e3207edfb45",
            "headers": {}
        }''')

        client = Client('user_key')
        game_token = client.connect_game()

        assert game_token == '3824239b-0b7c-4690-84dd-5eed7d527f14'

    def test_play_turn(self, requests_mock):
        requests_mock.post('https://piskvorky.jobs.cz/api/v1/play', text='''{
            "key": "value"
        }''')

        client = Client('user_key')
        play_result = client.play_turn('game_token', Coord(1, 1))

        assert play_result == {
            'key': 'value'
        }