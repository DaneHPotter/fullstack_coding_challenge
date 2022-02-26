import unittest
#from app import *
import requests

class TestAppMethods(unittest.TestCase):

    def test_normal_method(app):
        """
        Second Unit Test, this time I was testing that the 
        API still needs the correct key. In this one I am assigning
        a different key entirely (a key that was originally used) to confirm that the test fails this time.
        """
        hed = {"Content-Type": "application/json", "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDU4MjMwMzh9.nNitwJfb0WSfyVyF6ToKweVGU5mWIUkkrTMQYFWF8vw"}

        data = {"ages": "20, 45", "cur_id": "USD", "start_date": "2020-10-1", "end_date": "2020-10-30"}
        url = 'http://127.0.0.1:5000/quotation'

        response = requests.post(url, json=data, headers=hed)
        # Testing to see if an error statement was sent back to the test
        if 'error' in response.json():
            value = False
        else:
            value = True
        print("The error is: "+str(response.json()['error']))
        app.assertTrue(value)

if __name__ == '__main__':
    unittest.main()