from flask import Blueprint, render_template, url_for, redirect, request, flash, jsonify

from src.controllers import UserController

seeder_routes = Blueprint('seeder', __name__)


def create_users():
    # DELETE ALL USERS
    users = UserController.read_all()
    for user in users:
        UserController.delete(user.id)

    # CREATE USERS
    UserController.create(
        'admin', 'admin', 'admin@gmail.com', 'password123', 'ADMIN')
    UserController.create('commercial', 'commercial',
                          'commercial@gmail.com', 'password123', 'COMMERCIAL')
    UserController.create('gestionnaire', 'gestionnaire',
                          'gestionnaire@gmail.com', 'password123', 'GESTIONNAIRE')
    UserController.create('analyste', 'analyste',
                          'analyste@gmail.com', 'password123', 'ANALYSTE')


@seeder_routes.route('/')
def init_db():
    create_users()
    return jsonify({"message": "Database initialized successfully."})
