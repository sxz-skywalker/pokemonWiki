from flask import Blueprint, render_template

main_route = Blueprint('main', __name__)


@main_route.route('/')
def index():
    return render_template('index.html')
