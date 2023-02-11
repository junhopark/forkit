import pytest
from unittest.mock import MagicMock, patch


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_redirection(client):
    response = client.get('/login')
    assert response.status_code == 302


def test_oauth_callback_when_oauth_token_is_missing(client):
    with pytest.raises(ValueError):
        response = client.get('/oauth-callback')


@patch('requests.post')
def test_oauth_callback_when_access_token_cannot_be_retrieved(mock_get, client):
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_get.side_effect = [mock_response]
    response = client.get('/oauth-callback?code=test')
    assert response.data.decode('utf-8').__contains__("Authorization failed")


@patch('requests.post')
def test_oauth_callback_when_forking_attempt_failed(mock_get, client):
    mock_response_1 = MagicMock()
    mock_response_1.status_code = 200
    mock_response_1.json.return_value = {'access_token': 'fake_token'}

    mock_response_2 = MagicMock()
    mock_response_2.status_code = 500

    mock_get.side_effect = [mock_response_1, mock_response_2]

    response = client.get('/oauth-callback?code=test')

    assert response.data.decode('utf-8').__contains__("Error occurred")


@patch('requests.post')
def test_oauth_callback_when_forking_attempt_is_successful(mock_get, client):
    mock_response_1 = MagicMock()
    mock_response_1.status_code = 200
    mock_response_1.json.return_value = {'access_token': 'fake_token'}

    mock_response_2 = MagicMock()
    mock_response_2.status_code = 202

    mock_get.side_effect = [mock_response_1, mock_response_2]

    response = client.get('/oauth-callback?code=test')

    assert response.data.decode('utf-8').__contains__("Success!")
