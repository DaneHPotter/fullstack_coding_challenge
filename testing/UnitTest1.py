import unittest
import requests

class TestAppMethods(unittest.TestCase):

    def test_normal_method(app):
        """
        First Unit Test in order to just make sure that a basic 
        action of getting a token then sending it back works well
        with the base app.py code
        """
        authURL = 'http://127.0.0.1:5000/authentication'
        hed = {"Content-Type": "application/json"}

        authR = requests.get(authURL, headers=hed)
        key = authR.json()

        hed = {"Content-Type": "application/json", "Authorization": "Bearer "+key['token']}
        #hed = {"Content-Type": "application/json", "Authorization": "Bearer + eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDU4MjMwMzh9.nNitwJfb0WSfyVyF6ToKweVGU5mWIUkkrTMQYFWF8vw"}

        data = {"ages": "20, 45", "cur_id": "USD", "start_date": "2020-10-1", "end_date": "2020-10-30"}
        url = 'http://127.0.0.1:5000/quotation'

        response = requests.post(url, json=data, headers=hed)
        if 'error' in response.json():
            value = False
        else:
            value = True
        app.assertTrue(value)

if __name__ == '__main__':
    unittest.main()