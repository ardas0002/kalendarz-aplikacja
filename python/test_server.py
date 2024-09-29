import unittest
from unittest.mock import patch
from server import app

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('server.requests.get')
    def test_get_events_success(self, mock_get):

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                "id": 3,
                "name": "Jubileuszowy Piknik Naukowy z Uniwersytetem w Siedlcach",
                "start_time": "2024-10-02T10:00:00",
                "duration": 2,
                "image_url": "/media/442435186_947649987362224_3464617144294814090_n.webp",
                "short_description": "Jubileuszowy Piknik Naukowy UwS to dzień pełen atrakcji dla dzieci i dorosłych, z warsztatami, grami i występami.",
                "tags": [
                    {"id": 1, "name": "piknik"},
                    {"id": 2, "name": "popularyzacja nauki"},
                    {"id": 3, "name": "uws"}
                ]
            }
        ]

        response = self.app.get('/api/events?month=10&year=2024')


        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)  
        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(response.get_json()[0]['title'], "Jubileuszowy Piknik Naukowy z Uniwersytetem w Siedlcach")  
        
    @patch('server.requests.get')
    def test_get_events_failure(self, mock_get):

        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {"error": "Unable to fetch events"}

        response = self.app.get('/api/events?month=15&year=2024')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.get_json())

    @patch('server.requests.get')
    def test_get_event_success(self, mock_get):

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 5,
            "name": "Konfernecja naukowa management 2024",
            "start_time": "2024-09-23T14:00:00",
            "duration": 2,
            "location": "Dwór mościbrody - Mościbrody 52, 08-112",
            "registration_link": "https://management.uws.edu.pl",
            "short_description": "XVII Międzynarodowa Konferencja MANAGEMENT 2024 to wydarzenie o rozwoju organizacji, pełne wykładów i inspirujących dyskusji.",
            "long_description": "Detailed description of the event."
        }

        response = self.app.get('/api/events/5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], "Konfernecja naukowa management 2024")

    @patch('server.requests.get')
    def test_get_event_not_found(self, mock_get):

        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"error": "Unable to fetch event details"}

        response = self.app.get('/api/events/9999')
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', response.get_json())

if __name__ == '__main__':
    unittest.main()