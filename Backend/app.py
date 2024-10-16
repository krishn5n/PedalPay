from flask import Flask, request,jsonify
from flask_cors import CORS
import datetime as dt
import re
import random
from flask_mysqldb import MySQL as mysql
from sqlalchemy import text
import time
app = Flask(__name__)

cycleid = set(['abc123'])
app.config['MYSQL_HOST'] = 'localhost'  # MySQL server host
app.config['MYSQL_USER'] = 'root'  # MySQL username
app.config['MYSQL_PASSWORD'] = 'keerkrish'  # MySQL password
app.config['MYSQL_DB'] = 'krish'  # Database name

CORS(app)

def genotp():
    otp = random.randint(100000, 999999)  # Generates a 6-digit random number
    return str(otp)

def validcycle(id):
    if id in cycleid:
        return True
    return False

@app.route('/getotp',methods=['POST'])
def getotp():
    try:
        body = request.json
        idgot = body['cycleid']
        #print(body)
        if validcycle(idgot):
            otp = genotp()
            #print(otp)
            return jsonify({'otp':otp,'Status':200})
        else:
            return jsonify({'Message':'Wrong Cycle ID generated','Status':300})
    except:
        return jsonify({'Message':'An Error has occured, try again Later','Status':400})
    
@app.route('/signin',methods=['POST'])
def signin():
    try:
        body = request.json
        email = body['email']
        password = body['password']
        '''SQL Function to check'''
        query = 'Select 1 from smartcities where email='+email+'password='+password
        cur = mysql.connection.cursor()
        cur.execute(query)
        user = cur.fetchone()
        print(user)
        mysql.connection.commit()
        if user:
            return jsonify({'Status':200})
        else:
            return jsonify({'Status':300})
    except:
        return jsonify({'Message':'An Error has occured, try again Later','Status':400})

if __name__ == '__main__':
    app.run(debug=True)