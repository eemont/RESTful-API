from flask import Flask, jsonify, render_template, request, make_response, session, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
  return "Hello World"

# TASK 2 : ERROR HANDLING

def error_response(status_code, message):
   response = jsonify({
      "error": {
         "code": status_code,
         "message": message
      }
   })

   response.status_code = status_code
   return status_code

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

# TASK 3 : AUTHENTICATION
    
