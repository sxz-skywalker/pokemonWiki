from flask import Blueprint, render_template

user_route = Blueprint('user', __name__)


@user_route.route('/')
def list_user():
    return render_template('user.html')
