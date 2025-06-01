from flask import Blueprint, render_template

dashboard_routes = Blueprint(
    'dashboard', __name__, url_prefix='/dashboard'
)

@dashboard_routes.route('/')
def index():
    return render_template('dashboard/index.html')
