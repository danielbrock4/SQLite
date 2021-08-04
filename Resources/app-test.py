# Create a New Python File and Import the Flask Dependency
from flask import Flask

# Create a New Flask App Instance
    #"Instance" is a general term in programming to refer to a singular version of something.
    # Add the following to your code to create a new Flask instance called app:
app = Flask(__name__)
    # This __name__ variable denotes the name of the current function. 
    # You can use the __name__ variable to determine if your code is being run from the command line or if it has been imported into another piece of code. 
    # Variables with underscores before and after them are called magic methods in Python.

# Create Flask Routes
    # Step1: Define the starting point, also known as the root. To do this, we'll use the function @app.route('/')
    # Step2: Create Whenever you make a route in Flask, you put the code you want in that specific route below @app.route()
@app.route('/') # The forward slash inside of the app.route denotes that we want to put our data at the root of our routes. The / is commonly known as the highest level of hierarchy in any computer system   
def hello_world():
    return 'Hello world'

# Run a Flask App
    # To run the app, we're first going to need to use the command line to navigate to the folder where we've saved our code. 
    # You should save this code in the same folder you've used in the rest of this module.
        # Environment variables are essentially dynamic variables in your computer. They are used to modify the way a certain aspect of the computer operates.
        # For our FLASK_APP environment variable, we want to modify the path that will run our app.py file so that we can run our file.
        # Commands:
            # export FLASK_APP=app.py (for Mac)
            # set FLASK_APP=app.py (for PC)
            # flask run
    # Copy and paste your localhost address into your web browser. Generally, a localhost will look something like this, for context.  
    
          