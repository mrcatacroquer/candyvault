import datetime
import uuid

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from flask.ext.login import LoginManager
from flask.ext.login import login_required
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import current_user

import config

from mysqlhelper import MYSQLHelper

from passwordhelper import PasswordHelper
from user import User

from forms import RegistrationForm
from forms import LoginForm
from forms import APIAddRewardForm

app = Flask(__name__)
app.secret_key = "qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjkl"
login_manager = LoginManager(app)

DB = MYSQLHelper()
PH = PasswordHelper()


@login_manager.user_loader
def load_user(user_id):
    user = DB.get_user(user_id)
    if user:
        return User(user_id, user[4])

'''
************************
*******LOGIN************
************************
'''

@app.route("/httplogin", methods=["POST"])
def http_login():
    form = LoginForm(request.form)
    stored_user = DB.get_user(form.loginemail.data)
    if stored_user and PH.validate_password(form.loginpassword.data, stored_user[2], stored_user[3]):
        user = User(form.loginemail.data,  stored_user[4])
        login_user(user, remember=True)
        return "Welcome"
    return "Email or password invalid"

@app.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate():
        stored_user = DB.get_user(form.loginemail.data)

        if stored_user and PH.validate_password(form.loginpassword.data, stored_user[2], stored_user[3]):
            user = User(form.loginemail.data, stored_user[4])
            login_user(user, remember=True)

            if user.is_admin_user():
                return "Ualaaaa you're admin"
            return "hi there!"

        form.loginemail.errors.append("Email or password invalid")
    return render_template("home.html", loginform=form, registrationform=RegistrationForm())

@app.route("/register", methods=["POST"])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("Email address already registered")
            return render_template("home.html", loginform=LoginForm(), registrationform=form)
        salt = PH.get_salt()
        hashed = PH.get_hash(form.password2.data + salt)
        DB.add_user(str(form.email.data), str(salt), str(hashed), int("False" != 'False'), str("XXXXXXXXXXXXXX"))
        return render_template("home.html", loginform=LoginForm(), registrationform=form, onloadmessage="Registration successful. Please log in.")
    return render_template("home.html", loginform=LoginForm(), registrationform=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

'''
************************
*******HOME*************
************************
'''

@app.route("/")
def home():
    return render_template("home.html", loginform=LoginForm(), registrationform=RegistrationForm())

'''
************************
*******API ACTIONS******
************************
'''

@app.route("/addreward", methods=["POST"])
@login_required
def add_reward():
    if not current_user.is_admin_user():
        return "Nanai"

    form = APIAddRewardForm(request.form)
    reward_owner = form.rewardowner.data
    owner = DB.get_user(reward_owner)

    if not owner:
        return "nokay"

    reward_guid = str(uuid.uuid4())
    reward_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    DB.add_reward(reward_owner, reward_guid, reward_timestamp)

    return "okay"

'''
************************
*******APP START********
************************
'''

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)