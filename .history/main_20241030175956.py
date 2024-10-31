from flask import Flask, render_template, request, make_response, session, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
  if 'UserID' in session:
    return redirect(url_for("profile"))
  else:
    return redirect(url_for("login"))
  
@app.route("/set_cookie_and_session", methods=["POST", "GET"])
def set_cookie_and_session():
  session['UserID'] = request.form["userID"]
  session['Visits'] = 1
  resp = make_response(render_template("profile.html", userID = session['UserID'], visits = session['Visits']))
  resp.set_cookie("userID", session['UserID'], expires=1800)
  return resp

@app.route('/login')
def login():
  return render_template("login.html")

@app.route('/profile')
def profile():
  session['Visits'] += 1
  name = request.cookies.get('userID')
  return render_template("profile.html", userID = session['UserID'], visits = session['Visits'])

@app.route('/logout')
def logout():
  session.pop('UserID')
  session.pop('Visits')
  resp = make_response(render_template("login.html"))
  resp.set_cookie('userID', '', expires="0")
  return redirect(url_for("login"))
  
  
if __name__ == "__main__":
    app.run(debug=True, port=5001)