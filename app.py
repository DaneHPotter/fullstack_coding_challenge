# import the Flask class from the flask module
from flask import Flask, request, jsonify, make_response, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField, validators, IntegerField, DateField
from wtforms.validators import DataRequired
from datetime import date, timedelta, datetime
#from iso4217 import Currency
#from iso8601 import parse_date
import json
import requests
import jwt


# create the application object
app = Flask(__name__)

"""
# For this project I decided to simply use a key of my own creation
# If I were to do this project again I would create an env variable and have
the program call that instead for SECRET_KEY access
"""
app.config['SECRET_KEY'] = '753851326854128576523582'

# This is used to set up my basic HTML site later on
Bootstrap(app)

# The list of dictionaries that will be added to throughout the API's functions
quotations = []

def format_date(input):
    """
    The dates added into the API were entered in 
    as strings, to make sure the JSON found it acceptable.
    As such, the values needed to be convereted from string
    to date format. This seems a bit excessive in how I formatted
    this but since I am still new to python this is the best way I learned
    how to do this.
    """
    splitDate = input.split("-")
    mapDate = map(int, splitDate)
    listDate = list(mapDate)

    dateVal = date(listDate[0], listDate[1], listDate[2])
    return dateVal

def format_ages(input):
    """
    The ages needed to be turned from a comma separated string
    into a series of integers again, I just put them back into
    a list of integers again
    """
    splitAges = input.split(",")
    mapAges = map(int, splitAges)
    listAges = list(mapAges)
    return listAges


def tripCalculation(insuredAges, tripLength):
    """
    Takes in the list of already checked ages
    then simply goes down the list to calculate
    the overall cost of the Insurance

    Also checks to see if the first age is under
    18 years old, and if any ages are at 0. If this
    happens, the code takes advantage of Python's 
    fluidity of assigning variables and sends back an 
    error message
    """
    total = 0
    if insuredAges[0] < 18:
        return {"error": "Primary Insurer must be the age of 18 or older."}
    for age in insuredAges:
        if age == 0:
            return {"error": "Those being insured must be at least one year old to be insured. Please edit the values of those going on the trip to reflect this."}
        elif 18 <= age <= 30:
            total = total + (3 * .6 * tripLength)
        elif 31 <= age <= 40:
            total = total + (3 * .7 * tripLength)
        elif 41 <= age <= 50:
            total = total + (3 * .8 * tripLength)
        elif 51 <= age <= 60:
            total = total + (3 * .9 * tripLength)
        elif 61 <= age <= 70:
            total = total + (3 * 1 * tripLength)
    return (round(total, 2))

def find_next_id():
    """
    Goes through the list of dictionaries, quotations, to see
    the largest ID value and assigns sends back the largest value +1
    If the list of dictionaries is empty, it just sends back 1
    """
    if len(quotations) != 0:
        return max(quote["id"] for quote in quotations) + 1
    else:
        return 1


def decode_auth_token(auth_token):
    """
    Attempts to decode the authorization token
    Note: For the decode statement, I had to add in the algorithms section (and also for the endcode)
    In order to properly get the token to be what I needed it to be
    """
    try:
        payload = jwt.decode(auth_token, app.config['SECRET_KEY'], algorithms="HS256")
        return payload['exp']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please try again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please try again'
    
class QuoteForm(FlaskForm):
    """
    This is how the Form values are created, with the different fields.

    The ages StringField is checked inside the API to make sure all ages are valid
    
    The currID field is limited to 3 characters, which should align with the ISO 4217 field.

    The startDate and endDate use the DateField to have the user select the date that they want
    to use for the dates. This field follows the ISO 8601 format to the best of my knowledge.
    """
    ages = StringField('Please enter the ages of those going on the trip. Separate each age with a comma (i.e. 21,20,30, etc.)', validators=[DataRequired()])
    currID = StringField('Please enter your currency code. (I.e., USD, EUR, etc.)', validators=[validators.DataRequired(), validators.Length(min=3, max=3)])
    startDate = DateField('Please enter your start date. (I.e. YYYY-MM-DD)', validators=[validators.DataRequired()])
    endDate = DateField('Please enter your end date. (I.e. YYYY-MM-DD)', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')
    

@app.get("/quotation")
def get_quotations():
    return jsonify(quotations)

"""
This is where the bulk of the code happens in this project.

This is also where the testing will mostly be focused around, as there should be
tests to make sure the proper key is received for the user, as well as just testing
to make sure any values can be added without issue.
"""
@app.post("/quotation")
def get_quotation():
    if request.is_json:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                userInput = request.get_json()
                startDate = format_date(userInput.get("start_date"))
                endDate = format_date(userInput.get("end_date"))
                tripLength = endDate - startDate 
                tripLength = tripLength.days + 1 # The 1 is added here in order to make the entire trip dates inclusive
                insuredAges = format_ages(userInput.get("ages"))
                totalQuotation = tripCalculation(insuredAges, tripLength)
                if isinstance(totalQuotation, float):
                    quote = {"id": find_next_id(), "totalAmount": totalQuotation, "cur_id": userInput.get("cur_id")}
                    quotations.append(quote)
                    quote = json.dumps(quote) # Makes sure the quote is in JSON before returning the values
                    return quote
                else:
                    print(totalQuotation)
                    return make_response(jsonify(totalQuotation))
            else:
                return make_response(jsonify({"error": "Incorrect Token was sent, please call the authenticator again."}))
    return make_response(jsonify({"error": "Request must be JSON"}))

"""
An authentication page is necessary in order to get a JWT token to access /quotation
The assumption made here is that the user does *not* need to login for a token
This assumption is made due to the fact that there is a quotation_id sent back from
the POST statement above
"""
@app.get("/authentication")
def get_authentication():
    try:
        token = jwt.encode(
        {'exp': datetime.utcnow() + timedelta(minutes = 30)},
        app.config['SECRET_KEY'], algorithm="HS256")
        return make_response(jsonify({'token': token}), 201)
    except Exception as e:
       return e

"""
The default page that appears when you run this application for the first time
from the default address of http://127.0.0.1:5000 

This sets up the QuoteForm and the message that appears underneath the Submit button

When the form has valid inputs for every field, the API then checks to make sure
all of the ages entered are at the correct ages.
"""
@app.route("/", methods=['GET', 'POST'])
def get_webform():
    form = QuoteForm()
    message = ""
    if form.validate_on_submit():
        ages = form.ages.data
        delimAges = format_ages(ages)
        currID = form.currID.data
        startDate = str(form.startDate.data)
        endDate = str(form.endDate.data)

        # Get authorization Token
        authURL = 'http://127.0.0.1:5000/authentication'
        hed = {"Content-Type": "application/json"}
        authR = requests.get(authURL, headers=hed)
        token = authR.json()

        header = {"Content-Type": "application/json", "Authorization": "Bearer "+token['token']}
        data = {"ages": ages, "cur_id": currID, "start_date": startDate, "end_date": endDate}
        urlQ = 'http://127.0.0.1:5000/quotation'

        response = requests.post(urlQ, json=data, headers=header)
        quote = response.json()
        print(quote)
        if 'totalAmount' in quote:
            message = "Your total cost for the quote is "+ str(quote['totalAmount']) +" " + quote['cur_id'] \
                + ". The ID for your quote is " +  str(quote['id']) + "."
        else:
            message = quote['error']
    return render_template('index.html', form=form, message=message)