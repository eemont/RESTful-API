from flask import Flask, render_template, request, make_response, session, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/')
def home():
  return "Hello World"
  
if __name__ == "__main__":
    app.run(debug=True, port=5001)