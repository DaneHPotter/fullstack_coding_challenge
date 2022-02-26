Getting Started
-----------------------------------------------------------------

Hello! The beginning section of this README describes how to run the server for this code, along with how to access the API.

This code is running on Python 3.9, so to run it Python 3 will need to be installed.

Once Python is installed:

1. Setup.bat
Once the code is  unzipped, run setup.bat either by double clicking on the batch file or from the command line.

Setup.bat calls pip install for all of the required libraries to run the code.

Once complete, the Flask environment variables are set up next. This allows Flask to run the code immediately after everything is installed and set up. 

2. Access the app

When the code run, navigate to http://127.0.0.1:5000/ in your browser to access the front end for the API

Using the REST API
-----------------------------------------------------------------

Outside of just using the basic frontend for the API, you are able to access the API directly from command lines as well! You can ca


GET
+ /authentication: Input a header with the request to be given a key in return
    - Header: "Content-Type": "application/json"
+ /quotation: You can access this in the web browser with http://127.0.0.1:5000/quotation, this displays all of the current info given to the API as a way of confirming everything is being entered correctly.

POST
+ /quotation: This is the way to add in new quotes to the list of dictionaries "quotations". 
    - Header:
        * "Content-Type": "application/json"
        * "Authorization": "Bearer "+ the token gained from the authentication GET above


Final Notes
-----------------------------------------------------------------

This was my first ever attempt a Fullstack project! Since this was my first attempt I took over the estimated amount of time for this project, but I feel like I have certainly learned a lot throughout this process. Python is also a language I am not as familiar with, but this seemed like a good experience to learn multiple things at once!

I originally attempted to make it so the front end product had to check the ages instead of the API, but I realized that assumption was not going to hold weight in the end so I changed the API to check instead.

