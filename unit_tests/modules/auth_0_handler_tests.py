import unittest
from unittest.mock import patch, MagicMock
from src.modules.auth_0_handler import Auth0Handler


class TestAuth0Handler(unittest.TestCase):

    @patch('requests.post')
    @patch('modules.SecretsManager')
    def test_get_test_token(self, MockSecretsManager, mock_post):
        # Setup the mocked SecretsManager to return specific client id and secret
        mock_secrets_manager = MockSecretsManager.return_value
        mock_secrets_manager.get_secret.side_effect = ['test_client_id', 'test_client_secret']

        # Setup the mocked requests.post to return a specific access token
        mock_response = MagicMock()
        mock_response.json.return_value = {'access_token': 'test_access_token'}
        mock_post.return_value = mock_response

        auth0_handler = Auth0Handler(mock_secrets_manager, 'test_domain')
        token = auth0_handler.get_test_token()

        self.assertEqual(token, 'test_access_token')

        # Verify that the mocked methods were called with the correct arguments
        MockSecretsManager.assert_called_once()
        mock_secrets_manager.get_secret.assert_any_call('auth0_client_id_test')
        mock_secrets_manager.get_secret.assert_any_call('auth0_client_secret_test')
        mock_post.assert_called_once_with(
            'https://test_domain/oauth/token',
            headers={'content-type': 'application/json'},
            json={
                "client_id": 'test_client_id',
                "client_secret": 'test_client_secret',
                "audience": 'https://test_domain/api/v2/',
                "grant_type": "client_credentials"
            }
        )

# TODO: add exhaustive tests


if __name__ == '__main__':
    unittest.main()
