from server import app
from utils import read_json_from_file
import json

# TESTS (nose)
class ServerTests(object):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_status_code(self):
        result = self.app.get('/hello')
        assert result.status_code == 200
        assert result.data == 'Hello\n'

    def test_send_accept_html(self):
        sample_data=read_json_from_file("./sample.json")
        result = self.app.post('/send', data=json.dumps(sample_data), headers={'Content-Type' : 'application/json', 'Accept' : 'text/html'})
        assert result.status_code == 200
        assert result.headers.get('Content-Type', '').find('text/html') != -1

    def test_send_accept_json(self):
        sample_data=read_json_from_file("./sample.json")
        result = self.app.post('/send', data=json.dumps(sample_data), headers={'Content-Type' : 'application/json', 'Accept' : 'application/json'})
        assert result.status_code == 200
        assert result.headers.get('Content-Type', '').find('application/json') != -1



