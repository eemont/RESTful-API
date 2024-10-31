from flask import Flask, jsonify, render_template, request, make_response, session, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_USER'] = 'USERNAME goes here'
app.config['MYSQL_PASSWORD'] = 'PASSWORD goes here'
app.config['MYSQL_HOST'] = 'Name of HOST (server) goes here'
app.config['MYSQL_DB'] = 'DATABASE goes here'
mysql = MySQL(app)

@app.route('/')
def home():
  cursor = mysql.connections
  return "Hello World"

def error_response(status_code, message):
   response = jsonify({
      "error": {
         "code": status_code,
         "message": message
      }
   })

   response.status_code = status_code
   return status_code
 
@app.route('/create_table')
def create_table():
  cursor = mysql.connection.cursor()
  cursor.execute("'CREATE TABLE midterm_database(username VARCHAR(20), password VARCHAR(20))'")
  cursor.execute("'INSERT INTO midterm_database VALUES(emmanuel_montoya, em12345)")
  cursor.execute("'INSERT INTO midterm_database VALUES(renzo_salosagcol, rs12345)")
  cursor.execute("'INSERT INTO midterm_database VALUES(anthony weathers, aw12345)")
  cursor.execute("'INSERT INTO midterm_database VALUES(alice_johnson, aj12345)")
  cursor.execute("'INSERT INTO midterm_database VALUES(brian_smith, bs12345)")
  cursor.execute("'INSERT INTO midterm_database VALUES(carla_brown, cb12345)")
  cursor.execute("'INSERT INTO midterm_database VALUES(david_taylor, dt12345)")
  cursor.execute("'INSERT INTO midterm_database VALUES(emily_davis, ed12345)")
  cursor.execute("'INSERT INTO midterm_database VALUES(frank_wilson, fw12345)")
  cursor.execute("'INSERT INTO midterm_database VALUES(grace_martinez, gm12345)")

# ERROR 400 - Bad Request
@app.errorhandler(400)
def bad_request(error):
   return error_response(400, "Bad Request")

# ERROR 401 - Unauthenticated
@app.errorhandler(401)
def bad_request(error):
   return error_response(401, "Unauthenticated")

# ERROR 403 - Forbidden
@app.errorhandler(403)
def bad_request(error):
   return error_response(404, "Forbidden")

# ERROR 404 - Page Not Found
@app.errorhandler(404)
def bad_request(error):
   return error_response(404, "Page Not Found")

# ERROR 406 - Not Acceptable
@app.errorhandler(406)
def bad_request(error):
   return error_response(406, "Not Acceptable")

# ERROR 415 - Page Not Found
@app.errorhandler(415)
def bad_request(error):
   return error_response(415, "Unsupported Media Type")

# ERROR 429 - Too Many Requests
@app.errorhandler(429)
def bad_request(error):
   return error_response(429, "Too Many Requests")


  
if __name__ == "__main__":
    app.run(debug=True, port=5001)