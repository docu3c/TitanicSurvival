from flask import Flask, render_template, request
# import pandas as pd
# import numpy as np
# import urllib.request
import json
import os
import ssl
import requests


app = Flask(__name__)

         

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/predict", methods=['POST'])

def predict():

    if request.method == 'POST':
        try:
            
            data = {
                    "PassengerId": int(request.form['Passengerid']),
                    "Survived": int(request.form['Survived']),
                    "Pclass": int(request.form['Pclass']),
                    "Sex": str(request.form['Sex']),
                    "Age": float(request.form['Age']),
                    "SibSp": int(request.form['SibSp']),
                    "Parch": int(request.form['Parch']),
                    "Ticket": str(request.form['Ticket']),
                    "Fare": float(request.form['Fare']),
                    "Cabin": str(request.form['Cabin'])
                    }
        except KeyError or ValueError:
            return "Please check if the values are entered correctly"
        
        def allowSelfSignedHttps(allowed):
            # bypass the server certificate verification on client side
            if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
                ssl._create_default_https_context = ssl._create_unverified_context
        
        allowSelfSignedHttps(True)
        
        body = str.encode(json.dumps([data]))
        
        url = "http://8497b35f-5aee-4ab4-882f-43cea7a2fb8e.eastus.azurecontainer.io/score"
    
        api_key = 'QgdsQr60k3sOVtOYOwXcZYOdKui1NUg9'
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")


        headers = {'Content-Type':'application/json', 'Authorization':('Bearer ' + api_key)}

        r = requests.post(url=url, data=body, headers=headers)
        print(r.status_code)
        print(r.content)

        result = json.loads(r.content)
    return render_template('predict.html', prediction = result)
    





if __name__== "_main_":
    app.run()