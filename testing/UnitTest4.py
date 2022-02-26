import unittest
import requests

class TestAppMethods(unittest.TestCase):

    def test_normal_method(app):
        """
        Fourth Unit Test, this time to display one of the flaws with the way
        that I designed this program. This fails due to the fact that the
        first age written into the data is less than 18 years old.
        """
        authURL = 'http://127.0.0.1:5000/authentication'
        hed = {"Content-Type": "application/json"}

        authR = requests.get(authURL, headers=hed)
        key = authR.json()

        hed = {"Content-Type": "application/json", "Authorization": "Bearer "+key['token']}
        
        data = {"ages": "17, 30", "cur_id": "USD", "start_date": "2020-10-1", "end_date": "2020-10-30"}
        url = 'http://127.0.0.1:5000/quotation'

        response = requests.post(url, json=data, headers=hed)
        if 'error' in response.json():
            value = False
        else:
            value = True
        print("The error is: "+str(response.json()['error']))
        app.assertTrue(value)


if __name__ == '__main__':
    unittest.main()