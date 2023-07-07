from flask import Blueprint, request, render_template

routes = Blueprint('routes', __name__)

@routes.route('/', methods = ['GET','POST'])
def home():
    if request.method == 'GET':
        return render_template('login.html')
