from flask import Blueprint, render_template, session

from src.routes.utils import is_logged_in

home_routes = Blueprint('home', __name__)


@home_routes.route('/')
@is_logged_in
def home():
    return render_template('index.html')
    
