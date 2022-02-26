import unittest
import requests

class TestAppMethods(unittest.TestCase):

    def test_normal_method(app):
        """
        Third Unit Test in order to just make sure that repeatedly
        sending new values to the API works correctly and without issue.
        """
        authURL = 'http://127.0.0.1:5000/authentication'
        hed = {"Content-Type": "application/json"}

        authR = requests.get(authURL, headers=hed)
        key = authR.json()

        hed = {"Content-Type": "application/json", "Authorization": "Bearer "+key['token']}

        ages = ["20, 45", "30, 34, 50", "18", "68, 33, 20", "40, 40, 20", "35, 49, 59, 31", "59"]

        for age in ages:
            data = {"ages": age, "cur_id": "USD", "start_date": "2020-10-1", "end_date": "2020-10-30"}
            url = 'http://127.0.0.1:5000/quotation'

            response = requests.post(url, json=data, headers=hed)
            if 'error' in response.json():
                value = False
            else:
                value = True
            print("The ID is: "+ str(response.json()['id']))
            app.assertTrue(value)

if __name__ == '__main__':
    unittest.main()