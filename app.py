from flask import Flask, json, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

import os

DB_URL = os.environ.get("URL")

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)

@app.route("/getLocation")
def getLocation():
    sql = """
        SELECT DISTINCT address, name FROM light
        """
    data = db.engine.execute(sql)
    res = data.fetchall();

    return jsonify({'result': [dict(row) for row in res]})

@app.route('/light/<location>', methods = ['GET'])
def getLight(location):
    data = db.engine.execute("""
                            SELECT DISTINCT time, value, address FROM light 
                            WHERE address = '%s' ORDER BY time ASC""" % (location) )
    res = data.fetchall()

    return jsonify({'result': [dict(row) for row in res]})

@app.route("/")
def map():
    return render_template("map.html")

app.config['DEBUG'] = True
app.run()