# Trip-Advisor
Trip Advisor is a web application made in Python and MongoDB using Flask Web Framework.  
This is a hotel and flight booking application.

## How to run
Step 1: Download the code  
Step 2: Download and install Python 3 (https://www.python.org/downloads/) and MongoDB (https://www.mongodb.com/download-center#community)  
Step 3: Open a terminal and navigate to the folder outside the main code folder ie. code  
Step 4: Run this command
```
virtualenv venv
```
Step 5: Navigate to venv\Scripts and type (Only for Windows users)
```
activate.bat
```
Step 6: Navigate back to code and type
```
python --version
```
You should be able to see the version of python that is installed.  
Step 7: Install other libraries
```
pip install flask datetime werkzeug passlib pymongo uuid
```
Step 8: Run the app
```
python run.py
```
